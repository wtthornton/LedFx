from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class ConfigTestCase(TestCase):
    """Test case for configuration management testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Configuration management tests
config_tests = {
    "get_config": ConfigTestCase(
        api_endpoint="/api/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=1,
    ),
    "update_config": ConfigTestCase(
        api_endpoint="/api/config",
        method="PUT",
        payload_to_send={
            "config": {
                "devices": {
                    "default": {
                        "type": "wled",
                        "config": {
                            "ip_address": "192.168.1.100",
                            "port": 21324,
                            "pixel_count": 30,
                        },
                    },
                },
                "effects": {
                    "default": {
                        "type": "rainbow",
                        "config": {
                            "speed": 1.0,
                            "scale": 1.0,
                            "brightness": 1.0,
                        },
                    },
                },
                "scenes": {
                    "default": {
                        "devices": ["default"],
                        "effects": ["default"],
                    },
                },
                "presets": {
                    "default": {
                        "type": "scene",
                        "config": {
                            "scene": "default",
                            "settings": {
                                "brightness": 1.0,
                            },
                        },
                    },
                },
                "audio": {
                    "device": "default",
                    "config": {
                        "sample_rate": 44100,
                        "chunk_size": 1024,
                        "channels": 2,
                    },
                },
                "network": {
                    "interface": "eth0",
                    "config": {
                        "ip_address": "192.168.1.100",
                        "netmask": "255.255.255.0",
                        "gateway": "192.168.1.1",
                    },
                },
                "system": {
                    "log_level": "INFO",
                    "debug_mode": False,
                    "auto_start": True,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=2,
    ),
    "get_config_schema": ConfigTestCase(
        api_endpoint="/api/config/schema",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["schema"],
        execution_order=3,
    ),
    "validate_config": ConfigTestCase(
        api_endpoint="/api/config/validate",
        method="POST",
        payload_to_send={
            "config": {
                "devices": {
                    "default": {
                        "type": "wled",
                        "config": {
                            "ip_address": "192.168.1.100",
                            "port": 21324,
                            "pixel_count": 30,
                        },
                    },
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["valid"],
        execution_order=4,
    ),
    "reset_config": ConfigTestCase(
        api_endpoint="/api/config/reset",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
} 