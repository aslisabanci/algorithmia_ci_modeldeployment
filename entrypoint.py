#!/usr/bin/python3

import os
from src.algorithmia_deployer import AlgorithmiaDeployer
from src.notebook_executor import NotebookExecutor


if __name__ == "__main__":
    workspace = os.getenv("GITHUB_WORKSPACE")
    github_repo = os.getenv("GITHUB_REPOSITORY")
    commit_SHA = os.getenv("GITHUB_SHA")
    commit_msg = os.getenv("HEAD_COMMIT_MSG")
    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    algorithmia_username = os.getenv("INPUT_ALGORITHMIA_USERNAME")
    algorithmia_algo_name = os.getenv("INPUT_ALGORITHMIA_ALGONAME")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    model_path = os.getenv("INPUT_MODEL_PATH")
    # algorithmia_algo_dir = os.getenv("INPUT_ALGORITHMIA_ALGO_DIR")
    upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH")

    error_template_str = "Field '{}' not defined in workflow file. Please check your workflow configuration"
    if not algorithmia_api_key:
        raise Exception(error_template_str.format("algorithmia_api_key"))
    # TODO: Add new inputs checks too
    if not model_path:
        raise Exception(error_template_str.format("model_path"))
    if not upload_path:
        raise Exception(error_template_str.format("algorithmia_uploadpath"))

    if os.path.exists(workspace):
        try:
            notebook_executor = NotebookExecutor(workspace, notebook_path)
            notebook_executor.run()

            algorithmia_deployer = AlgorithmiaDeployer(
                api_key=algorithmia_api_key,
                username=algorithmia_username,
                algo_name=algorithmia_algo_name,
                model_path=model_path,
                # algo_dir=algorithmia_algo_dir,
                workspace_path=workspace,
            )
            algorithmia_deployer.check_upload_link_algomodel(
                upload_path=upload_path,
                commit_SHA=commit_SHA,
                github_repo=github_repo,
                commit_msg=commit_msg,
            )
        except Exception as e:
            raise e
    else:
        raise Exception(
            "actions/checkout action should be run on the main repository, before this action. Please check your workflow configuration."
        )