from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class RecoveryTestCase(TestCase):
    """Test case for recovery testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Recovery tests
recovery_tests = {
    "device_recovery": RecoveryTestCase(
        api_endpoint="/api/devices/recovery",
        method="POST",
        payload_to_send={
            "device": "Test Device",
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=1,
    ),
    "effect_recovery": RecoveryTestCase(
        api_endpoint="/api/effects/recovery",
        method="POST",
        payload_to_send={
            "effect": "rainbow",
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=2,
    ),
    "scene_recovery": RecoveryTestCase(
        api_endpoint="/api/scenes/recovery",
        method="POST",
        payload_to_send={
            "scene": "Test Scene",
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "preset_recovery": RecoveryTestCase(
        api_endpoint="/api/presets/recovery",
        method="POST",
        payload_to_send={
            "preset": "Test Preset",
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "audio_recovery": RecoveryTestCase(
        api_endpoint="/api/audio/recovery",
        method="POST",
        payload_to_send={
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "network_recovery": RecoveryTestCase(
        api_endpoint="/api/network/recovery",
        method="POST",
        payload_to_send={
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "system_recovery": RecoveryTestCase(
        api_endpoint="/api/system/recovery",
        method="POST",
        payload_to_send={
            "action": "recover",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
} 