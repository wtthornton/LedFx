from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class PluginTestCase(TestCase):
    """Test case for plugin management testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Plugin management tests
plugin_tests = {
    "get_installed_plugins": PluginTestCase(
        api_endpoint="/api/plugins",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["plugins"],
        execution_order=1,
    ),
    "get_available_plugins": PluginTestCase(
        api_endpoint="/api/plugins/available",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["plugins"],
        execution_order=2,
    ),
    "install_plugin": PluginTestCase(
        api_endpoint="/api/plugins/install",
        method="POST",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
                "source": "github",
                "repository": "https://github.com/user/test_plugin",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "uninstall_plugin": PluginTestCase(
        api_endpoint="/api/plugins/uninstall",
        method="POST",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "update_plugin": PluginTestCase(
        api_endpoint="/api/plugins/update",
        method="POST",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
                "target_version": "1.1.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "enable_plugin": PluginTestCase(
        api_endpoint="/api/plugins/enable",
        method="POST",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=6,
    ),
    "disable_plugin": PluginTestCase(
        api_endpoint="/api/plugins/disable",
        method="POST",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=7,
    ),
    "get_plugin_config": PluginTestCase(
        api_endpoint="/api/plugins/config",
        method="GET",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["config"],
        execution_order=8,
    ),
    "update_plugin_config": PluginTestCase(
        api_endpoint="/api/plugins/config",
        method="PUT",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
            "config": {
                "setting1": "value1",
                "setting2": "value2",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=9,
    ),
    "get_plugin_dependencies": PluginTestCase(
        api_endpoint="/api/plugins/dependencies",
        method="GET",
        payload_to_send={
            "plugin": {
                "name": "test_plugin",
                "version": "1.0.0",
            },
        },
        expected_return_code=200,
        expected_response_keys=["dependencies"],
        execution_order=10,
    ),
} 