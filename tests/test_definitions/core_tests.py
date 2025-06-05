from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class CoreTestCase(TestCase):
    """Test case for core functionality testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Core functionality tests
core_tests = {
    "get_system_info": CoreTestCase(
        api_endpoint="/api/system/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["version", "platform", "python_version", "dependencies"],
        expected_response_values=[
            {
                "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "platform": {"type": "string", "enum": ["windows", "linux", "darwin"]},
                "python_version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "dependencies": {"type": "object", "required": ["numpy", "scipy", "sounddevice"]},
            }
        ],
        execution_order=1,
    ),
    "get_system_status": CoreTestCase(
        api_endpoint="/api/system/status",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["status", "uptime", "memory_usage", "cpu_usage"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["running", "stopped", "error"]},
                "uptime": {"type": "number", "minimum": 0},
                "memory_usage": {"type": "object", "required": ["total", "used", "free"]},
                "cpu_usage": {"type": "number", "minimum": 0, "maximum": 100},
            }
        ],
        execution_order=2,
    ),
    "get_system_config": CoreTestCase(
        api_endpoint="/api/system/config",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["config"],
        expected_response_values=[
            {
                "config": {
                    "type": "object",
                    "required": [
                        "host",
                        "port",
                        "debug",
                        "log_level",
                        "data_dir",
                        "user_dir",
                        "backup_dir",
                    ],
                    "properties": {
                        "host": {"type": "string", "pattern": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"},
                        "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                        "debug": {"type": "boolean"},
                        "log_level": {"type": "string", "enum": ["debug", "info", "warning", "error"]},
                        "data_dir": {"type": "string", "pattern": r"^[a-zA-Z]:\\.*|^/.*"},
                        "user_dir": {"type": "string", "pattern": r"^[a-zA-Z]:\\.*|^/.*"},
                        "backup_dir": {"type": "string", "pattern": r"^[a-zA-Z]:\\.*|^/.*"},
                    },
                }
            }
        ],
        execution_order=3,
    ),
    "update_system_config": CoreTestCase(
        api_endpoint="/api/system/config",
        method="PUT",
        payload_to_send={
            "config": {
                "host": "127.0.0.1",
                "port": 8080,
                "debug": False,
                "log_level": "info",
                "data_dir": "C:/LedFx/data",
                "user_dir": "C:/LedFx/user",
                "backup_dir": "C:/LedFx/backup",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status", "config"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
                "config": {
                    "type": "object",
                    "required": [
                        "host",
                        "port",
                        "debug",
                        "log_level",
                        "data_dir",
                        "user_dir",
                        "backup_dir",
                    ],
                },
            }
        ],
        execution_order=4,
    ),
    "get_system_logs": CoreTestCase(
        api_endpoint="/api/system/logs",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["logs"],
        expected_response_values=[
            {
                "logs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["timestamp", "level", "message"],
                        "properties": {
                            "timestamp": {"type": "string", "format": "date-time"},
                            "level": {"type": "string", "enum": ["debug", "info", "warning", "error"]},
                            "message": {"type": "string"},
                        },
                    },
                }
            }
        ],
        execution_order=5,
    ),
    "clear_system_logs": CoreTestCase(
        api_endpoint="/api/system/logs",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
            }
        ],
        execution_order=6,
    ),
    "get_system_metrics": CoreTestCase(
        api_endpoint="/api/system/metrics",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        expected_response_values=[
            {
                "metrics": {
                    "type": "object",
                    "required": ["cpu", "memory", "disk", "network"],
                    "properties": {
                        "cpu": {
                            "type": "object",
                            "required": ["usage", "temperature"],
                            "properties": {
                                "usage": {"type": "number", "minimum": 0, "maximum": 100},
                                "temperature": {"type": "number", "minimum": 0},
                            },
                        },
                        "memory": {
                            "type": "object",
                            "required": ["total", "used", "free"],
                            "properties": {
                                "total": {"type": "number", "minimum": 0},
                                "used": {"type": "number", "minimum": 0},
                                "free": {"type": "number", "minimum": 0},
                            },
                        },
                        "disk": {
                            "type": "object",
                            "required": ["total", "used", "free"],
                            "properties": {
                                "total": {"type": "number", "minimum": 0},
                                "used": {"type": "number", "minimum": 0},
                                "free": {"type": "number", "minimum": 0},
                            },
                        },
                        "network": {
                            "type": "object",
                            "required": ["bytes_sent", "bytes_received"],
                            "properties": {
                                "bytes_sent": {"type": "number", "minimum": 0},
                                "bytes_received": {"type": "number", "minimum": 0},
                            },
                        },
                    },
                }
            }
        ],
        execution_order=7,
    ),
    "get_system_alerts": CoreTestCase(
        api_endpoint="/api/system/alerts",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["alerts"],
        expected_response_values=[
            {
                "alerts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "level", "message", "timestamp"],
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "level": {"type": "string", "enum": ["info", "warning", "error", "critical"]},
                            "message": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"},
                        },
                    },
                }
            }
        ],
        execution_order=8,
    ),
    "clear_system_alerts": CoreTestCase(
        api_endpoint="/api/system/alerts",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        expected_response_values=[
            {
                "status": {"type": "string", "enum": ["success", "error"]},
            }
        ],
        execution_order=9,
    ),
    "get_system_health": CoreTestCase(
        api_endpoint="/api/system/health",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["health"],
        expected_response_values=[
            {
                "health": {
                    "type": "object",
                    "required": ["status", "components"],
                    "properties": {
                        "status": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                        "components": {
                            "type": "object",
                            "required": ["api", "database", "websocket", "audio"],
                            "properties": {
                                "api": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                                "database": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                                "websocket": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                                "audio": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                            },
                        },
                    },
                }
            }
        ],
        execution_order=10,
    ),
} 