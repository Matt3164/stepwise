import json
import subprocess
import time
from enum import Enum, auto
from pathlib import Path
from typing import Union

from stepwise.utils import custom_logger

PATH = Path

class Status(Enum):
    CREATED = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()


class JobStatus:
    def __init__(
        self,
        name: str,
        worker_time: int,
        disk_usage: str,
        status: Status,
        path: Path,
        last_time: float,
    ):

        self.name = name
        self.worker_time = worker_time
        self.disk_usage = disk_usage
        self.status = status
        self.path = path
        self.last_time = last_time

    @staticmethod
    def load(path: PATH):
        name = path.name
        path = Path(path) / ".status.json"
        status = None
        try:
            with path.open() as _:
                data = json.load(_)
                data["status"] = Status[data["status"]]
                data["path"] = path
                data["last_time"] = time.time()
                status = JobStatus(**data)
        except:
            status = JobStatus(
                name=str(name),
                worker_time=0,
                disk_usage="unknown",
                status=Status.CREATED,
                path=path,
                last_time=time.time(),
            )

        status.update()
        return status

    def update(self, status: Status = None):
        log = custom_logger(self.name)
        self.disk_usage = _disk_usage(self.path.parent)
        if status is not None and status != self.status:
            old_status = self.status
            self.status = status
            log.info(f"{old_status.name} -> {self.status.name}")

        now = time.time()
        self.worker_time += now - self.last_time
        self.last_time = now

        try:
            with self.path.open("w") as _:
                json.dump(
                    {
                        "name": self.name,
                        "worker_time": self.worker_time,
                        "disk_usage": self.disk_usage,
                        "status": self.status.name,
                    },
                    _,
                    indent=4,
                    sort_keys=True,
                )
        except Exception as e:
            log.error(f"Error while updating JobStatus : {str(e)}")


def _disk_usage(path: Union[str, Path]):
    try:
        return subprocess.check_output(["du", "-sh", str(path)]).split()[0].decode("utf-8")
    except:
        return "unknown"
