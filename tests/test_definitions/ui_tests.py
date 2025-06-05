from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class UITestCase(TestCase):
    """Test case for UI component testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# UI component tests
ui_tests = {
    "get_ui_components": UITestCase(
        api_endpoint="/api/ui/components",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["components"],
        execution_order=1,
    ),
    "get_ui_layout": UITestCase(
        api_endpoint="/api/ui/layout",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["layout"],
        execution_order=2,
    ),
    "update_ui_layout": UITestCase(
        api_endpoint="/api/ui/layout",
        method="PUT",
        payload_to_send={
            "layout": {
                "type": "grid",
                "components": [
                    {
                        "id": "device_panel",
                        "type": "panel",
                        "position": {"x": 0, "y": 0},
                        "size": {"width": 300, "height": 400},
                    },
                    {
                        "id": "effect_panel",
                        "type": "panel",
                        "position": {"x": 310, "y": 0},
                        "size": {"width": 300, "height": 400},
                    },
                ],
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "get_ui_theme": UITestCase(
        api_endpoint="/api/ui/theme",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["theme"],
        execution_order=4,
    ),
    "update_ui_theme": UITestCase(
        api_endpoint="/api/ui/theme",
        method="PUT",
        payload_to_send={
            "theme": {
                "name": "dark",
                "colors": {
                    "primary": "#2196F3",
                    "secondary": "#FFC107",
                    "background": "#121212",
                    "surface": "#1E1E1E",
                    "error": "#CF6679",
                },
                "typography": {
                    "font_family": "Roboto",
                    "font_size": "14px",
                },
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "get_ui_preferences": UITestCase(
        api_endpoint="/api/ui/preferences",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["preferences"],
        execution_order=6,
    ),
    "update_ui_preferences": UITestCase(
        api_endpoint="/api/ui/preferences",
        method="PUT",
        payload_to_send={
            "preferences": {
                "show_tooltips": True,
                "enable_animations": True,
                "compact_mode": False,
                "language": "en",
                "timezone": "UTC",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
    "get_ui_notifications": UITestCase(
        api_endpoint="/api/ui/notifications",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["notifications"],
        execution_order=8,
    ),
    "update_ui_notifications": UITestCase(
        api_endpoint="/api/ui/notifications",
        method="PUT",
        payload_to_send={
            "notifications": {
                "enable_sound": True,
                "enable_desktop": True,
                "enable_email": False,
                "notification_types": [
                    "device_connected",
                    "device_disconnected",
                    "effect_started",
                    "effect_stopped",
                ],
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=9,
    ),
} 