import Algorithmia
import os
import json
from datetime import datetime
import hashlib


def calculate_md5(filepath):
    DIGEST_BLOCK_SIZE = 128 * 64
    md5_hash = None
    try:
        with open(filepath, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(DIGEST_BLOCK_SIZE):
                file_hash.update(chunk)
        md5_hash = file_hash.hexdigest()
    except Exception as e:
        print(f"An exception occurred while getting MD5 hash of file: {e}")
    return md5_hash


def upload_model(api_key, local_path, remote_path, commit_SHA):
    _, model_name = os.path.split(local_path)
    name_before_ext, ext = tuple(os.path.splitext(model_name))
    unique_model_name = "{}_{}{}".format(name_before_ext, commit_SHA, ext)
    print(
        "will upload {} from {} to {}".format(
            unique_model_name, local_path, remote_path
        )
    )
    algo_client = Algorithmia.client(api_key)
    upload_path = None
    try:
        if not algo_client.dir(remote_path).exists():
            algo_client.dir(remote_path).create()
        full_remote_path = "{}/{}".format(remote_path, unique_model_name)
        if algo_client.file(full_remote_path).exists():
            print(f"File with the same name exists, overriding: {full_remote_path}")
        result = algo_client.file(full_remote_path).putFile(local_path)
        if result.path:
            print(f"File successfully uploaded at: {full_remote_path}")
            upload_path = result.path
    except Exception as e:
        print(f"An exception occurred while uploading model file to Algorithmia: {e}")
    return upload_path


def update_algo_model_config(
    base_path,
    github_repo,
    commit_SHA,
    commit_msg,
    model_filepath,
    model_md5_hash,
    config_rel_path="model_config.json",
):
    config = {}
    full_path = "{}/{}".format(base_path, config_rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as config_file:
            config = json.load(config_file)

    config["model_filepath"] = model_filepath
    config["model_md5_hash"] = model_md5_hash
    config["model_origin_commit_SHA"] = commit_SHA
    config["model_origin_commit_msg"] = commit_msg
    config["model_origin_repo"] = github_repo
    config["model_uploaded_utc"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    with open(full_path, "w") as new_config_file:
        json.dump(config, new_config_file)