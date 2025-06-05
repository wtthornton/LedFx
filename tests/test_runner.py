import pytest
import sys
from pathlib import Path

def main():
    """Run the test suite."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Add the project root to the Python path
    sys.path.insert(0, str(project_root))

    # Run the tests
    args = [
        "--verbose",
        "--cov=ledfx",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/",
    ]

    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(main()) 