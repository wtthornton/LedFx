from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class DeviceTestCase(TestCase):
    """Test case for device management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Device management tests
device_tests = {
    "create_device": DeviceTestCase(
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
    "update_device": DeviceTestCase(
        api_endpoint="/api/devices/Test Device",
        method="PUT",
        payload_to_send={
            "config": {
                "ip_address": "192.168.1.101",
                "port": 21324,
                "pixel_count": 30,
            },
        },
        expected_return_code=200,
        expected_response_keys=["device"],
        execution_order=2,
    ),
    "get_device": DeviceTestCase(
        api_endpoint="/api/devices/Test Device",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["device"],
        execution_order=3,
    ),
    "activate_device": DeviceTestCase(
        api_endpoint="/api/devices/Test Device/activate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "deactivate_device": DeviceTestCase(
        api_endpoint="/api/devices/Test Device/deactivate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "delete_device": DeviceTestCase(
        api_endpoint="/api/devices/Test Device",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 