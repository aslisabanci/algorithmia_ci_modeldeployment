import Algorithmia
import os
import json
from datetime import datetime
import hashlib


class AlgorithmiaDeployer:
    def __init__(
        self, api_key, username, algo_name, model_path, workspace_path
    ) -> None:
        self.algo_client = Algorithmia.client(api_key)
        self.username = username
        self.algo_name = algo_name
        self.model_path = model_path
        self.workspace_path = workspace_path

        self.model_full_path = f"{workspace_path}/{model_path}"

        os.environ[
            "ALGORITHMIA_SCRIPT_PATH"
        ] = f"{self.workspace_path}/{self.algo_name}/src/{self.algo_name}.py"
        os.environ[
            "ALGORITHMIA_REQUIREMENTS_PATH"
        ] = f"{self.workspace_path}/{self.algo_name}/requirements.txt"

    def check_upload_link_algomodel(
        self, upload_path, commit_SHA, github_repo, commit_msg
    ):
        if os.path.exists(self.model_full_path):
            model_md5_hash = self._calculate_model_md5()
            if model_md5_hash:
                self._replace_placeholders(upload_path)
                algorithmia_upload_path = self._upload_model(upload_path, commit_SHA)
                if algorithmia_upload_path:
                    self._update_algo_model_config(
                        github_repo=github_repo,
                        commit_SHA=commit_SHA,
                        commit_msg=commit_msg,
                        model_filepath=algorithmia_upload_path,
                        model_md5_hash=model_md5_hash,
                    )
                else:
                    raise Exception(
                        "Could not upload model file to Algorithmia. Stopping the workflow execution."
                    )
            else:
                raise Exception(
                    "Could not calculate model file hash. Stopping the workflow execution."
                )
        else:
            raise Exception(
                f"Model file not found at {self.model_full_path}. Please check your workflow configuration."
            )

    def _replace_placeholders(self, parametric_str):
        if "$ALGORITHMIA_USERNAME" in parametric_str:
            parametric_str = parametric_str.replace(
                "$ALGORITHMIA_USERNAME", self.username
            )
        if "$ALGORITHMIA_ALGONAME" in parametric_str:
            parametric_str = parametric_str.replace(
                "$ALGORITHMIA_ALGONAME", self.algo_name
            )

    def _calculate_model_md5(self):
        DIGEST_BLOCK_SIZE = 128 * 64
        md5_hash = None
        try:
            with open(self.model_full_path, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(DIGEST_BLOCK_SIZE):
                    file_hash.update(chunk)
            md5_hash = file_hash.hexdigest()
        except Exception as e:
            print(f"An exception occurred while getting MD5 hash of file: {e}")
        return md5_hash

    def _upload_model(self, remote_path, commit_SHA):
        _, model_name = os.path.split(self.model_full_path)
        name_before_ext, ext = tuple(os.path.splitext(model_name))
        unique_model_name = "{}_{}{}".format(name_before_ext, commit_SHA, ext)
        print(
            "Will upload {} from {} to {}".format(
                unique_model_name, self.model_full_path, remote_path
            )
        )

        upload_path = None
        try:
            if not self.algo_client.dir(remote_path).exists():
                self.algo_client.dir(remote_path).create()
            full_remote_path = "{}/{}".format(remote_path, unique_model_name)
            if self.algo_client.file(full_remote_path).exists():
                print(f"File with the same name exists, overriding: {full_remote_path}")
            result = self.algo_client.file(full_remote_path).putFile(
                self.model_full_path
            )
            if result.path:
                print(f"File successfully uploaded at: {full_remote_path}")
                upload_path = result.path
        except Exception as e:
            print(
                f"An exception occurred while uploading model file to Algorithmia: {e}"
            )
        return upload_path

    def _update_algo_model_config(
        self,
        github_repo,
        commit_SHA,
        commit_msg,
        model_filepath,
        model_md5_hash,
        config_rel_path="model_config.json",
    ):
        algo_dir = f"{self.workspace_path}/{self.algo_name}"
        config_full_path = f"{algo_dir}/{config_rel_path}"

        config = {}
        if os.path.exists(config_full_path):
            with open(config_full_path, "r") as config_file:
                config = json.load(config_file)

        config["model_filepath"] = model_filepath
        config["model_md5_hash"] = model_md5_hash
        config["model_origin_commit_SHA"] = commit_SHA
        config["model_origin_commit_msg"] = commit_msg
        config["model_origin_repo"] = github_repo
        config["model_uploaded_utc"] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        with open(config_full_path, "w") as new_config_file:
            json.dump(config, new_config_file)