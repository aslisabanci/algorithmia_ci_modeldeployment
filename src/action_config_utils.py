import yaml

ALGORITHMIA_CI_JOB = "algorithmia-CI-deployment"
ALGORITHMIA_MODELDEPLOY_STEP = "Deploy Model to Algorithmia"
MODELFILE_RELPATH_KEY = "modelfile_relativepath"
ALGONAME_KEY = "ALGORITHMIA_ALGONAME"


class ActionConfigUtils:
    def __init__(self, config_path=".github/workflows/main.yml") -> None:
        self.action_config_path = config_path
        self.config = None
        with open(self.action_config_path, "r") as stream:
            self.config = yaml.safe_load(stream)

    def get_algoname(self, default_name):
        algo_name = default_name
        try:
            algo_name = self.config["jobs"][ALGORITHMIA_CI_JOB]["env"][ALGONAME_KEY]
        except KeyError as e:
            print(
                f"Required keys for algorithm name do not exist in workflow YAML file: {e}"
            )
        return algo_name

    def get_model_relativepath(self, default_path):
        model_relativepath = default_path
        try:
            ci_steps = self.config["jobs"][ALGORITHMIA_CI_JOB]["steps"]
            for step in ci_steps:
                if step["name"] == ALGORITHMIA_MODELDEPLOY_STEP:
                    model_relativepath = step["with"][MODELFILE_RELPATH_KEY]
                    break
        except KeyError as e:
            print(
                f"Required keys for model file relative path do not exist in workflow YAML file: {e}"
            )
        return model_relativepath

    def get_algorithmia_filepaths(
        self, algo_name, workspace_path="/github/workspace", inference_script_name=None
    ):
        if not inference_script_name:
            inference_script_name = algo_name
        algo_script_path = (
            f"{workspace_path}/{algo_name}/src/{inference_script_name}.py"
        )
        algo_requirements_path = f"{workspace_path}/{algo_name}/requirements.txt"
        return algo_script_path, algo_requirements_path
