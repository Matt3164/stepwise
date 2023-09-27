import shutil
from collections import OrderedDict

import stepwise as S


def copy_worker(ctx: S.Workspace):
    shutil.copy(str(ctx.root / "resources/file0.txt"), "file.txt")
    return None


def task_pipeline_1():
    yield S.task(
        worker=copy_worker,
        name="0_step"
    )

    yield S.retry(
        worker=copy_worker,
        name="1_step"
    )

    yield S.chain(
        name="2_step",
        steps=OrderedDict({"21_step": copy_worker, "22_step": copy_worker})
    )

if __name__ == "__main__":
    S.run(globals())
    # S.run({f.__name__: f for f in [task_pipeline_1]})
