from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class APIVersionTestCase(TestCase):
    """Test case for API versioning testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# API versioning tests
api_version_tests = {
    "get_api_versions": APIVersionTestCase(
        api_endpoint="/api/versions",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["versions"],
        execution_order=1,
    ),
    "get_api_version_info": APIVersionTestCase(
        api_endpoint="/api/versions/info",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["current_version", "supported_versions"],
        execution_order=2,
    ),
    "get_api_version_changes": APIVersionTestCase(
        api_endpoint="/api/versions/changes",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["changes"],
        execution_order=3,
    ),
    "get_api_version_deprecations": APIVersionTestCase(
        api_endpoint="/api/versions/deprecations",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["deprecations"],
        execution_order=4,
    ),
    "get_api_version_migration_guide": APIVersionTestCase(
        api_endpoint="/api/versions/migration",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["migration_guide"],
        execution_order=5,
    ),
    "get_api_version_compatibility": APIVersionTestCase(
        api_endpoint="/api/versions/compatibility",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["compatibility"],
        execution_order=6,
    ),
    "get_api_version_requirements": APIVersionTestCase(
        api_endpoint="/api/versions/requirements",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["requirements"],
        execution_order=7,
    ),
    "get_api_version_security": APIVersionTestCase(
        api_endpoint="/api/versions/security",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["security"],
        execution_order=8,
    ),
    "get_api_version_performance": APIVersionTestCase(
        api_endpoint="/api/versions/performance",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["performance"],
        execution_order=9,
    ),
    "get_api_version_documentation": APIVersionTestCase(
        api_endpoint="/api/versions/documentation",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["documentation"],
        execution_order=10,
    ),
} 