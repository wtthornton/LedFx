# -*- coding: utf-8 -*-
"""
Enhanced dependency checker for LedFx.
Checks for all required dependencies, installs any missing ones, and provides clear, color-coded output.
"""

import importlib
import subprocess
import sys
from typing import Dict, Optional, Tuple

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[90m'

def color_text(text, color):
    return f"{color}{text}{Colors.ENDC}"

REQUIRED_DEPENDENCIES = {
    "numpy": "numpy",
    "aiohttp": "aiohttp",
    "aiohttp-cors": "aiohttp_cors",
    "aubio": "aubio",
    "cffi": "cffi",
    "wheel": "wheel",
    "certifi": "certifi",
    "multidict": "multidict",
    "openrgb-python": "openrgb",
    "paho-mqtt": "paho.mqtt",
    "psutil": "psutil",
    "pyserial": "serial",
    "pystray": "pystray",
    "python-rtmidi": "rtmidi",
    "requests": "requests",
    "sacn": "sacn",
    "sentry-sdk": "sentry_sdk",
    "sounddevice": "sounddevice",
    "samplerate": "samplerate",
    "icmplib": "icmplib",
    "voluptuous": "voluptuous",
    "zeroconf": "zeroconf",
    "pillow": "PIL",
    "flux-led": "flux_led",
    "python-osc": "pythonosc",
    "pybase64": "pybase64",
    "mss": "mss",
    "setuptools": "setuptools",
    "python-dotenv": "dotenv",
    "vnoise": "vnoise",
}

OPTIONAL_DEPENDENCIES = {
    "uvloop": "uvloop",
    "rpi-ws281x": "rpi_ws281x",
    "stupidartnet": "stupidartnet",
}

def check_dependency(package_name: str, import_name: str) -> Tuple[bool, Optional[str]]:
    try:
        importlib.import_module(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def install_dependency(package_name: str) -> Tuple[bool, Optional[str]]:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install {package_name}: {str(e)}"

def print_section(title: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{Colors.GREY}{'-' * 60}{Colors.ENDC}")

def check_and_install_dependencies() -> Dict[str, Tuple[bool, Optional[str]]]:
    results = {}
    print_section("Checking Required Dependencies")
    for package_name, import_name in REQUIRED_DEPENDENCIES.items():
        print(f"{Colors.BOLD}Checking {package_name}...{Colors.ENDC}", end=" ")
        is_installed, error = check_dependency(package_name, import_name)
        if is_installed:
            print(color_text("✓ Installed", Colors.OKGREEN))
            results[package_name] = (True, None)
        else:
            print(color_text("✗ Not installed", Colors.FAIL))
            print(color_text(f"  Error: {error}", Colors.WARNING))
            print(color_text(f"  Attempting to install {package_name}...", Colors.OKBLUE))
            success, install_error = install_dependency(package_name)
            if success:
                print(color_text(f"  ✓ Successfully installed {package_name}", Colors.OKGREEN))
                results[package_name] = (True, None)
            else:
                print(color_text(f"  ✗ Failed to install {package_name}", Colors.FAIL))
                print(color_text(f"    Error: {install_error}", Colors.FAIL))
                results[package_name] = (False, install_error)
    print_section("Checking Optional Dependencies")
    for package_name, import_name in OPTIONAL_DEPENDENCIES.items():
        print(f"{Colors.BOLD}Checking {package_name}...{Colors.ENDC}", end=" ")
        is_installed, error = check_dependency(package_name, import_name)
        if is_installed:
            print(color_text("✓ Installed", Colors.OKGREEN))
            results[package_name] = (True, None)
        else:
            print(color_text("! Not installed (optional)", Colors.WARNING))
            print(color_text(f"  Note: {error}", Colors.GREY))
            results[package_name] = (False, error)
    return results

def print_summary(results: Dict[str, Tuple[bool, Optional[str]]]):
    print_section("Dependency Check Summary")
    print(f"{Colors.BOLD}{'Dependency':<25} {'Status':<12} {'Details'}{Colors.ENDC}")
    print(f"{Colors.GREY}{'-' * 60}{Colors.ENDC}")
    required_failed = False
    for package_name, (success, error) in results.items():
        if package_name in REQUIRED_DEPENDENCIES:
            if success:
                status = color_text("OK", Colors.OKGREEN)
                details = ""
            else:
                status = color_text("FAILED", Colors.FAIL)
                details = error or ""
                required_failed = True
            print(f"{package_name:<25} {status:<12} {details}")
    print(f"{Colors.GREY}{'-' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Optional dependencies not installed:{Colors.ENDC}")
    for package_name, (success, error) in results.items():
        if package_name in OPTIONAL_DEPENDENCIES and not success:
            print(f"{color_text(package_name, Colors.WARNING)}: {color_text(error or 'Not installed', Colors.GREY)}")
    if required_failed:
        print(color_text("\nSome required dependencies failed to install.", Colors.FAIL))
        print(color_text("Please check the errors above and try installing them manually.", Colors.WARNING))
        sys.exit(1)
    else:
        print(color_text("\nAll required dependencies are installed!", Colors.OKGREEN))

def main():
    """Main function to run the dependency checker."""
    print(color_text("LedFx Dependency Checker", Colors.HEADER + Colors.BOLD))
    print(color_text("=" * 60, Colors.HEADER))
    results = check_and_install_dependencies()
    print_summary(results)

if __name__ == "__main__":
    main() 