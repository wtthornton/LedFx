from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class ErrorTestCase(TestCase):
    """Test case for error handling."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 400
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Error handling tests
error_tests = {
    "invalid_device_config": ErrorTestCase(
        api_endpoint="/api/devices",
        method="POST",
        payload_to_send={
            "name": "Test Device",
            "type": "invalid_type",
            "config": {
                "ip_address": "invalid_ip",
                "port": -1,
                "pixel_count": 0,
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=1,
    ),
    "invalid_effect_config": ErrorTestCase(
        api_endpoint="/api/effects",
        method="POST",
        payload_to_send={
            "type": "invalid_effect",
            "config": {
                "speed": -1.0,
                "scale": 0.0,
                "brightness": 2.0,
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=2,
    ),
    "invalid_scene_config": ErrorTestCase(
        api_endpoint="/api/scenes",
        method="POST",
        payload_to_send={
            "name": "Test Scene",
            "config": {
                "devices": ["NonExistentDevice"],
                "effects": ["NonExistentEffect"],
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=3,
    ),
    "invalid_preset_config": ErrorTestCase(
        api_endpoint="/api/presets",
        method="POST",
        payload_to_send={
            "name": "Test Preset",
            "type": "invalid_type",
            "config": {
                "scene": "NonExistentScene",
                "settings": {
                    "brightness": 2.0,
                },
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=4,
    ),
    "invalid_audio_config": ErrorTestCase(
        api_endpoint="/api/audio/config",
        method="PUT",
        payload_to_send={
            "config": {
                "sample_rate": -1,
                "chunk_size": 0,
                "channels": 0,
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=5,
    ),
    "invalid_network_config": ErrorTestCase(
        api_endpoint="/api/network/config",
        method="PUT",
        payload_to_send={
            "config": {
                "interface": "invalid_interface",
                "ip_address": "invalid_ip",
                "netmask": "invalid_netmask",
                "gateway": "invalid_gateway",
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=6,
    ),
    "invalid_system_config": ErrorTestCase(
        api_endpoint="/api/system/config",
        method="PUT",
        payload_to_send={
            "config": {
                "log_level": "INVALID_LEVEL",
                "debug_mode": "not_a_boolean",
                "auto_start": "not_a_boolean",
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=7,
    ),
} 