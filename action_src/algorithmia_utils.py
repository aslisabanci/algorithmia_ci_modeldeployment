import Algorithmia
import logging


def upload_model(local_path, remote_path):
    logging.info("will upload model from {} to {}".format(local_path, remote_path))
