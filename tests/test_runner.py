import pytest
import sys
import os
import subprocess
import time
import requests

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def start_ledfx_server():
    """Start the LedFx server if it is not already running."""
    try:
        # Check if the server is already running
        response = requests.get('http://127.0.0.1:4619/api/schema')
        if response.status_code == 200:
            print("LedFx server is already running.")
            return True
    except requests.exceptions.ConnectionError:
        print("LedFx server is not running. Starting it now...")
        # Start the LedFx server
        subprocess.Popen([sys.executable, '-m', 'ledfx'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the server to start
        time.sleep(5)  # Adjust the sleep time as needed
        return True
    return False

def main():
    """Main function to run the test suite."""
    # Ensure the LedFx server is running
    if not start_ledfx_server():
        print("Failed to start the LedFx server. Exiting.")
        sys.exit(1)

    # Run the tests
    pytest.main(['--verbose', '--cov=ledfx', '--cov-report=term-missing', '--cov-report=html', 'tests/'])

if __name__ == "__main__":
    main() 