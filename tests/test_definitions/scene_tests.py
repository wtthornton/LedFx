from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class SceneTestCase(TestCase):
    """Test case for scene management."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Scene management tests
scene_tests = {
    "create_scene": SceneTestCase(
        api_endpoint="/api/scenes",
        method="POST",
        payload_to_send={
            "name": "Test Scene",
            "config": {
                "devices": ["Test Device"],
                "effects": ["rainbow"],
            },
        },
        expected_return_code=200,
        expected_response_keys=["scene"],
        execution_order=1,
    ),
    "update_scene": SceneTestCase(
        api_endpoint="/api/scenes/Test Scene",
        method="PUT",
        payload_to_send={
            "config": {
                "devices": ["Test Device"],
                "effects": ["rainbow", "energy"],
            },
        },
        expected_return_code=200,
        expected_response_keys=["scene"],
        execution_order=2,
    ),
    "get_scene": SceneTestCase(
        api_endpoint="/api/scenes/Test Scene",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["scene"],
        execution_order=3,
    ),
    "activate_scene": SceneTestCase(
        api_endpoint="/api/scenes/Test Scene/activate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "deactivate_scene": SceneTestCase(
        api_endpoint="/api/scenes/Test Scene/deactivate",
        method="POST",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "delete_scene": SceneTestCase(
        api_endpoint="/api/scenes/Test Scene",
        method="DELETE",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
} 