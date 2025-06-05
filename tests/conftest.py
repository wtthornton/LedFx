import subprocess
import time
import os
import sys
from pathlib import Path

import pytest

from tests.test_definitions.all_effects import get_ledfx_effects
from tests.test_definitions.audio_configs import get_ledfx_audio_configs
from tests.test_utilities.consts import BASE_PORT
from tests.test_utilities.test_utils import EnvironmentCleanup, TestCase

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Mock aubio module
sys.modules['aubio'] = __import__('tests.mock_aubio')

# Set up environment variables for testing
os.environ['LEDFX_TESTING'] = 'true'
os.environ['LEDFX_CONFIG_DIR'] = os.path.join(project_root, 'tests', 'config')
os.environ['LEDFX_DATA_DIR'] = os.path.join(project_root, 'tests', 'data')
os.environ['LEDFX_USER_DIR'] = os.path.join(project_root, 'tests', 'user')
os.environ['LEDFX_BACKUP_DIR'] = os.path.join(project_root, 'tests', 'backup')

# Create test directories if they do not exist
for directory in [os.environ['LEDFX_CONFIG_DIR'], os.environ['LEDFX_DATA_DIR'], os.environ['LEDFX_USER_DIR'], os.environ['LEDFX_BACKUP_DIR']]:
    os.makedirs(directory, exist_ok=True)

@pytest.fixture
def test_case():
    """Fixture to provide test case utilities."""
    from tests.test_utilities.test_utils import TestCase
    return TestCase()

@pytest.fixture
def test_directories():
    """Fixture to provide test directory paths."""
    return {
        'config': os.environ['LEDFX_CONFIG_DIR'],
        'data': os.environ['LEDFX_DATA_DIR'],
        'user': os.environ['LEDFX_USER_DIR'],
        'backup': os.environ['LEDFX_BACKUP_DIR'],
    }

def pytest_sessionstart(session):
    """
    Function to start LedFx as a subprocess and initialize necessary variables.
    It is called once at the start of the pytest session, before any tests are run.
    We use this function to start LedFx as a subprocess and initialize the all_effects variable.
    These are then exported as global variables so that they can be used by the tests.
    Args:
        session: The pytest session object.

    Returns:
        None
    """
    EnvironmentCleanup.cleanup_test_config_folder()
    # Start LedFx as a subprocess
    global ledfx
    try:
        ledfx = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "ledfx",
                "-p",
                f"{BASE_PORT}",
                "--offline",
                "-c",
                "debug_config",
                "-vv",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        pytest.fail(f"An error occurred while starting LedFx: {str(e)}")

    time.sleep(
        2
    )  # Wait for 2 seconds for the server to start and schema to be generated

    # Dynamic import of tests happens here
    # Needs to be done at session start so that the tests are available to pytest
    # This is a hack to get around the fact that pytest doesn't support dynamic imports
    global all_effects
    all_effects = get_ledfx_effects()
    global audio_configs
    audio_configs = get_ledfx_audio_configs()
    # To add another test group, add it here, and then in test_apis.py


def pytest_sessionfinish(session, exitstatus):
    """
    Function to terminate the ledfx subprocess.
    It is called once at the end of the pytest session, after all tests are run.
    Args:
        session: The pytest session object.
        exitstatus: The exit status of the pytest session.

    Returns:
        None
    """
    # send LedFx a shutdown signal
    try:
        EnvironmentCleanup.shutdown_ledfx()
    except Exception as e:
        pytest.fail(f"An error occurred while shutting down LedFx: {str(e)}")
    # Wait for LedFx to terminate
    while ledfx.poll() is None:
        time.sleep(0.5)
