import os
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Callable, Any, Dict, OrderedDict

import doit

from stepwise.job_status import JobStatus, Status
from stepwise.utils import custom_logger


@dataclass
class Workspace:
    root: Path
    logger: Logger


Worker = Callable[[Workspace], Any]


def step(worker: Worker, name: str):
    def _step_fn():
        root = Path.cwd()
        (root / name).mkdir(exist_ok=True, parents=True)
        os.chdir(str(root / name))

        ctx = Workspace(root=root, logger=custom_logger(name))
        ctx.logger.info("Start")

        status = JobStatus.load(Path.cwd())

        try:
            status.update(Status.RUNNING)
            worker(ctx)
            status.update(Status.SUCCESS)
        except Exception as e:
            status.update(Status.FAILED)
            raise e

        ctx.logger.info("End")
        os.chdir(str(root))

        f = open(os.path.join(name, "infos.txt"), "w")
        print("Done", file=f)
        f.close()

    return _step_fn


def run(task_creators: Dict):
    """
    run all steps/tasks defined in file
    using doit command
    task_creators=globals()
    """

    doit.run(task_creators)


def task(worker: Worker, name: str, force: bool = False) -> Dict:
    """
    Create a doit action for a worker: func+name
    """
    targets = list()

    uptodate = not force

    if not (name is None):
        targets = [f"{name}/infos.txt"]

    return {
        "name": name,
        'actions': [(step(worker, name), (), dict())],
        'verbosity': 1,
        "uptodate": [uptodate],
        "targets": targets
    }


def retry(worker: Worker, name: str) -> Dict:
    return task(worker, name, force=True)


def chain(steps: OrderedDict, name: str, force: bool = False) -> Dict:
    for sub_name, worker in steps.items():
        yield task(worker, f"{name}/{sub_name}", force=force)
