from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class WebSocketTestCase(TestCase):
    """Test case for WebSocket testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# WebSocket tests
websocket_tests = {
    "connect_websocket": WebSocketTestCase(
        api_endpoint="/ws",
        method="GET",
        expected_return_code=101,
        expected_response_keys=["status"],
        execution_order=1,
    ),
    "send_websocket_message": WebSocketTestCase(
        api_endpoint="/ws",
        method="POST",
        payload_to_send={
            "type": "message",
            "data": {
                "action": "test",
                "payload": {
                    "test": "data",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=2,
    ),
    "subscribe_to_websocket_events": WebSocketTestCase(
        api_endpoint="/ws/events",
        method="POST",
        payload_to_send={
            "events": [
                "device_connected",
                "device_disconnected",
                "effect_started",
                "effect_stopped",
                "scene_activated",
                "scene_deactivated",
                "preset_applied",
                "audio_started",
                "audio_stopped",
                "system_started",
                "system_stopped",
            ],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "unsubscribe_from_websocket_events": WebSocketTestCase(
        api_endpoint="/ws/events",
        method="DELETE",
        payload_to_send={
            "events": [
                "device_connected",
                "device_disconnected",
                "effect_started",
                "effect_stopped",
                "scene_activated",
                "scene_deactivated",
                "preset_applied",
                "audio_started",
                "audio_stopped",
                "system_started",
                "system_stopped",
            ],
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "get_websocket_connections": WebSocketTestCase(
        api_endpoint="/ws/connections",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["connections"],
        execution_order=5,
    ),
    "close_websocket_connection": WebSocketTestCase(
        api_endpoint="/ws/close",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 