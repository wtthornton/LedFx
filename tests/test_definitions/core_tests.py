from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class CoreTestCase(TestCase):
    """Test case for core functionality."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Core functionality tests
core_tests = {
    "get_version": CoreTestCase(
        api_endpoint="/api/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["version", "platform"],
        execution_order=1,
    ),
    "get_config": CoreTestCase(
        api_endpoint="/api/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=2,
    ),
    "get_audio_devices": CoreTestCase(
        api_endpoint="/api/audio/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["devices"],
        execution_order=3,
    ),
    "get_audio_config": CoreTestCase(
        api_endpoint="/api/audio/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=4,
    ),
    "get_effects": CoreTestCase(
        api_endpoint="/api/effects",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["effects"],
        execution_order=5,
    ),
    "get_devices": CoreTestCase(
        api_endpoint="/api/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["devices"],
        execution_order=6,
    ),
    "get_virtuals": CoreTestCase(
        api_endpoint="/api/virtuals",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["virtuals"],
        execution_order=7,
    ),
    "get_scenes": CoreTestCase(
        api_endpoint="/api/scenes",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["scenes"],
        execution_order=8,
    ),
    "get_presets": CoreTestCase(
        api_endpoint="/api/presets",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["presets"],
        execution_order=9,
    ),
} 