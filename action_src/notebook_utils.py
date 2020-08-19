import subprocess


def run_notebook(path):
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to notebook", "--execute", path]
    )
    print(f"subprocess run result: {result}")
