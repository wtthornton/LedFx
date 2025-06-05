from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class I18nTestCase(TestCase):
    """Test case for internationalization testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Internationalization tests
i18n_tests = {
    "get_available_languages": I18nTestCase(
        api_endpoint="/api/i18n/languages",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["languages"],
        execution_order=1,
    ),
    "get_current_language": I18nTestCase(
        api_endpoint="/api/i18n/language",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["language"],
        execution_order=2,
    ),
    "set_language": I18nTestCase(
        api_endpoint="/api/i18n/language",
        method="PUT",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=3,
    ),
    "get_translations": I18nTestCase(
        api_endpoint="/api/i18n/translations",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["translations"],
        execution_order=4,
    ),
    "update_translations": I18nTestCase(
        api_endpoint="/api/i18n/translations",
        method="PUT",
        payload_to_send={
            "language": "en",
            "translations": {
                "key1": "value1",
                "key2": "value2",
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
    "get_date_formats": I18nTestCase(
        api_endpoint="/api/i18n/date_formats",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["formats"],
        execution_order=6,
    ),
    "get_time_formats": I18nTestCase(
        api_endpoint="/api/i18n/time_formats",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["formats"],
        execution_order=7,
    ),
    "get_number_formats": I18nTestCase(
        api_endpoint="/api/i18n/number_formats",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["formats"],
        execution_order=8,
    ),
    "get_currency_formats": I18nTestCase(
        api_endpoint="/api/i18n/currency_formats",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["formats"],
        execution_order=9,
    ),
    "get_measurement_formats": I18nTestCase(
        api_endpoint="/api/i18n/measurement_formats",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["formats"],
        execution_order=10,
    ),
    "get_text_direction": I18nTestCase(
        api_endpoint="/api/i18n/text_direction",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["direction"],
        execution_order=11,
    ),
    "get_calendar_system": I18nTestCase(
        api_endpoint="/api/i18n/calendar",
        method="GET",
        payload_to_send={
            "language": "en",
        },
        expected_return_code=200,
        expected_response_keys=["calendar"],
        execution_order=12,
    ),
    "get_timezone": I18nTestCase(
        api_endpoint="/api/i18n/timezone",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["timezone"],
        execution_order=13,
    ),
    "set_timezone": I18nTestCase(
        api_endpoint="/api/i18n/timezone",
        method="PUT",
        payload_to_send={
            "timezone": "UTC",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=14,
    ),
    "get_region": I18nTestCase(
        api_endpoint="/api/i18n/region",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["region"],
        execution_order=15,
    ),
    "set_region": I18nTestCase(
        api_endpoint="/api/i18n/region",
        method="PUT",
        payload_to_send={
            "region": "US",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=16,
    ),
} 