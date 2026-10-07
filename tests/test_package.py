"""Exercise the installed package and module entry point."""

import subprocess
import sys
from importlib.metadata import version

import analyze


def test_installed_package() -> None:
    assert analyze.__doc__
    assert version("analyze") == "0.1.0"


def test_module_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "analyze", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == version("analyze")
