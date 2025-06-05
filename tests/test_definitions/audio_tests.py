from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class AudioTestCase(TestCase):
    """Test case for audio management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Audio management tests
audio_tests = {
    "get_audio_devices": AudioTestCase(
        api_endpoint="/api/audio/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["devices"],
        execution_order=1,
    ),
    "set_audio_device": AudioTestCase(
        api_endpoint="/api/audio/device",
        method="POST",
        payload_to_send={
            "device": "Default Device",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=2,
    ),
    "get_audio_config": AudioTestCase(
        api_endpoint="/api/audio/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=3,
    ),
    "update_audio_config": AudioTestCase(
        api_endpoint="/api/audio/config",
        method="PUT",
        payload_to_send={
            "config": {
                "sample_rate": 44100,
                "chunk_size": 1024,
                "channels": 2,
            },
        },
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=4,
    ),
    "start_audio": AudioTestCase(
        api_endpoint="/api/audio/start",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "stop_audio": AudioTestCase(
        api_endpoint="/api/audio/stop",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "get_audio_analysis": AudioTestCase(
        api_endpoint="/api/audio/analysis",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analysis"],
        execution_order=7,
    ),
    "get_audio_visualization": AudioTestCase(
        api_endpoint="/api/audio/visualization",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["visualization"],
        execution_order=8,
    ),
} 