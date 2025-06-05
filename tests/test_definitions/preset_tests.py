from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class PresetTestCase(TestCase):
    """Test case for preset management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Preset management tests
preset_tests = {
    "create_preset": PresetTestCase(
        api_endpoint="/api/presets",
        method="POST",
        payload_to_send={
            "name": "Test Preset",
            "type": "effect",
            "config": {
                "effect": "rainbow",
                "settings": {
                    "speed": 1.0,
                    "scale": 1.0,
                    "brightness": 1.0,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["preset"],
        execution_order=1,
    ),
    "update_preset": PresetTestCase(
        api_endpoint="/api/presets/Test Preset",
        method="PUT",
        payload_to_send={
            "config": {
                "effect": "rainbow",
                "settings": {
                    "speed": 2.0,
                    "scale": 1.5,
                    "brightness": 0.8,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["preset"],
        execution_order=2,
    ),
    "get_preset": PresetTestCase(
        api_endpoint="/api/presets/Test Preset",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["preset"],
        execution_order=3,
    ),
    "apply_preset": PresetTestCase(
        api_endpoint="/api/presets/Test Preset/apply",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "delete_preset": PresetTestCase(
        api_endpoint="/api/presets/Test Preset",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
} 