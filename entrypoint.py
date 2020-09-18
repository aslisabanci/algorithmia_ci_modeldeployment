#!/usr/bin/python3

import os

# from src import algorithmia_utils, notebook_utils


if __name__ == "__main__":
    github_repo = os.getenv("GITHUB_REPOSITORY")
    workspace = os.getenv("GITHUB_WORKSPACE")
    # commit_msg = os.getenv("HEAD_COMMIT_MSG")
    commit_SHA = os.getenv("GITHUB_SHA")

    github_env = os.getenv("GITHUB_CONTEXT")
    print(github_env)

    # algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY", "")
    # algorithmia_username = os.getenv("INPUT_ALGORITHMIA_USERNAME", "")
    # algo_name = os.getenv("INPUT_ALGORITHMIA_ALGONAME", "")

    # notebook_path = os.getenv("INPUT_NOTEBOOK_PATH", "")
    # model_rel_path = os.getenv("INPUT_MODEL_PATH", "")
    # upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH", "")

    # print(f"Pre-replacement: {upload_path}")
    # if "$ALGORITHMIA_USERNAME" in upload_path:
    #     upload_path = upload_path.replace("$ALGORITHMIA_USERNAME", algorithmia_username)
    # if "$ALGORITHMIA_ALGONAME" in upload_path:
    #     upload_path = upload_path.replace("$ALGORITHMIA_ALGONAME", algo_name)
    # print(f"Post-replacement: {upload_path}")

    # extra = os.getenv("INPUT_EXTRA")
    # print(f"extra input: {extra}")
    # commit = os.getenv("INPUT_COMMIT")
    # print(f"commit: {commit}")

    # test_dir = os.getenv("INPUT_UPLOAD_DIR")
    # print(f"test_dir: {test_dir}")

    # error_template_str = "Field '{}' not defined in workflow file. Please check your workflow configuration"
    # if not algorithmia_api_key:
    #     raise Exception(error_template_str.format("algorithmia_api_key"))
    # # TODO: Add new inputs checks too
    # if not model_rel_path:
    #     raise Exception(error_template_str.format("model_path"))
    # if not upload_path:
    #     raise Exception(error_template_str.format("algorithmia_uploadpath"))

    # if os.path.exists(workspace):
    #     if notebook_path:
    #         workspace_notebook_path = "{}/{}".format(workspace, notebook_path)
    #         if os.path.exists(workspace_notebook_path):
    #             notebook_utils.run_notebook(
    #                 notebook_path=workspace_notebook_path, execution_path=workspace
    #             )
    #         else:
    #             print(
    #                 f"Notebook file not found at path: {workspace_notebook_path}. Please check your workflow configuration."
    #             )
    #     else:
    #         print(
    #             "Notebook path is not configured, skipping the notebook execution step."
    #         )

    #     model_full_path = "{}/{}".format(workspace, model_rel_path)

    #     if os.path.exists(model_full_path):
    #         model_md5_hash = algorithmia_utils.calculate_md5(model_full_path)
    #         if model_md5_hash:
    #             algorithmia_upload_path = algorithmia_utils.upload_model(
    #                 algorithmia_api_key, model_full_path, upload_path, commit_SHA
    #             )
    #             if algorithmia_upload_path:
    #                 algo_dir = "{}/{}".format(workspace, algo_name)
    #                 algorithmia_utils.update_algo_model_config(
    #                     base_path=algo_dir,
    #                     github_repo=github_repo,
    #                     commit_SHA=commit_SHA,
    #                     commit_msg=commit_msg,
    #                     model_filepath=algorithmia_upload_path,
    #                     model_md5_hash=model_md5_hash,
    #                 )
    #             else:
    #                 raise Exception(
    #                     "Could not upload model file to Algorithmia. Stopping the workflow execution."
    #                 )
    #         else:
    #             raise Exception(
    #                 "Could not calculate model file hash. Stopping the workflow execution."
    #             )
    #     else:
    #         raise Exception(
    #             f"Model file not found at {model_full_path}. Please check your workflow configuration."
    #         )
    # else:
    #     raise Exception(
    #         "actions/checkout action should be run on the main repository, before this action can be completed. Please check your workflow configuration."
    #     )