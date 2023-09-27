import logging

import stepwise as S

from stepwise.utils import configure_custom_logger


def is_debug():
    return True  # change this value to verify the condition is working

def task_pipeline_1():
    yield S.retry(
        worker=lambda ctx: ctx.logger.debug("toto"),
        name="toto"
    )

    yield S.retry(
        worker=lambda ctx: ctx.logger.warning("tata"),
        name="tata"
    )

if __name__ == '__main__':
    # this will disable most logs (can change default Formatter too)
    configure_custom_logger(level=logging.INFO)

    S.run({"pipeline_1": task_pipeline_1})
