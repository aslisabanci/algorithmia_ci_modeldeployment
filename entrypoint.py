import os
from src import algorithmia_utils, notebook_utils

if __name__ == "__main__":
    repo_name = os.getenv("INPUT_CURRENT_REPO")
    repo_path = "/github/workspace/{}".format(repo_name)

    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    print("notebook path:", notebook_path)
    remote_upload_path = os.getenv("INPUT_REMOTE_UPLOAD_PATH")
    model_file_path = os.getenv("INPUT_MODEL_FILE_PATH")

    if not algorithmia_api_key:
        raise Exception("field 'algorithmia_api_key' not defined in workflow")
    # TODO: continue checks

    if os.path.exists(repo_path):
        workspace_notebook_path = "{}/{}".format(repo_path, notebook_path)
        print("workspace notebook path:", workspace_notebook_path)
        notebook_utils.run_notebook(
            notebook_path=workspace_notebook_path, execution_path=repo_path
        )

        test_model_name = "autodeployed_model.pkl"
        test_model_full_path = "{}/{}".format(repo_path, test_model_name)
        remote_path = "data://asli/automated_deploy"
        algorithmia_utils.upload_model(
            algorithmia_api_key, test_model_full_path, remote_path, test_model_name
        )
    else:
        raise Exception(
            "actions/checkout on the local repo must be run before this action can be completed"
        )
