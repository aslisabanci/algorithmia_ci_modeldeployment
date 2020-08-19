import Algorithmia
import logging


def upload_model(local_path, remote_path):
    logging.debug(f"will upload model from {local_path} to {remote_path}")
