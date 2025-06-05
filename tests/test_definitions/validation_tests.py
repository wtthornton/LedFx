from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class ValidationTestCase(TestCase):
    """Test case for data validation testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Data validation tests
validation_tests = {
    "validate_device_config": ValidationTestCase(
        api_endpoint="/api/validation/device",
        method="POST",
        payload_to_send={
            "config": {
                "name": "Test Device",
                "type": "led",
                "ip_address": "192.168.1.100",
                "port": 8080,
                "protocol": "wled",
                "settings": {
                    "brightness": 100,
                    "color_mode": "rgb",
                    "effect_speed": 50,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=1,
    ),
    "validate_effect_config": ValidationTestCase(
        api_endpoint="/api/validation/effect",
        method="POST",
        payload_to_send={
            "config": {
                "name": "Test Effect",
                "type": "audio_reactive",
                "settings": {
                    "sensitivity": 0.8,
                    "smoothing": 0.5,
                    "color_palette": "rainbow",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=2,
    ),
    "validate_scene_config": ValidationTestCase(
        api_endpoint="/api/validation/scene",
        method="POST",
        payload_to_send={
            "config": {
                "name": "Test Scene",
                "devices": ["device1", "device2"],
                "effects": ["effect1", "effect2"],
                "transitions": {
                    "type": "fade",
                    "duration": 1000,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=3,
    ),
    "validate_preset_config": ValidationTestCase(
        api_endpoint="/api/validation/preset",
        method="POST",
        payload_to_send={
            "config": {
                "name": "Test Preset",
                "scenes": ["scene1", "scene2"],
                "settings": {
                    "auto_start": True,
                    "loop": True,
                    "randomize": False,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=4,
    ),
    "validate_audio_config": ValidationTestCase(
        api_endpoint="/api/validation/audio",
        method="POST",
        payload_to_send={
            "config": {
                "input_device": "default",
                "output_device": "default",
                "sample_rate": 44100,
                "channels": 2,
                "buffer_size": 1024,
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=5,
    ),
    "validate_network_config": ValidationTestCase(
        api_endpoint="/api/validation/network",
        method="POST",
        payload_to_send={
            "config": {
                "host": "0.0.0.0",
                "port": 8080,
                "ssl_enabled": False,
                "cors_enabled": True,
                "rate_limit": 100,
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=6,
    ),
    "validate_system_config": ValidationTestCase(
        api_endpoint="/api/validation/system",
        method="POST",
        payload_to_send={
            "config": {
                "log_level": "info",
                "log_file": "ledfx.log",
                "backup_enabled": True,
                "backup_interval": 3600,
                "performance_mode": "balanced",
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=7,
    ),
    "validate_ui_config": ValidationTestCase(
        api_endpoint="/api/validation/ui",
        method="POST",
        payload_to_send={
            "config": {
                "theme": "dark",
                "language": "en",
                "timezone": "UTC",
                "notifications": {
                    "enabled": True,
                    "sound": True,
                    "desktop": True,
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=8,
    ),
    "validate_api_config": ValidationTestCase(
        api_endpoint="/api/validation/api",
        method="POST",
        payload_to_send={
            "config": {
                "version": "1.0.0",
                "auth_required": True,
                "rate_limit": 100,
                "cors_enabled": True,
                "ssl_enabled": False,
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=9,
    ),
    "validate_websocket_config": ValidationTestCase(
        api_endpoint="/api/validation/websocket",
        method="POST",
        payload_to_send={
            "config": {
                "enabled": True,
                "port": 8081,
                "ssl_enabled": False,
                "heartbeat_interval": 30,
                "max_connections": 100,
            },
        },
        expected_return_code=200,
        expected_response_keys=["is_valid", "errors"],
        execution_order=10,
    ),
} 