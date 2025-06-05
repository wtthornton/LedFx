from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class IntegrationTestCase(TestCase):
    """Test case for integration testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Integration tests
integration_tests = {
    "create_device_and_effect": IntegrationTestCase(
        api_endpoint="/api/devices",
        method="POST",
        payload_to_send={
            "name": "Test Device",
            "type": "wled",
            "config": {
                "ip_address": "192.168.1.100",
                "port": 21324,
                "pixel_count": 30,
            },
        },
        expected_return_code=200,
        expected_response_keys=["device"],
        execution_order=1,
    ),
    "create_effect_for_device": IntegrationTestCase(
        api_endpoint="/api/effects",
        method="POST",
        payload_to_send={
            "type": "rainbow",
            "config": {
                "speed": 1.0,
                "scale": 1.0,
                "brightness": 1.0,
            },
        },
        expected_return_code=200,
        expected_response_keys=["effect"],
        execution_order=2,
    ),
    "create_scene_with_device_and_effect": IntegrationTestCase(
        api_endpoint="/api/scenes",
        method="POST",
        payload_to_send={
            "name": "Test Scene",
            "config": {
                "devices": ["Test Device"],
                "effects": ["rainbow"],
            },
        },
        expected_return_code=200,
        expected_response_keys=["scene"],
        execution_order=3,
    ),
    "create_preset_for_scene": IntegrationTestCase(
        api_endpoint="/api/presets",
        method="POST",
        payload_to_send={
            "name": "Test Preset",
            "type": "scene",
            "config": {
                "scene": "Test Scene",
                "settings": {
                    "brightness": 1.0,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["preset"],
        execution_order=4,
    ),
    "activate_scene_with_preset": IntegrationTestCase(
        api_endpoint="/api/scenes/Test Scene/activate",
        method="POST",
        payload_to_send={
            "preset": "Test Preset",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "cleanup_test_resources": IntegrationTestCase(
        api_endpoint="/api/cleanup",
        method="POST",
        payload_to_send={
            "resources": [
                "Test Device",
                "rainbow",
                "Test Scene",
                "Test Preset",
            ],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 