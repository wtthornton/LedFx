from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class AnalyticsTestCase(TestCase):
    """Test case for analytics testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Analytics tests
analytics_tests = {
    "get_usage_statistics": AnalyticsTestCase(
        api_endpoint="/api/analytics/usage",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["statistics"],
        execution_order=1,
    ),
    "get_performance_metrics": AnalyticsTestCase(
        api_endpoint="/api/analytics/performance",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=2,
    ),
    "get_user_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/users",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=3,
    ),
    "get_device_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=4,
    ),
    "get_effect_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/effects",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=5,
    ),
    "get_scene_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/scenes",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=6,
    ),
    "get_preset_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/presets",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=7,
    ),
    "get_audio_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/audio",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=8,
    ),
    "get_network_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/network",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=9,
    ),
    "get_system_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/system",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=10,
    ),
    "get_error_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/errors",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=11,
    ),
    "get_security_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/security",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=12,
    ),
    "get_plugin_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/plugins",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=13,
    ),
    "get_api_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/api",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=14,
    ),
    "get_websocket_analytics": AnalyticsTestCase(
        api_endpoint="/api/analytics/websocket",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["analytics"],
        execution_order=15,
    ),
} 