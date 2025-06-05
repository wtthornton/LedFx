import os
import shutil
import sys
import time
from dataclasses import dataclass
from typing import Any, Literal, Optional, Union, Dict, List
from pathlib import Path

import numpy as np
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tests.test_utilities.consts import SERVER_PATH


@dataclass
class TestCase:
    """Base test case class for all test cases."""
    api_endpoint: str
    method: str
    payload_to_send: Optional[Dict] = None
    expected_return_code: int = 200
    expected_response_keys: Optional[List[str]] = None
    expected_response_values: Optional[List[Dict]] = None
    sleep_after_test: Optional[float] = None
    execution_order: int = 0


APITestCase = TestCase


class HTTPSession:
    def __init__(
        self,
        retries=5,
        backoff_factor=0.25,
        status_forcelist=(500, 502, 504),
        allowed_methods=frozenset(
            ["HEAD", "TRACE", "GET", "PUT", "POST", "OPTIONS", "DELETE"]
        ),
    ):
        """
        Initialize the RetrySession object.

        Args:
            retries (int): The maximum number of retries for a request. Default is 5.
            backoff_factor (float): The backoff factor between retries. Default is 0.25.
            status_forcelist (tuple): The HTTP status codes that trigger a retry. Default is (500, 502, 504).
            allowed_methods (frozenset): The set of allowed HTTP methods. Default is {"HEAD", "TRACE", "GET", "PUT", "POST", "OPTIONS", "DELETE"}.
        """
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.allowed_methods = allowed_methods
        self.session = self.requests_retry_session()

    def requests_retry_session(self):
        """
        Creates a session object with retry functionality for making HTTP requests.

        Returns:
            requests.Session: A session object with retry functionality.
        """
        session = requests.Session()
        retry = Retry(
            total=None,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=self.allowed_methods,
            raise_on_status=False,
            other=self.retries,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def send_test_api_request(
        self, url, method, payload: Optional[Union[str, dict]] = None
    ):
        """
        Sends a test API request to the specified URL using the specified HTTP method.

        Args:
            url (str): The URL to send the request to.
            method (str): The HTTP method to use for the request (GET, POST, PUT, DELETE).
            payload (Optional[Union[str, dict]], optional): The payload to include in the request. Defaults to None.

        Returns:
            requests.Response: The response object containing the server's response to the request.

        Raises:
            ValueError: If an invalid HTTP method is provided.

        """
        headers = {"Content-Type": "application/json"}
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(
                    url, json=payload, headers=headers
                )
            elif method == "PUT":
                response = self.session.put(url, json=payload, headers=headers)
            elif method == "DELETE":
                response = self.session.delete(
                    url, json=payload, headers=headers
                )
            else:
                raise ValueError(f"Invalid method: {method}")
        except Exception as e:
            pytest.fail(
                f"An error occurred while sending the API request: {str(e)}"
            )
        return response


class EnvironmentCleanup:
    """Utility class for cleaning up test environment."""

    def __init__(self, test_directories: Dict[str, str]):
        """Initialize with test directory paths."""
        self.test_directories = test_directories

    def cleanup(self):
        """Clean up test directories."""
        for directory in self.test_directories.values():
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory)

    def setup(self):
        """Set up test directories."""
        for directory in self.test_directories.values():
            os.makedirs(directory, exist_ok=True)

    def __enter__(self):
        """Context manager entry."""
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

    @staticmethod
    def shutdown_ledfx():
        """
        Shuts down the LedFx server by sending a POST request to the power endpoint
        and waits for the server to stop responding.

        Returns:
            None
        """
        _ = requests.post(f"http://{SERVER_PATH}/api/power", json={})
        while True:
            try:
                response = requests.get(
                    f"http://{SERVER_PATH}/api/info", timeout=1
                )
                if response.status_code != 200:
                    break
                time.sleep(0.5)
            except requests.exceptions.ConnectionError:
                break
        time.sleep(1)

    @staticmethod
    def cleanup_test_config_folder():
        """
        Cleans up the test configuration folder by removing it if it exists.

        This function checks if the 'debug_config' folder exists and attempts to remove it.
        If the folder cannot be removed, it waits for a short period of time and retries.
        The function will make up to 10 attempts before giving up.

        The delay -> retry is used as LedFx can take a bit of time to shut down and release the

        Raises:
            Any exception that occurs during the removal of the folder.

        """
        current_dir = os.getcwd()
        ci_test_dir = os.path.join(current_dir, "debug_config")

        # If the directory doesn't exist, return immediately
        if not os.path.exists(ci_test_dir):
            return

        for idx in range(10):
            try:
                shutil.rmtree(ci_test_dir)
                break
            except Exception as e:
                time.sleep(idx / 10)
        else:
            pytest.fail("Unable to remove the test config folder.")

    @staticmethod
    def ledfx_is_alive():
        """
        Checks to see if LedFx is running by sending a GET request to the schema endpoint.

        Returns:
            bool: True if LedFx is running, False otherwise.
        """
        try:
            response = requests.get(
                f"http://{SERVER_PATH}/api/info", timeout=1
            )
            if response.status_code == 200:
                # LedFx has returned a response, so it is running, but likely still hydrating the schema
                # We will wait until it is fully hydrated
                start_time = time.time()
                while True:
                    old_schema = requests.get(
                        f"http://{SERVER_PATH}/api/schema", timeout=1
                    )
                    time.sleep(0.1)
                    new_schema = requests.get(
                        f"http://{SERVER_PATH}/api/schema", timeout=1
                    )
                    if old_schema.json() == new_schema.json():
                        break
                    if time.time() - start_time > 5:
                        return False
                time.sleep(2)
                return True
        except requests.exceptions.ConnectionError:
            pass
        return False


class SystemInfo:
    @staticmethod
    def calc_available_fps():
        """
        Calculate the available frames per second (fps) based on the system's clock resolution.
        Note: This comes from the ledfx/utils.py file

        Returns:
            dict: A dictionary where the keys represent the fps and the values represent the corresponding tick value.
        """
        if (
            sys.version_info[0] == 3 and sys.version_info[1] >= 11
        ) or sys.version_info[0] >= 4:
            clock_source = "perf_counter"
        else:
            clock_source = "monotonic"
        sleep_res = time.get_clock_info(clock_source).resolution
        if sleep_res < 0.001:
            mult = int(0.001 / sleep_res)
        else:
            mult = 1
        max_fps_target = 126
        min_fps_target = 10
        max_fps_ticks = np.ceil(
            (1 / max_fps_target) / (sleep_res * mult)
        ).astype(int)
        min_fps_ticks = np.ceil(
            (1 / min_fps_target) / (sleep_res * mult)
        ).astype(int)
        tick_range = reversed(range(max_fps_ticks, min_fps_ticks))
        return {int(1 / (sleep_res * mult * i)): i * mult for i in tick_range}

    @staticmethod
    def default_fps():
        available_fps = SystemInfo.calc_available_fps()
        default_fps = next(
            (f for f in available_fps if f >= 60), list(available_fps)[-1]
        )
        return default_fps
