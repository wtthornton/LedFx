from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class UtilsTestCase(TestCase):
    """Test case for utility functions."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Utility function tests
utils_tests = {
    "get_logs": UtilsTestCase(
        api_endpoint="/api/logs",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["logs"],
        execution_order=1,
    ),
    "get_system_info": UtilsTestCase(
        api_endpoint="/api/system/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["system_info"],
        execution_order=2,
    ),
    "get_network_info": UtilsTestCase(
        api_endpoint="/api/network/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["network_info"],
        execution_order=3,
    ),
    "get_audio_analysis": UtilsTestCase(
        api_endpoint="/api/audio/analysis",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analysis"],
        execution_order=4,
    ),
    "get_audio_visualization": UtilsTestCase(
        api_endpoint="/api/audio/visualization",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["visualization"],
        execution_order=5,
    ),
} 