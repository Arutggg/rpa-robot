import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

ROBOT_PATH = Path(__file__).resolve().parent.parent / "robot" / "robot.py"


class RobotAlreadyRunning(Exception):
    pass


class RobotNotRunning(Exception):
    pass


class RobotManager:
    def __init__(self) -> None:
        self._process: subprocess.Popen | None = None
        self._started_at: datetime | None = None
        self._start_number: int | None = None
        self._lock = threading.Lock()

    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self, start_number: int = 0) -> None:
        with self._lock:
            if self.is_running():
                raise RobotAlreadyRunning

            flags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            self._process = subprocess.Popen(
                [sys.executable, str(ROBOT_PATH), "--start", str(start_number)],
                creationflags=flags,
            )
            self._started_at = datetime.now()
            self._start_number = start_number

    def stop(self) -> None:
        with self._lock:
            if not self.is_running():
                raise RobotNotRunning

            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
            self._process = None

    def status(self) -> dict:
        if not self.is_running():
            return {"running": False}
        return {
            "running": True,
            "pid": self._process.pid,
            "start_number": self._start_number,
            "started_at": self._started_at,
        }