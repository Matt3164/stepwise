
# Stepwise: An Analysis Pipeline Library (PyDoIt Wrapper)

Stepwise is a Python library designed to simplify the creation and management of analysis pipelines. It allows you to 
define a sequence of steps (usually running a function) in a clear and organized manner. Stepwise is particularly 
well-suited for data analysis, ETL (Extract, Transform, Load) tasks, and automation workflows.


## Features

- **Step Definitions**: Define individual steps of your analysis pipeline using Python functions.
- **Retry Mechanism**: Set up automatic retries for steps that may fail.
- **Logging and Reporting**: Capture and report the progress, status, and errors of each step.
- **Integration with PyDoIt**: Stepwise is built as a wrapper around the [PyDoIt](https://pydoit.org/) library, leveraging its powerful task execution and automation capabilities.

## Installation

Stepwise can be installed via pip:

```bash
pip install stepwise
```

## Getting Started

To get started with Stepwise, define your analysis pipeline using Python functions and decorators. Here's a basic example:

```python
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
```

In this example, you define your analysis steps as Python functions and use Stepwise decorators to organize and run them. 
Stepwise provides a clean and efficient way to manage complex pipelines.

## Usage with PyDoIt

Stepwise is built as a wrapper around the [PyDoIt](https://pydoit.org/) library, which means you can take advantage 
of PyDoIt's powerful task execution and automation capabilities. If you are already familiar with PyDoIt, Stepwise 
seamlessly integrates with it, making it easy to transition to this library.

## Contributing

We welcome contributions from the community!

## License

Stepwise is open-source software licensed under the [MIT License](LICENSE).

---

**Note**: Stepwise is not affiliated with or endorsed by the PyDoIt project. It simply utilizes PyDoIt as a core 
component for task execution and automation within analysis pipelines.