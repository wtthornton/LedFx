from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class VirtualTestCase(TestCase):
    """Test case for virtual device management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Virtual device management tests
virtual_tests = {
    "create_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals",
        method="POST",
        payload_to_send={
            "name": "Test Virtual",
            "type": "matrix",
            "config": {
                "rows": 8,
                "columns": 8,
                "pixel_count": 64,
            },
        },
        expected_return_code=200,
        expected_response_keys=["virtual"],
        execution_order=1,
    ),
    "update_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals/Test Virtual",
        method="PUT",
        payload_to_send={
            "config": {
                "rows": 16,
                "columns": 16,
                "pixel_count": 256,
            },
        },
        expected_return_code=200,
        expected_response_keys=["virtual"],
        execution_order=2,
    ),
    "get_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals/Test Virtual",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["virtual"],
        execution_order=3,
    ),
    "activate_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals/Test Virtual/activate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "deactivate_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals/Test Virtual/deactivate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "delete_virtual": VirtualTestCase(
        api_endpoint="/api/virtuals/Test Virtual",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 