#!/usr/bin/python3

import os, json
from action_src import algorithmia_utils, notebook_utils
import logging

if __name__ == "__main__":
    repo_name = os.getenv("INPUT_CURRENT_REPO")
    repo_path = "/github/workspace/{}".format(repo_name)

    # TODO: needed?
    algo_hash = os.getenv("GITHUB_SHA")

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    print(f"notebook path: {notebook_path}")
    remote_upload_path = os.getenv("INPUT_REMOTE_UPLOAD_PATH")
    model_file_path = os.getenv("INPUT_MODEL_FILE_PATH")

    # metric = os.getenv("INPUT_METRIC")
    # threshold = os.getenv("INPUT_THRESHOLD")
    # checkpoints = os.getenv("INPUT_CHECKPOINTS")

    # github_token = os.getenv("GITHUB_TOKEN")
    # github_repo = os.getenv("GITHUB_REPOSITORY")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: continue checks

    if os.path.exists(repo_path):
        workspace_notebook_path = f"{repo_path}/{notebook_path}"
        print(f"workspace notebook path: {workspace_notebook_path}")
        notebook_utils.run_notebook(workspace_notebook_path)

        notebook_output_file = f"{repo_path}/test_out.txt"
        with open(notebook_output_file) as f:
            test_file_contents = f.read()
            print(test_file_contents)
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )
