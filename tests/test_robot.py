import subprocess
import sys

from app.robot_manager import ROBOT_PATH


def test_robot_counts_from_start_number():
    process = subprocess.Popen(
        [sys.executable, str(ROBOT_PATH), "--start", "7"],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        lines = [process.stdout.readline().strip() for _ in range(3)]
    finally:
        process.kill()
        process.wait()

    assert lines == ["7", "8", "9"]