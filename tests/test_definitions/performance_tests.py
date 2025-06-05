from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class PerformanceTestCase(TestCase):
    """Test case for performance testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Performance tests
performance_tests = {
    "create_multiple_devices": PerformanceTestCase(
        api_endpoint="/api/devices/batch",
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
                for i in range(10)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["devices"],
        execution_order=1,
    ),
    "create_multiple_effects": PerformanceTestCase(
        api_endpoint="/api/effects/batch",
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
                for _ in range(10)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["effects"],
        execution_order=2,
    ),
    "create_multiple_scenes": PerformanceTestCase(
        api_endpoint="/api/scenes/batch",
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
                for i in range(10)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["scenes"],
        execution_order=3,
    ),
    "create_multiple_presets": PerformanceTestCase(
        api_endpoint="/api/presets/batch",
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
                for i in range(10)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["presets"],
        execution_order=4,
    ),
    "activate_multiple_scenes": PerformanceTestCase(
        api_endpoint="/api/scenes/batch/activate",
        method="POST",
        payload_to_send={
            "scenes": [f"Test Scene {i}" for i in range(10)],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "cleanup_test_resources": PerformanceTestCase(
        api_endpoint="/api/cleanup",
        method="POST",
        payload_to_send={
            "resources": [
                f"Test Device {i}"
                for i in range(10)
            ]
            + ["rainbow"]
            + [
                f"Test Scene {i}"
                for i in range(10)
            ]
            + [
                f"Test Preset {i}"
                for i in range(10)
            ],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 