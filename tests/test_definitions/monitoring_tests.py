from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class MonitoringTestCase(TestCase):
    """Test case for monitoring testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Monitoring tests
monitoring_tests = {
    "get_system_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/system",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=1,
    ),
    "get_device_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/devices",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=2,
    ),
    "get_effect_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/effects",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=3,
    ),
    "get_scene_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/scenes",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=4,
    ),
    "get_audio_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/audio",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=5,
    ),
    "get_network_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/network",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=6,
    ),
    "get_performance_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/performance",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=7,
    ),
    "get_resource_metrics": MonitoringTestCase(
        api_endpoint="/api/monitoring/resources",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["metrics"],
        execution_order=8,
    ),
    "get_health_status": MonitoringTestCase(
        api_endpoint="/api/monitoring/health",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=9,
    ),
    "get_alerts": MonitoringTestCase(
        api_endpoint="/api/monitoring/alerts",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["alerts"],
        execution_order=10,
    ),
    "set_alert_threshold": MonitoringTestCase(
        api_endpoint="/api/monitoring/alerts/threshold",
        method="PUT",
        payload_to_send={
            "metric": "cpu_usage",
            "threshold": 80.0,
            "operator": ">",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=11,
    ),
    "get_alert_history": MonitoringTestCase(
        api_endpoint="/api/monitoring/alerts/history",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["history"],
        execution_order=12,
    ),
} 