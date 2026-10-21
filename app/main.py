from contextlib import asynccontextmanager, suppress
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.robot_manager import RobotAlreadyRunning, RobotManager, RobotNotRunning

robot = RobotManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    with suppress(RobotNotRunning):
        robot.stop()


app = FastAPI(title="Robot service", lifespan=lifespan)


class StartRequest(BaseModel):
    start_number: int = 0


class RobotStatus(BaseModel):
    running: bool
    pid: int | None = None
    start_number: int | None = None
    started_at: datetime | None = None


@app.post("/robot/start", response_model=RobotStatus)
def start_robot(body: StartRequest | None = None):
    start_number = body.start_number if body else 0
    try:
        robot.start(start_number)
    except RobotAlreadyRunning:
        raise HTTPException(status_code=409, detail="Robot is already running")
    return robot.status()


@app.post("/robot/stop", response_model=RobotStatus)
def stop_robot():
    try:
        robot.stop()
    except RobotNotRunning:
        raise HTTPException(status_code=409, detail="Robot is not running")
    return robot.status()


@app.get("/robot/status", response_model=RobotStatus)
def get_status():
    return robot.status()