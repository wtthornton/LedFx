from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class SecurityTestCase(TestCase):
    """Test case for security testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 401
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Security tests
security_tests = {
    "unauthorized_access": SecurityTestCase(
        api_endpoint="/api/devices",
        method="GET",
        expected_return_code=401,
        expected_response_keys=["error"],
        execution_order=1,
    ),
    "invalid_token": SecurityTestCase(
        api_endpoint="/api/devices",
        method="GET",
        payload_to_send={
            "token": "invalid_token",
        },
        expected_return_code=401,
        expected_response_keys=["error"],
        execution_order=2,
    ),
    "expired_token": SecurityTestCase(
        api_endpoint="/api/devices",
        method="GET",
        payload_to_send={
            "token": "expired_token",
        },
        expected_return_code=401,
        expected_response_keys=["error"],
        execution_order=3,
    ),
    "malicious_payload": SecurityTestCase(
        api_endpoint="/api/devices",
        method="POST",
        payload_to_send={
            "name": "<script>alert('xss')</script>",
            "type": "wled",
            "config": {
                "ip_address": "192.168.1.100; rm -rf /",
                "port": 21324,
                "pixel_count": 30,
            },
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=4,
    ),
    "sql_injection": SecurityTestCase(
        api_endpoint="/api/devices",
        method="GET",
        payload_to_send={
            "name": "'; DROP TABLE devices; --",
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=5,
    ),
    "path_traversal": SecurityTestCase(
        api_endpoint="/api/config",
        method="GET",
        payload_to_send={
            "path": "../../../etc/passwd",
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=6,
    ),
    "command_injection": SecurityTestCase(
        api_endpoint="/api/system/command",
        method="POST",
        payload_to_send={
            "command": "ls; rm -rf /",
        },
        expected_return_code=400,
        expected_response_keys=["error"],
        execution_order=7,
    ),
} 