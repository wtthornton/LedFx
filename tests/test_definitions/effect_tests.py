from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class EffectTestCase(TestCase):
    """Test case for effect management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Effect management tests
effect_tests = {
    "create_effect": EffectTestCase(
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
        execution_order=1,
    ),
    "update_effect": EffectTestCase(
        api_endpoint="/api/effects/rainbow",
        method="PUT",
        payload_to_send={
            "config": {
                "speed": 2.0,
                "scale": 1.5,
                "brightness": 0.8,
            },
        },
        expected_return_code=200,
        expected_response_keys=["effect"],
        execution_order=2,
    ),
    "get_effect": EffectTestCase(
        api_endpoint="/api/effects/rainbow",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["effect"],
        execution_order=3,
    ),
    "activate_effect": EffectTestCase(
        api_endpoint="/api/effects/rainbow/activate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "deactivate_effect": EffectTestCase(
        api_endpoint="/api/effects/rainbow/deactivate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "delete_effect": EffectTestCase(
        api_endpoint="/api/effects/rainbow",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 