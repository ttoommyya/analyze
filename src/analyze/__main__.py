"""Package smoke check: python -m analyze --version."""

import argparse
from importlib.metadata import version


def main() -> None:
    """Display the installed package version or usage."""
    parser = argparse.ArgumentParser(description="Shared Python analysis foundation")
    parser.add_argument("--version", action="version", version=version("analyze"))
    parser.parse_args()
    parser.print_help()


if __name__ == "__main__":
    main()
