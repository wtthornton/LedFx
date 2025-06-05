from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class LoggingTestCase(TestCase):
    """Test case for logging testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Logging tests
logging_tests = {
    "get_logs": LoggingTestCase(
        api_endpoint="/api/logs",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["logs"],
        execution_order=1,
    ),
    "get_log_level": LoggingTestCase(
        api_endpoint="/api/logs/level",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["level"],
        execution_order=2,
    ),
    "set_log_level": LoggingTestCase(
        api_endpoint="/api/logs/level",
        method="PUT",
        payload_to_send={
            "level": "DEBUG",
        },
        expected_return_code=200,
        expected_response_keys=["level"],
        execution_order=3,
    ),
    "get_log_file": LoggingTestCase(
        api_endpoint="/api/logs/file",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["file"],
        execution_order=4,
    ),
    "set_log_file": LoggingTestCase(
        api_endpoint="/api/logs/file",
        method="PUT",
        payload_to_send={
            "file": "test.log",
        },
        expected_return_code=200,
        expected_response_keys=["file"],
        execution_order=5,
    ),
    "get_log_format": LoggingTestCase(
        api_endpoint="/api/logs/format",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["format"],
        execution_order=6,
    ),
    "set_log_format": LoggingTestCase(
        api_endpoint="/api/logs/format",
        method="PUT",
        payload_to_send={
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        expected_return_code=200,
        expected_response_keys=["format"],
        execution_order=7,
    ),
    "clear_logs": LoggingTestCase(
        api_endpoint="/api/logs/clear",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=8,
    ),
} 