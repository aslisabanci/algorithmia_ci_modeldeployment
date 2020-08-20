import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def run_notebook(notebook_path, execution_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(
            nb, {"metadata": {"path": execution_path}},
        )
