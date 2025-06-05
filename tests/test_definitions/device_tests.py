from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class DeviceTestCase(TestCase):
    """Test case for device management testing."""
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
    "get_devices": DeviceTestCase(
        api_endpoint="/api/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["devices"],
        expected_response_values=[
            {
                "devices": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "name", "type", "status", "config"],
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "name": {"type": "string", "minLength": 1},
                            "type": {"type": "string", "enum": ["wled", "falcon", "e131", "artnet"]},
                            "status": {"type": "string", "enum": ["connected", "disconnected", "error"]},
                            "config": {
                                "type": "object",
                                "required": ["ip_address", "port", "protocol"],
                                "properties": {
                                    "ip_address": {"type": "string", "format": "ipv4"},
                                    "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                                    "protocol": {"type": "string", "enum": ["udp", "tcp"]},
                                },
                            },
                        },
                    },
                }
            }
        ],
        execution_order=1,
    ),
    "add_device": DeviceTestCase(
        api_endpoint="/api/devices",
        method="POST",
        payload_to_send={
            "device": {
                "name": "Test Device",
                "type": "wled",
                "config": {
                    "ip_address": "192.168.1.100",
                    "port": 8080,
                    "protocol": "udp",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "device"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "device": {
                    "type": "object",
                    "required": ["id", "name", "type", "status", "config"],
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string", "minLength": 1},
                        "type": {"type": "string", "enum": ["wled", "falcon", "e131", "artnet"]},
                        "status": {"type": "string", "enum": ["connected", "disconnected", "error"]},
                        "config": {
                            "type": "object",
                            "required": ["ip_address", "port", "protocol"],
                            "properties": {
                                "ip_address": {"type": "string", "format": "ipv4"},
                                "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                                "protocol": {"type": "string", "enum": ["udp", "tcp"]},
                            },
                        },
                    },
                },
            }
        ],
        execution_order=2,
    ),
    "update_device": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}",
        method="PUT",
        payload_to_send={
            "device": {
                "name": "Updated Device",
                "config": {
                    "ip_address": "192.168.1.101",
                    "port": 8081,
                    "protocol": "tcp",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "device"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "device": {
                    "type": "object",
                    "required": ["id", "name", "type", "status", "config"],
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string", "minLength": 1},
                        "type": {"type": "string", "enum": ["wled", "falcon", "e131", "artnet"]},
                        "status": {"type": "string", "enum": ["connected", "disconnected", "error"]},
                        "config": {
                            "type": "object",
                            "required": ["ip_address", "port", "protocol"],
                            "properties": {
                                "ip_address": {"type": "string", "format": "ipv4"},
                                "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                                "protocol": {"type": "string", "enum": ["udp", "tcp"]},
                            },
                        },
                    },
                },
            }
        ],
        execution_order=3,
    ),
    "delete_device": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
            }
        ],
        execution_order=4,
    ),
    "get_device_status": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/status",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["status"],
        expected_response_values=[
            {
                "status": {
                    "type": "object",
                    "required": ["connected", "last_seen", "errors"],
                    "properties": {
                        "connected": {"type": "boolean"},
                        "last_seen": {"type": "string", "format": "date-time"},
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["code", "message", "timestamp"],
                                "properties": {
                                    "code": {"type": "string"},
                                    "message": {"type": "string"},
                                    "timestamp": {"type": "string", "format": "date-time"},
                                },
                            },
                        },
                    },
                }
            }
        ],
        execution_order=5,
    ),
    "get_device_config": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        expected_response_values=[
            {
                "config": {
                    "type": "object",
                    "required": ["ip_address", "port", "protocol", "settings"],
                    "properties": {
                        "ip_address": {"type": "string", "format": "ipv4"},
                        "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                        "protocol": {"type": "string", "enum": ["udp", "tcp"]},
                        "settings": {
                            "type": "object",
                            "required": ["brightness", "color_mode", "effect_speed"],
                            "properties": {
                                "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
                                "color_mode": {"type": "string", "enum": ["rgb", "rgbw", "rgbww"]},
                                "effect_speed": {"type": "integer", "minimum": 0, "maximum": 100},
                            },
                        },
                    },
                }
            }
        ],
        execution_order=6,
    ),
    "update_device_config": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/config",
        method="PUT",
        payload_to_send={
            "config": {
                "ip_address": "192.168.1.102",
                "port": 8082,
                "protocol": "udp",
                "settings": {
                    "brightness": 75,
                    "color_mode": "rgbw",
                    "effect_speed": 50,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "config"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "config": {
                    "type": "object",
                    "required": ["ip_address", "port", "protocol", "settings"],
                    "properties": {
                        "ip_address": {"type": "string", "format": "ipv4"},
                        "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                        "protocol": {"type": "string", "enum": ["udp", "tcp"]},
                        "settings": {
                            "type": "object",
                            "required": ["brightness", "color_mode", "effect_speed"],
                            "properties": {
                                "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
                                "color_mode": {"type": "string", "enum": ["rgb", "rgbw", "rgbww"]},
                                "effect_speed": {"type": "integer", "minimum": 0, "maximum": 100},
                            },
                        },
                    },
                },
            }
        ],
        execution_order=7,
    ),
    "get_device_effects": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/effects",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["effects"],
        expected_response_values=[
            {
                "effects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "name", "type", "config"],
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "name": {"type": "string", "minLength": 1},
                            "type": {"type": "string", "enum": ["audio_reactive", "static", "gradient"]},
                            "config": {
                                "type": "object",
                                "required": ["sensitivity", "smoothing", "color_palette"],
                                "properties": {
                                    "sensitivity": {"type": "number", "minimum": 0, "maximum": 1},
                                    "smoothing": {"type": "number", "minimum": 0, "maximum": 1},
                                    "color_palette": {"type": "string", "enum": ["rainbow", "fire", "ocean"]},
                                },
                            },
                        },
                    },
                }
            }
        ],
        execution_order=8,
    ),
    "add_device_effect": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/effects",
        method="POST",
        payload_to_send={
            "effect": {
                "name": "Test Effect",
                "type": "audio_reactive",
                "config": {
                    "sensitivity": 0.8,
                    "smoothing": 0.5,
                    "color_palette": "rainbow",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "effect"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "effect": {
                    "type": "object",
                    "required": ["id", "name", "type", "config"],
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string", "minLength": 1},
                        "type": {"type": "string", "enum": ["audio_reactive", "static", "gradient"]},
                        "config": {
                            "type": "object",
                            "required": ["sensitivity", "smoothing", "color_palette"],
                            "properties": {
                                "sensitivity": {"type": "number", "minimum": 0, "maximum": 1},
                                "smoothing": {"type": "number", "minimum": 0, "maximum": 1},
                                "color_palette": {"type": "string", "enum": ["rainbow", "fire", "ocean"]},
                            },
                        },
                    },
                },
            }
        ],
        execution_order=9,
    ),
    "update_device_effect": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/effects/{effect_id}",
        method="PUT",
        payload_to_send={
            "effect": {
                "name": "Updated Effect",
                "config": {
                    "sensitivity": 0.9,
                    "smoothing": 0.6,
                    "color_palette": "fire",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "effect"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "effect": {
                    "type": "object",
                    "required": ["id", "name", "type", "config"],
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string", "minLength": 1},
                        "type": {"type": "string", "enum": ["audio_reactive", "static", "gradient"]},
                        "config": {
                            "type": "object",
                            "required": ["sensitivity", "smoothing", "color_palette"],
                            "properties": {
                                "sensitivity": {"type": "number", "minimum": 0, "maximum": 1},
                                "smoothing": {"type": "number", "minimum": 0, "maximum": 1},
                                "color_palette": {"type": "string", "enum": ["rainbow", "fire", "ocean"]},
                            },
                        },
                    },
                },
            }
        ],
        execution_order=10,
    ),
    "delete_device_effect": DeviceTestCase(
        api_endpoint="/api/devices/{device_id}/effects/{effect_id}",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
            }
        ],
        execution_order=11,
    ),
} 