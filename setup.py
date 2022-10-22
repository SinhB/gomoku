import os
import sys


def clean_and_lint():
    for directory in ["src", "tests"]:
        os.system(f"poetry run black {directory}")
        os.system(f"poetry run isort {directory}")
        os.system(f"poetry run flake8 {directory}")


def display_help():
    print(
        """available commands:
    - lint: clean and lint sources
    """
    )


if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        print("Command missing. use lint or any other command.")
        display_help()
        sys.exit(1)

    if command == "lint":
        clean_and_lint()
    else:
        display_help()