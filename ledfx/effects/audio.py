import logging
import queue
import threading
import time
from collections import deque
from functools import cached_property, lru_cache

import aubio
import numpy as np
import samplerate
try:
    import sounddevice as sd
except Exception:  # pragma: no cover - fallback when PortAudio is missing
    sd = None
import voluptuous as vol

import ledfx.api.websocket
from ledfx.api.websocket import WEB_AUDIO_CLIENTS, WebAudioStream
from ledfx.effects import Effect
from ledfx.effects.math import ExpFilter
from ledfx.effects.melbank import FFT_SIZE, MIC_RATE, Melbanks
from ledfx.events import AudioDeviceChangeEvent, Event

_LOGGER = logging.getLogger(__name__)

MIN_MIDI = 21
MAX_MIDI = 108


class AudioInputSource:
    _audio_stream_active = False
    _audio = None
    _stream = None
    _callbacks = []
    _audioWindowSize = 4
    _processed_audio_sample = None
    _volume = -90
    _volume_filter = ExpFilter(-90, alpha_decay=0.99, alpha_rise=0.99)
    _subscriber_threshold = 0
    _timer = None

    @staticmethod
    def device_index_validator(val):
        """
        Validates device index in case the saved setting is no longer valid
        """
        if val in AudioInputSource.valid_device_indexes():
            return val
        else:
            return AudioInputSource.default_device_index()

    @staticmethod
    def valid_device_indexes():
        """
        A list of integers corresponding to valid input devices
        """
        return tuple(AudioInputSource.input_devices().keys())

    @staticmethod
    def audio_input_device_exists():
        """
        Returns True if there are valid input devices
        """
        return len(AudioInputSource.valid_device_indexes()) > 0

    @staticmethod
    def default_device_index():
        """
        Finds the WASAPI loopback device index of the default output device if it exists
        If it does not exist, return the default input device index
        Returns:
            integer: the sounddevice device index to use for audio input
        """
        if sd is None:
            return None

        device_list = sd.query_devices()
        default_output_device_idx = sd.default.device["output"]
        default_input_device_idx = sd.default.device["input"]
        if len(device_list) == 0 or default_output_device_idx == -1:
            _LOGGER.warning("No audio output devices found.")
        else:
            default_output_device_name = device_list[
                default_output_device_idx
            ]["name"]

            # We need to run over the device list looking for the target devices name
            _LOGGER.debug(
                f"Looking for audio loopback device for default output device at index {default_output_device_idx}: {default_output_device_name}"
            )
            for device_index, device in enumerate(device_list):
                # sometimes the audio device name string is truncated, so we need to match what we have and Loopback but otherwise be sloppy
                if (
                    default_output_device_name in device["name"]
                    and "[Loopback]" in device["name"]
                ):
                    # Return the loopback device index
                    _LOGGER.debug(
                        f"Found audio loopback device for default output device at index {device_index}: {device['name']}"
                    )
                    return device_index

        # The default input device index is not always valid (i.e no default input devices)
        valid_device_indexes = AudioInputSource.valid_device_indexes()
        if len(valid_device_indexes) == 0:
            _LOGGER.warning(
                "No valid audio input devices found. Unable to use audio reactive effects."
            )
            return None
        else:
            if default_input_device_idx in valid_device_indexes:
                _LOGGER.debug(
                    f"No audio loopback device found for default output device. Using default input device at index {default_input_device_idx}: {device_list[default_input_device_idx]['name']}"
                )
                return default_input_device_idx
            else:
                # Return the first valid input device index if we can't find a valid default input device
                if len(valid_device_indexes) > 0:
                    first_valid_idx = next(iter(valid_device_indexes))
                    _LOGGER.debug(
                        f"No valid default audio input device found. Using first valid input device at index {first_valid_idx}: {device_list[first_valid_idx]['name']}"
                    )
                    return first_valid_idx

    @staticmethod
    def query_hostapis():
        if sd is None:
            return ({"name": "WEB AUDIO"},)
        return sd.query_hostapis() + ({"name": "WEB AUDIO"},)

    @staticmethod
    def query_devices():
        if sd is None:
            devices = ()
        else:
            devices = sd.query_devices()
        return devices + tuple(
            {
                "hostapi": len(AudioInputSource.query_hostapis()) - 1,
                "name": f"{client}",
                "max_input_channels": 1,
                "client": client,
            }
            for client in WEB_AUDIO_CLIENTS
        )

    @staticmethod
    def input_devices():
        hostapis = AudioInputSource.query_hostapis()
        devices = AudioInputSource.query_devices()
        return {
            idx: f"{hostapis[device['hostapi']]['name']}: {device['name']}"
            for idx, device in enumerate(devices)
            if (
                device.get("max_input_channels", 0) > 0
                and "asio" not in device["name"].lower()
            )
        }

    @staticmethod
    @property
    def AUDIO_CONFIG_SCHEMA():
        default_device_index = AudioInputSource.default_device_index()
        valid_device_indexes = AudioInputSource.valid_device_indexes()
        input_devices = AudioInputSource.input_devices()
        melbanks = Melbanks.CONFIG_SCHEMA
        audio_analysis = AudioAnalysisSource.CONFIG_SCHEMA
        return vol.Schema(
            {
                vol.Optional("sample_rate", default=60): int,
                vol.Optional("mic_rate", default=44100): int,
                vol.Optional("fft_size", default=FFT_SIZE): int,
                vol.Optional("min_volume", default=0.2): vol.All(
                    vol.Coerce(float), vol.Range(min=0.0, max=1.0)
                ),
                vol.Optional(
                    "audio_device", default=default_device_index
                ): AudioInputSource.device_index_validator,
                vol.Optional(
                    "delay_ms",
                    default=0,
                    description="Add a delay to LedFx's output to sync with your audio. Useful for Bluetooth devices which typically have a short audio lag.",
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=5000)),
            },
            extra=vol.ALLOW_EXTRA,
        )

    def __init__(self, ledfx, config):
        self._ledfx = ledfx
        self.lock = threading.Lock()
        # We must not inherit legacy _callbacks from prior instances
        self._callbacks = []
        self.update_config(config)

        def shutdown_event(e):
            # We give the rest of LedFx a second to shutdown before we deactivate the audio subsystem.
            # This is to prevent LedFx hanging on shutdown if the audio subsystem is still running while
            # effects are being unloaded. This is a bit hacky but it works.
            self._timer = threading.Timer(0.5, self.check_and_deactivate)
            self._timer.start()

        self._ledfx.events.add_listener(shutdown_event, Event.LEDFX_SHUTDOWN)

    def update_config(self, config):
        """Deactivate the audio, update the config, the reactivate"""
        old_input_device = False
        if hasattr(self, "_config"):
            old_input_device = self._config["audio_device"]

        if self._audio_stream_active:
            self.deactivate()
        self._config = self.AUDIO_CONFIG_SCHEMA.fget()(config)
        if len(self._callbacks) != 0:
            self.activate()
        if (
            old_input_device
            and self._config["audio_device"] is not old_input_device
        ):
            self._ledfx.events.fire_event(
                AudioDeviceChangeEvent(
                    self.input_devices()[self._config["audio_device"]]
                )
            )
        self._ledfx.config["audio"] = self._config

    def activate(self):
        if self._audio is None:
            try:
                self._audio = sd
            except OSError as Error:
                _LOGGER.critical(f"Sounddevice error: {Error}. Shutting down.")
                self._ledfx.stop()

        # Enumerate all of the input devices and find the one matching the
        # configured host api and device name
        input_devices = self.query_devices()

        hostapis = self.query_hostapis()
        default_device = self.default_device_index()
        if default_device is None:
            # There are no valid audio input devices, so we can't activate the audio source.
            # We should never get here, as we check for devices on start-up.
            # This likely just captures if a device is removed after start-up.
            _LOGGER.warning(
                "Audio input device not found. Unable to activate audio source. Deactivating."
            )
            self.deactivate()
            return
        valid_device_indexes = self.valid_device_indexes()
        _LOGGER.debug("********************************************")
        _LOGGER.debug("Valid audio input devices:")
        for index in valid_device_indexes:
            hostapi_name = hostapis[input_devices[index]["hostapi"]]["name"]
            device_name = input_devices[index]["name"]
            input_channels = input_devices[index]["max_input_channels"]
            _LOGGER.debug(
                f"Audio Device {index}\t{hostapi_name}\t{device_name}\tinput_channels: {input_channels}"
            )
        _LOGGER.debug("********************************************")
        device_idx = self._config["audio_device"]
        _LOGGER.debug(
            f"default_device: {default_device} config_device: {device_idx}"
        )

        if device_idx > max(valid_device_indexes):
            _LOGGER.warning(
                f"Audio device out of range: {device_idx}. Reverting to default input device: {default_device}"
            )
            device_idx = default_device

        elif device_idx not in valid_device_indexes:
            _LOGGER.warning(
                f"Audio device {input_devices[device_idx]['name']} not in valid_device_indexes. Reverting to default input device: {default_device}"
            )
            device_idx = default_device

        # Setup a pre-emphasis filter to balance the input volume of lows to highs
        self.pre_emphasis = aubio.digital_filter(3)
        # depending on the coeffs type, we need to use different pre_emphasis values to make em work better. allegedly.
        selected_coeff = self._ledfx.config["melbanks"]["coeffs_type"]
        if selected_coeff == "matt_mel":
            _LOGGER.debug("Using matt_mel settings for pre-emphasis.")
            self.pre_emphasis.set_biquad(
                0.8268, -1.6536, 0.8268, -1.6536, 0.6536
            )
        elif selected_coeff == "scott_mel":
            _LOGGER.debug("Using scott_mel settings for pre-emphasis.")
            self.pre_emphasis.set_biquad(
                1.3662, -1.9256, 0.5621, -1.9256, 0.9283
            )
        else:
            _LOGGER.debug("Using generic settings for pre-emphasis")
            self.pre_emphasis.set_biquad(
                0.85870, -1.71740, 0.85870, -1.71605, 0.71874
            )

        freq_domain_length = (self._config["fft_size"] // 2) + 1

        self._raw_audio_sample = np.zeros(
            MIC_RATE // self._config["sample_rate"],
            dtype=np.float32,
        )

        # Setup the phase vocoder to perform a windowed FFT
        self._phase_vocoder = aubio.pvoc(
            self._config["fft_size"],
            MIC_RATE // self._config["sample_rate"],
        )
        self._frequency_domain_null = aubio.cvec(self._config["fft_size"])
        self._frequency_domain = self._frequency_domain_null
        self._frequency_domain_x = np.linspace(
            0,
            MIC_RATE,
            freq_domain_length,
        )

        samples_to_delay = int(
            0.001 * self._config["delay_ms"] * self._config["sample_rate"]
        )
        if samples_to_delay:
            self.delay_queue = queue.Queue(maxsize=samples_to_delay)
        else:
            self.delay_queue = None

        def open_audio_stream(device_idx):
            """
            Opens an audio stream for the specified input device.
            Parameters:
            device_idx (int): The index of the input device to open the audio stream for.
            Behavior:
            - Detects if the device is a Windows WASAPI Loopback device and logs its name and channel count.
            - If the device is a WEB AUDIO device, initializes a WebAudioStream and sets it as the active audio stream.
            - For other devices, initializes an InputStream with the device's default sample rate and other parameters.
            - Initializes a resampler with the "sinc_fastest" algorithm that downmixes the source to a single-channel.
            - Logs the name of the opened audio source.
            - Starts the audio stream and sets the audio stream active flag to True.
            """

            device = input_devices[device_idx]
            channels = None
            if (
                hostapis[device["hostapi"]]["name"] == "Windows WASAPI"
                and "Loopback" in device["name"]
            ):
                _LOGGER.info(
                    f"Loopback device detected: {device['name']} with {device['max_input_channels']} channels"
                )
            else:
                # if are not a windows loopback device, we will downmix to mono
                # issue seen with poor audio behaviour on Mac and Linux
                # this is similar to the long standing prior implementation
                channels = 1

            if hostapis[device["hostapi"]]["name"] == "WEB AUDIO":
                ledfx.api.websocket.ACTIVE_AUDIO_STREAM = self._stream = (
                    WebAudioStream(
                        device["client"], self._audio_sample_callback
                    )
                )
            else:
                self._stream = self._audio.InputStream(
                    samplerate=int(device["default_samplerate"]),
                    device=device_idx,
                    callback=self._audio_sample_callback,
                    dtype=np.float32,
                    latency="low",
                    blocksize=int(
                        device["default_samplerate"]
                        / self._config["sample_rate"]
                    ),
                    # only pass channels if we set it to something other than None
                    **({"channels": channels} if channels is not None else {}),
                )

            self.resampler = samplerate.Resampler("sinc_fastest", channels=1)

            _LOGGER.info(
                f"Audio source opened: {hostapis[device['hostapi']]['name']}: {device.get('name', device.get('client'))}"
            )

            self._stream.start()
            self._audio_stream_active = True

        try:
            open_audio_stream(device_idx)
        except OSError as e:
            _LOGGER.critical(
                f"Unable to open Audio Device: {e} - please retry."
            )
            self.deactivate()
        except Exception as e:
            if sd is not None and isinstance(e, sd.PortAudioError):
                _LOGGER.error(f"{e}, Reverting to default input device")
                open_audio_stream(default_device)
            else:
                raise

    def deactivate(self):
        with self.lock:
            if self._stream:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            self._audio_stream_active = False
        _LOGGER.info("Audio source closed.")

    def subscribe(self, callback):
        """Registers a callback with the input source"""
        self._callbacks.append(callback)
        if len(self._callbacks) > 0 and not self._audio_stream_active:
            self.activate()
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def unsubscribe(self, callback):
        """Unregisters a callback with the input source"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
        if (
            len(self._callbacks) <= self._subscriber_threshold
            and self._audio_stream_active
        ):
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(5.0, self.check_and_deactivate)
            self._timer.start()

    def check_and_deactivate(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None
        if (
            len(self._callbacks) <= self._subscriber_threshold
            and self._audio_stream_active
        ):
            self.deactivate()

    def get_device_index_by_name(self, device_name: str):
        for key, value in self.input_devices().items():
            if device_name == value:
                return key
        return -1

    def _audio_sample_callback(self, in_data, frame_count, time_info, status):
        """Callback for when a new audio sample is acquired"""
        # time_start = time.time()
        # self._raw_audio_sample = np.frombuffer(in_data, dtype=np.float32)
        raw_sample = np.frombuffer(in_data, dtype=np.float32)

        in_sample_len = len(raw_sample)
        out_sample_len = MIC_RATE // self._config["sample_rate"]

        if in_sample_len != out_sample_len:
            # Simple resampling
            processed_audio_sample = self.resampler.process(
                raw_sample,
                # MIC_RATE / self._stream.samplerate
                out_sample_len / in_sample_len,
                # end_of_input=True
            )
        else:
            processed_audio_sample = raw_sample

        if len(processed_audio_sample) != out_sample_len:
            _LOGGER.debug(
                f"Discarded malformed audio frame - {len(processed_audio_sample)} samples, expected {out_sample_len}"
            )
            return

        # handle delaying the audio with the queue
        if self.delay_queue:
            try:
                self.delay_queue.put_nowait(processed_audio_sample)
            except queue.Full:
                self._raw_audio_sample = self.delay_queue.get_nowait()
                self.delay_queue.put_nowait(processed_audio_sample)
                self.pre_process_audio()
                self._invalidate_caches()
                self._invoke_callbacks()
        else:
            self._raw_audio_sample = processed_audio_sample
            self.pre_process_audio()
            self._invalidate_caches()
            self._invoke_callbacks()

        # print(f"Core Audio Processing Latency {round(time.time()-time_start, 3)} s")
        # return self._raw_audio_sample

    def _invoke_callbacks(self):
        """Notifies all clients of the new data"""
        for callback in self._callbacks:
            callback()

    def _invalidate_caches(self):
        """Invalidates the necessary cache"""
        pass

    def pre_process_audio(self):
        """
        Pre-processing stage that will run on every sample, only
        core functionality that will be used for every audio effect
        should be done here. Everything else should be deferred until
        queried by an effect.
        """
        # clean up nans that have been mysteriously appearing..
        self._raw_audio_sample[np.isnan(self._raw_audio_sample)] = 0

        # Calculate the current volume for silence detection
        self._volume = 1 + aubio.db_spl(self._raw_audio_sample) / 100
        self._volume = max(0, min(1, self._volume))
        self._volume_filter.update(self._volume)

        # Calculate the frequency domain from the filtered data and
        # force all zeros when below the volume threshold
        if self._volume_filter.value > self._config["min_volume"]:
            self._processed_audio_sample = self._raw_audio_sample

            # Perform a pre-emphasis to balance the highs and lows
            if self.pre_emphasis:
                self._processed_audio_sample = self.pre_emphasis(
                    self._raw_audio_sample
                )

            # Pass into the phase vocoder to get a windowed FFT
            self._frequency_domain = self._phase_vocoder(
                self._processed_audio_sample
            )
        else:
            self._frequency_domain = self._frequency_domain_null

    def audio_sample(self, raw=False):
        """Returns the raw audio sample"""

        if raw:
            return self._raw_audio_sample
        return self._processed_audio_sample

    def frequency_domain(self):
        return self._frequency_domain

    def volume(self, filtered=True):
        if filtered:
            return self._volume_filter.value
        return self._volume


class AudioAnalysisSource(AudioInputSource):
    # https://aubio.org/doc/latest/pitch_8h.html
    PITCH_METHODS = [
        "yinfft",
        "yin",
        "yinfast",
        # mcomb and fcomb appears to just explode something deeep in the aubio code, no logs, no errors, it just dies.
        # "mcomb",
        # "fcomb",
        "schmitt",
        "specacf",
    ]
    # https://aubio.org/doc/latest/specdesc_8h.html
    ONSET_METHODS = [
        "energy",
        "hfc",
        "complex",
        "phase",
        "wphase",
        "specdiff",
        "kl",
        "mkl",
        "specflux",
    ]
    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Optional(
                "pitch_method",
                default="yinfft",
                description="Method to detect pitch",
            ): vol.In(PITCH_METHODS),
            vol.Optional("tempo_method", default="default"): str,
            vol.Optional(
                "onset_method",
                default="hfc",
                description="Method used to detect onsets",
            ): vol.In(ONSET_METHODS),
            vol.Optional(
                "pitch_tolerance",
                default=0.8,
                description="Pitch detection tolerance",
            ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=2)),
        },
        extra=vol.ALLOW_EXTRA,
    )

    # some frequency constants
    # beat, bass, mids, high
    freq_max_mels = [
        100,
        250,
        3000,
        10000,
    ]

    def __init__(self, ledfx, config):
        config = self.CONFIG_SCHEMA(config)
        super().__init__(ledfx, config)
        self.initialise_analysis()

        # Subscribe functions to be run on every frame of audio
        self.subscribe(self.melbanks)
        self.subscribe(self.pitch)
        self.subscribe(self.onset)
        self.subscribe(self.bar_oscillator)
        self.subscribe(self.volume_beat_now)
        self.subscribe(self.freq_power)

        # ensure any new analysis callbacks are above this line
        self._subscriber_threshold = len(self._callbacks)

    def initialise_analysis(self):
        # melbanks
        if not hasattr(self, "melbanks"):
            self.melbanks = Melbanks(
                self._ledfx, self, self._ledfx.config.get("melbanks", {})
            )

        fft_params = (
            self._config["fft_size"],
            MIC_RATE // self._config["sample_rate"],
            MIC_RATE,
        )

        # pitch, tempo, onset
        self._tempo = aubio.tempo(self._config["tempo_method"], *fft_params)
        self._onset = aubio.onset(self._config["onset_method"], *fft_params)
        self._pitch = aubio.pitch(self._config["pitch_method"], *fft_params)
        self._pitch.set_unit("midi")
        self._pitch.set_tolerance(self._config["pitch_tolerance"])

        # bar oscillator
        self.beat_counter = 0

        # beat oscillator
        self.beat_timestamp = time.time()
        self.beat_period = 2

        # freq power
        self.freq_power_raw = np.zeros(len(self.freq_max_mels))
        self.freq_power_filter = ExpFilter(
            np.zeros(len(self.freq_max_mels)), alpha_decay=0.2, alpha_rise=0.97
        )
        self.freq_mel_indexes = []

        for freq in self.freq_max_mels:
            assert self.melbanks.melbanks_config["max_frequencies"][2] >= freq

            self.freq_mel_indexes.append(
                next(
                    (
                        i
                        for i, f in enumerate(
                            self.melbanks.melbank_processors[
                                2
                            ].melbank_frequencies
                        )
                        if f > freq
                    ),
                    len(
                        self.melbanks.melbank_processors[2].melbank_frequencies
                    ),
                )
            )

        # volume based beat detection
        self.beat_max_mel_index = next(
            (
                i - 1
                for i, f in enumerate(
                    self.melbanks.melbank_processors[0].melbank_frequencies
                )
                if f > self.freq_max_mels[0]
            ),
            self.melbanks.melbank_processors[0].melbank_frequencies[-1],
        )

        self.beat_min_percent_diff = 0.5
        self.beat_min_time_since = 0.1
        self.beat_min_amplitude = 0.5
        self.beat_power_history_len = int(self._config["sample_rate"] * 0.2)

        self.beat_prev_time = time.time()
        self.beat_power_history = deque(maxlen=self.beat_power_history_len)

    def update_config(self, config):
        validated_config = self.CONFIG_SCHEMA(config)
        super().update_config(validated_config)
        self.initialise_analysis()

    def _invalidate_caches(self):
        """Invalidates the cache for all melbank related data"""
        super()._invalidate_caches()

        self.pitch.cache_clear()
        self.onset.cache_clear()
        self.bpm_beat_now.cache_clear()
        self.volume_beat_now.cache_clear()
        self.bar_oscillator.cache_clear()

    @lru_cache(maxsize=None)
    def pitch(self):
        # If our audio handler is returning null, then we just return 0 for midi_value and wait for the device starts sending audio.
        try:
            return self._pitch(self.audio_sample(raw=True))[0]
        except ValueError as e:
            _LOGGER.warning(e)
            return 0

    @lru_cache(maxsize=None)
    def onset(self):
        try:
            return bool(self._onset(self.audio_sample(raw=True))[0])
        except ValueError as e:
            _LOGGER.warning(e)
            return 0

    @lru_cache(maxsize=None)
    def bpm_beat_now(self):
        """
        Returns True if a beat is expected now based on BPM data
        """
        try:
            return bool(self._tempo(self.audio_sample(raw=True))[0])
        except ValueError as e:
            _LOGGER.warning(e)
            return False

    @lru_cache(maxsize=None)
    def volume_beat_now(self):
        """
        Returns True if a beat is expected now based on volume of the beat freq region
        This algorithm is a bit weird, but works quite nicely.
        I've tried my best to optimise it from the original
        implementation in systematic_leds
        """

        time_now = time.time()
        melbank = self.melbanks.melbanks[0][: self.beat_max_mel_index]
        beat_power = np.sum(melbank)
        melbank_max = np.max(melbank)

        # calculates the % difference of the first value of the channel to the average for the channel
        if sum(self.beat_power_history) > 0:
            difference = (
                beat_power
                * self.beat_power_history_len
                / sum(self.beat_power_history)
                - 1
            )
        else:
            difference = 0

        self.beat_power_history.appendleft(beat_power)

        if (
            difference >= self.beat_min_percent_diff
            and melbank_max >= self.beat_min_amplitude
            and time_now - self.beat_prev_time > self.beat_min_time_since
        ):
            self.beat_prev_time = time_now
            return True
        else:
            return False

    def freq_power(self):
        # hard coded this bc i'm tired and it'll run faster

        melbank = self.melbanks.melbanks[2]

        self.freq_power_raw[0] = np.average(
            melbank[: self.freq_mel_indexes[0]]
        )
        self.freq_power_raw[1] = np.average(
            melbank[self.freq_mel_indexes[0] : self.freq_mel_indexes[1]]
        )
        self.freq_power_raw[2] = np.average(
            melbank[self.freq_mel_indexes[1] : self.freq_mel_indexes[2]]
        )
        self.freq_power_raw[3] = np.average(
            melbank[self.freq_mel_indexes[2] : self.freq_mel_indexes[3]]
        )
        np.minimum(self.freq_power_raw, 1, out=self.freq_power_raw)
        self.freq_power_filter.update(self.freq_power_raw)

    def get_freq_power(self, i, filtered=True):
        if filtered:
            value = self.freq_power_filter.value[i]
        else:
            value = self.freq_power_raw[i]

        return value if not np.isnan(value) else 0.0

    def beat_power(self, filtered=True):
        """
        Returns a float (0<=x<=1) corresponding to the beat power
        """
        return self.get_freq_power(0, filtered)

    def bass_power(self, filtered=True):
        """
        Returns a float (0<=x<=1) corresponding to the bass power
        """
        return self.get_freq_power(1, filtered)

    def lows_power(self, filtered=True):
        """
        Returns a float (0<=x<=1) corresponding to the lows power.
        this is just the sum of bass and beat power.
        """
        return (
            self.get_freq_power(0, filtered) + self.get_freq_power(1, filtered)
        ) * 0.5

    def mids_power(self, filtered=True):
        """
        Returns a float (0<=x<=1) corresponding to the mids power
        """
        return self.get_freq_power(2, filtered)

    def high_power(self, filtered=True):
        """
        Returns a float (0<=x<=1) corresponding to the highs power
        """
        return self.get_freq_power(3, filtered)

    @lru_cache(maxsize=None)
    def bar_oscillator(self):
        """
        Returns a float (0<=x<4) corresponding to the position of the beat
        tracker in the musical bar (4 beats)
        This is synced and quantized to the bpm of whatever is playing.
        While the beat number might not necessarily be accurate, the
        relative position of the tracker between beats will be quite accurate.

        NOTE: currently this makes no attempt to guess which beat is the first
        in the bar. It simple counts to four with each beat that is detected.
        The actual value of the current beat in the bar is completely arbitrary,
        but in time with each beat.

        0           1           2           3
        {----------time for one bar---------}
               ^    -->      -->      -->
            value of
        beat grid pointer
        """
        # update tempo and oscillator
        # print(self._tempo.get_delay_s())
        if self.bpm_beat_now():
            self.beat_counter = (self.beat_counter + 1) % 4
            self.beat_period = self._tempo.get_period_s()
            # print("beat at:", self._tempo.get_delay_s())
            self.beat_timestamp = time.time()
            oscillator = self.beat_counter
        else:
            time_since_beat = time.time() - self.beat_timestamp
            oscillator = (
                1 - (self.beat_period - time_since_beat) / self.beat_period
            ) + self.beat_counter
            # ensure it's between [0 and 4). useful when audio cuts
            oscillator = oscillator % 4
        return oscillator

    def beat_oscillator(self):
        """
        returns a float (0<=x<1) corresponding to the relative position of the
        bar oscillator in the current beat.

        0                0.5                 <1
        {----------time for one beat---------}
               ^    -->      -->      -->
            value of
           oscillator
        """
        return self.bar_oscillator() % 1


@Effect.no_registration
class AudioReactiveEffect(Effect):
    """
    Base for audio reactive effects. This really just subscribes
    to the melbank input source and forwards input along to the
    subclasses. This can be expanded to do the common r/g/b filters.
    """

    # this can be used by inheriting classes for power func selection in schema
    # see magnitude or scan effect for examples
    POWER_FUNCS_MAPPING = {
        "Beat": "beat_power",
        "Bass": "bass_power",
        "Lows (beat+bass)": "lows_power",
        "Mids": "mids_power",
        "High": "high_power",
    }

    def __init__(self, ledfx, config):
        super().__init__(ledfx, config)
        # protect against possible deactivate race condition
        self.audio = None

    def activate(self, channel):
        _LOGGER.info("Activating AudioReactiveEffect.")
        super().activate(channel)

        if not self._ledfx.audio or id(AudioAnalysisSource) != id(
            self._ledfx.audio.__class__
        ):
            self._ledfx.audio = AudioAnalysisSource(
                self._ledfx, self._ledfx.config.get("audio", {})
            )

        self.audio = self._ledfx.audio
        self._ledfx.audio.subscribe(self._audio_data_updated)

    def deactivate(self):
        _LOGGER.info("Deactivating AudioReactiveEffect.")
        if self.audio:
            self.audio.unsubscribe(self._audio_data_updated)
        super().deactivate()

    def create_filter(self, alpha_decay, alpha_rise):
        # TODO: Since most effects reuse the same general filters it would be
        # nice for all that computation to be shared. This mean that shared
        # filters are needed, or if there is really just a small set of filters
        # that those get added to the Melbank input source instead.
        return ExpFilter(alpha_decay=alpha_decay, alpha_rise=alpha_rise)

    def _audio_data_updated(self):
        self.melbank.cache_clear()
        with self.lock:
            if self.is_active:
                self.audio_data_updated(self.audio)

    def audio_data_updated(self, data):
        """
        Callback for when the audio data is updated. Should
        be implemented by subclasses
        """
        pass

    def clear_melbank_freq_props(self):
        """
        Clears the cached data for selecting and interpolating melbank.
        Almost all the properties used to build the melbank are cached
        to try and ease computational load.
        """

        for prop in [
            "_selected_melbank",
            "_melbank_min_idx",
            "_melbank_max_idx",
            "_input_mel_length",
        ]:
            if hasattr(self, prop):
                delattr(self, prop)

        self._melbank_interp_linspaces.cache_clear()

    @cached_property
    def _selected_melbank(self):
        return next(
            (
                i
                for i, x in enumerate(
                    self.audio.melbanks.melbanks_config["max_frequencies"]
                )
                if x >= self._virtual.frequency_range.max
            ),
            len(self.audio.melbanks.melbanks_config["max_frequencies"]),
        )

    @cached_property
    def _melbank_min_idx(self):
        return next(
            idx
            for idx, freq in enumerate(
                self.audio.melbanks.melbank_processors[
                    self._selected_melbank
                ].melbank_frequencies
            )
            if freq >= self._virtual.frequency_range.min
        )

    @cached_property
    def _melbank_max_idx(self):
        return next(
            (
                idx
                for idx, freq in enumerate(
                    self.audio.melbanks.melbank_processors[
                        self._selected_melbank
                    ].melbank_frequencies
                )
                if freq >= self._virtual.frequency_range.max
            ),
            len(
                self.audio.melbanks.melbank_processors[
                    self._selected_melbank
                ].melbank_frequencies
            ),
        )

    @cached_property
    def _input_mel_length(self):
        return self._melbank_max_idx - self._melbank_min_idx

    @lru_cache(maxsize=16)
    def _melbank_interp_linspaces(self, size):
        old = np.linspace(0, 1, self._input_mel_length)
        new = np.linspace(0, 1, size)
        return (new, old)

    def melbank_no_nan(self, melbank):
        # Check for NaN values in the melbank array, replace with 0 in place
        # Difficult to determine why this happens, but it seems to be related to
        # the audio input device.
        # TODO: Investigate why NaNs are present in the melbank array for some people/devices
        if np.isnan(melbank).any():
            _LOGGER.warning(
                "NaN values detected in the melbank array and replaced with 0."
            )
            # Replace NaN values with 0
            np.nan_to_num(melbank, copy=False)

    @lru_cache(maxsize=None)
    def melbank(self, filtered=False, size=0):
        """
        This little bit of code pulls together information from the effect's
        virtual (which controls the audio frequency range), and uses that
        to deliver the melbank, correctly selected and interpolated, to the effect

        size, int      : interpolate the melbank to the target size. value of 0 is no interpolation
        filtered, bool : melbank with smoothed attack and decay
        """
        if filtered:
            melbank = self.audio.melbanks.melbanks_filtered[
                self._selected_melbank
            ][self._melbank_min_idx : self._melbank_max_idx]
        else:
            melbank = self.audio.melbanks.melbanks[self._selected_melbank][
                self._melbank_min_idx : self._melbank_max_idx
            ]

        self.melbank_no_nan(melbank)

        if size and (self._input_mel_length != size):
            return np.interp(*self._melbank_interp_linspaces(size), melbank)
        else:
            return melbank

    def melbank_thirds(self, **kwargs):
        """
        Returns the melbank split into three sections (unequal length)
        Useful for effects that use lows, mids, and highs
        """
        melbank = self.melbank(**kwargs)
        mel_length = len(melbank)
        splits = tuple(map(lambda i: int(i * mel_length), [0.2, 0.5]))

        return np.split(melbank, splits)
