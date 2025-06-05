from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class EventTestCase(TestCase):
    """Test case for event handling testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Event handling tests
event_tests = {
    "subscribe_to_events": EventTestCase(
        api_endpoint="/api/events/subscribe",
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
        execution_order=1,
    ),
    "unsubscribe_from_events": EventTestCase(
        api_endpoint="/api/events/unsubscribe",
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
        execution_order=2,
    ),
    "get_event_history": EventTestCase(
        api_endpoint="/api/events/history",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["history"],
        execution_order=3,
    ),
    "clear_event_history": EventTestCase(
        api_endpoint="/api/events/history/clear",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "get_event_handlers": EventTestCase(
        api_endpoint="/api/events/handlers",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["handlers"],
        execution_order=5,
    ),
    "register_event_handler": EventTestCase(
        api_endpoint="/api/events/handlers/register",
        method="POST",
        payload_to_send={
            "event": "device_connected",
            "handler": {
                "type": "function",
                "name": "handle_device_connected",
                "config": {
                    "action": "notify",
                    "target": "admin",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "unregister_event_handler": EventTestCase(
        api_endpoint="/api/events/handlers/unregister",
        method="POST",
        payload_to_send={
            "event": "device_connected",
            "handler": {
                "type": "function",
                "name": "handle_device_connected",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
} 