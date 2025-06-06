import asyncio
import logging

from ledfx.events import Event

_LOGGER = logging.getLogger(__name__)


class VisDeduplicateQ(asyncio.Queue):
    """Deduplicate queue for visualisation updates."""

    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        # Maintain a set of keys for constant time duplicate checks
        self._dedupe_keys: set[tuple[str, str | None]] = set()

    def _make_key(self, item) -> tuple[str, str | None]:
        return item.get("event_type"), item.get("vis_id")

    def put_nowait(self, item):
        # to debug depth of queues and queue leakage enable teleplot below
        # from ledfx.utils import Teleplot
        # Teleplot.send(f"{hex(id(self))}:{self.qsize()}")

        if item and item.get("event_type") in (
            Event.DEVICE_UPDATE,
            Event.VISUALISATION_UPDATE,
        ):
            key = self._make_key(item)
            if key in self._dedupe_keys:
                _LOGGER.info(
                    f"Queue: {hex(id(self))} discarding, qsize {self.qsize()}"
                )
                return
            self._dedupe_keys.add(key)

        super().put_nowait(item)

    async def put(self, item):
        if item and item.get("event_type") in (
            Event.DEVICE_UPDATE,
            Event.VISUALISATION_UPDATE,
        ):
            key = self._make_key(item)
            if key in self._dedupe_keys:
                _LOGGER.info(
                    f"Queue: {hex(id(self))} discarding, qsize {self.qsize()}"
                )
                return
            self._dedupe_keys.add(key)
        await super().put(item)

    def get_nowait(self):
        item = super().get_nowait()
        if item and item.get("event_type") in (
            Event.DEVICE_UPDATE,
            Event.VISUALISATION_UPDATE,
        ):
            self._dedupe_keys.discard(self._make_key(item))
        return item

    async def get(self):
        item = await super().get()
        if item and item.get("event_type") in (
            Event.DEVICE_UPDATE,
            Event.VISUALISATION_UPDATE,
        ):
            self._dedupe_keys.discard(self._make_key(item))
        return item

    def is_similar(self, new, queued):
        # We know we are already one of the correct types, but is it the same as queued
        # then check if it is for the same device

        # Protect against None events
        if new is None or queued is None:
            return False

        if new.get("event_type") == queued.get("event_type") and new.get(
            "vis_id"
        ) == queued.get("vis_id"):
            return True

        return False
