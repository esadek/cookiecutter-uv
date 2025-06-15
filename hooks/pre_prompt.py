import subprocess
import sys


def is_uv_installed() -> bool:
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if not is_uv_installed():
        print("ERROR: uv is not installed.")
        sys.exit(1)
