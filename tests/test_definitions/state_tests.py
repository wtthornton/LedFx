from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class StateTestCase(TestCase):
    """Test case for state management testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# State management tests
state_tests = {
    "save_device_state": StateTestCase(
        api_endpoint="/api/devices/state",
        method="POST",
        payload_to_send={
            "device": "Test Device",
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=1,
    ),
    "load_device_state": StateTestCase(
        api_endpoint="/api/devices/state",
        method="POST",
        payload_to_send={
            "device": "Test Device",
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=2,
    ),
    "save_effect_state": StateTestCase(
        api_endpoint="/api/effects/state",
        method="POST",
        payload_to_send={
            "effect": "rainbow",
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "load_effect_state": StateTestCase(
        api_endpoint="/api/effects/state",
        method="POST",
        payload_to_send={
            "effect": "rainbow",
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "save_scene_state": StateTestCase(
        api_endpoint="/api/scenes/state",
        method="POST",
        payload_to_send={
            "scene": "Test Scene",
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "load_scene_state": StateTestCase(
        api_endpoint="/api/scenes/state",
        method="POST",
        payload_to_send={
            "scene": "Test Scene",
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "save_preset_state": StateTestCase(
        api_endpoint="/api/presets/state",
        method="POST",
        payload_to_send={
            "preset": "Test Preset",
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
    "load_preset_state": StateTestCase(
        api_endpoint="/api/presets/state",
        method="POST",
        payload_to_send={
            "preset": "Test Preset",
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=8,
    ),
    "save_audio_state": StateTestCase(
        api_endpoint="/api/audio/state",
        method="POST",
        payload_to_send={
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=9,
    ),
    "load_audio_state": StateTestCase(
        api_endpoint="/api/audio/state",
        method="POST",
        payload_to_send={
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=10,
    ),
    "save_network_state": StateTestCase(
        api_endpoint="/api/network/state",
        method="POST",
        payload_to_send={
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=11,
    ),
    "load_network_state": StateTestCase(
        api_endpoint="/api/network/state",
        method="POST",
        payload_to_send={
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=12,
    ),
    "save_system_state": StateTestCase(
        api_endpoint="/api/system/state",
        method="POST",
        payload_to_send={
            "action": "save",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=13,
    ),
    "load_system_state": StateTestCase(
        api_endpoint="/api/system/state",
        method="POST",
        payload_to_send={
            "action": "load",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=14,
    ),
} 