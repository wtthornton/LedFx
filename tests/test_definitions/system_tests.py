from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class SystemTestCase(TestCase):
    """Test case for system management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# System management tests
system_tests = {
    "get_system_info": SystemTestCase(
        api_endpoint="/api/system/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["system_info"],
        execution_order=1,
    ),
    "get_system_config": SystemTestCase(
        api_endpoint="/api/system/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=2,
    ),
    "update_system_config": SystemTestCase(
        api_endpoint="/api/system/config",
        method="PUT",
        payload_to_send={
            "config": {
                "log_level": "INFO",
                "debug_mode": False,
                "auto_start": True,
            },
        },
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=3,
    ),
    "get_system_logs": SystemTestCase(
        api_endpoint="/api/system/logs",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["logs"],
        execution_order=4,
    ),
    "clear_system_logs": SystemTestCase(
        api_endpoint="/api/system/logs/clear",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "restart_system": SystemTestCase(
        api_endpoint="/api/system/restart",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "shutdown_system": SystemTestCase(
        api_endpoint="/api/system/shutdown",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
} 