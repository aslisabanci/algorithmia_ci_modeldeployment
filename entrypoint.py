#!/usr/bin/python3

import os
from src import algorithmia_utils, notebook_utils

print("entry outside")

if __name__ == "__main__":
    print("Entry point called")
    repo_name = os.getenv("INPUT_CURRENT_REPO")
    repo_path = "/github/workspace/{}".format(repo_name)

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    remote_upload_path = os.getenv("INPUT_REMOTE_UPLOAD_PATH")
    model_file_name = os.getenv("INPUT_MODEL_FILE_NAME")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: continue checks

    if os.path.exists(repo_path):
        workspace_notebook_path = "{}/{}".format(repo_path, notebook_path)
        print("workspace notebook path:", workspace_notebook_path)
        notebook_utils.run_notebook(
            notebook_path=workspace_notebook_path, execution_path=repo_path
        )

        test_model_full_path = "{}/{}".format(repo_path, model_file_name)
        algorithmia_utils.upload_model(
            algorithmia_api_key,
            test_model_full_path,
            remote_upload_path,
            model_file_name,
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )
