from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class ConcurrentTestCase(TestCase):
    """Test case for concurrent operations testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Concurrent operations tests
concurrent_tests = {
    "concurrent_device_creation": ConcurrentTestCase(
        api_endpoint="/api/devices/concurrent",
        method="POST",
        payload_to_send={
            "devices": [
                {
                    "name": f"Test Device {i}",
                    "type": "wled",
                    "config": {
                        "ip_address": f"192.168.1.{100 + i}",
                        "port": 21324,
                        "pixel_count": 30,
                    },
                }
                for i in range(5)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["devices"],
        execution_order=1,
    ),
    "concurrent_effect_creation": ConcurrentTestCase(
        api_endpoint="/api/effects/concurrent",
        method="POST",
        payload_to_send={
            "effects": [
                {
                    "type": "rainbow",
                    "config": {
                        "speed": 1.0,
                        "scale": 1.0,
                        "brightness": 1.0,
                    },
                }
                for _ in range(5)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["effects"],
        execution_order=2,
    ),
    "concurrent_scene_creation": ConcurrentTestCase(
        api_endpoint="/api/scenes/concurrent",
        method="POST",
        payload_to_send={
            "scenes": [
                {
                    "name": f"Test Scene {i}",
                    "config": {
                        "devices": [f"Test Device {i}"],
                        "effects": ["rainbow"],
                    },
                }
                for i in range(5)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["scenes"],
        execution_order=3,
    ),
    "concurrent_preset_creation": ConcurrentTestCase(
        api_endpoint="/api/presets/concurrent",
        method="POST",
        payload_to_send={
            "presets": [
                {
                    "name": f"Test Preset {i}",
                    "type": "scene",
                    "config": {
                        "scene": f"Test Scene {i}",
                        "settings": {
                            "brightness": 1.0,
                        },
                    },
                }
                for i in range(5)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["presets"],
        execution_order=4,
    ),
    "concurrent_scene_activation": ConcurrentTestCase(
        api_endpoint="/api/scenes/concurrent/activate",
        method="POST",
        payload_to_send={
            "scenes": [f"Test Scene {i}" for i in range(5)],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "concurrent_resource_cleanup": ConcurrentTestCase(
        api_endpoint="/api/cleanup/concurrent",
        method="POST",
        payload_to_send={
            "resources": [
                f"Test Device {i}"
                for i in range(5)
            ]
            + ["rainbow"]
            + [
                f"Test Scene {i}"
                for i in range(5)
            ]
            + [
                f"Test Preset {i}"
                for i in range(5)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 