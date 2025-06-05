from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class NetworkTestCase(TestCase):
    """Test case for network management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Network management tests
network_tests = {
    "get_network_info": NetworkTestCase(
        api_endpoint="/api/network/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["network_info"],
        execution_order=1,
    ),
    "get_network_interfaces": NetworkTestCase(
        api_endpoint="/api/network/interfaces",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["interfaces"],
        execution_order=2,
    ),
    "get_network_config": NetworkTestCase(
        api_endpoint="/api/network/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=3,
    ),
    "update_network_config": NetworkTestCase(
        api_endpoint="/api/network/config",
        method="PUT",
        payload_to_send={
            "config": {
                "interface": "eth0",
                "ip_address": "192.168.1.100",
                "netmask": "255.255.255.0",
                "gateway": "192.168.1.1",
            },
        },
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=4,
    ),
    "test_network_connection": NetworkTestCase(
        api_endpoint="/api/network/test",
        method="POST",
        payload_to_send={
            "host": "8.8.8.8",
            "port": 53,
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
} 