from dataclasses import dataclass
from typing import Dict, List, Optional

from tests.test_utilities.test_utils import TestCase


@dataclass
class BackupTestCase(TestCase):
    """Test case for backup and restore testing."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


# Backup and restore tests
backup_tests = {
    "create_backup": BackupTestCase(
        api_endpoint="/api/backup",
        method="POST",
        payload_to_send={
            "action": "create",
            "config": {
                "include_devices": True,
                "include_effects": True,
                "include_scenes": True,
                "include_presets": True,
                "include_audio": True,
                "include_network": True,
                "include_system": True,
            },
        },
        expected_return_code=200,
        expected_response_keys=["backup"],
        execution_order=1,
    ),
    "list_backups": BackupTestCase(
        api_endpoint="/api/backup",
        method="GET",
        expected_return_code=200,
        expected_response_keys=["backups"],
        execution_order=2,
    ),
    "get_backup_info": BackupTestCase(
        api_endpoint="/api/backup/info",
        method="GET",
        payload_to_send={
            "backup": "latest",
        },
        expected_return_code=200,
        expected_response_keys=["info"],
        execution_order=3,
    ),
    "restore_backup": BackupTestCase(
        api_endpoint="/api/backup/restore",
        method="POST",
        payload_to_send={
            "backup": "latest",
            "config": {
                "include_devices": True,
                "include_effects": True,
                "include_scenes": True,
                "include_presets": True,
                "include_audio": True,
                "include_network": True,
                "include_system": True,
            },
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=4,
    ),
    "delete_backup": BackupTestCase(
        api_endpoint="/api/backup",
        method="DELETE",
        payload_to_send={
            "backup": "latest",
        },
        expected_return_code=200,
        expected_response_keys=["status"],
        execution_order=5,
    ),
} 