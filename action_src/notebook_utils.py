import subprocess
import logging


def run_notebook(path):
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to notebook", "--execute", path]
    )
    logging.info("subprocess run result:", result)
