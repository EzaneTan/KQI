import mlflow
import yaml
from pathlib import Path

# Load config
_cfg_path = Path(__file__).parent / "config.yaml"
_cfg = yaml.safe_load(_cfg_path)["mlflow"]

mlflow.set_tracking_uri(_cfg["tracking_uri"])

class MLflowClientWrapper:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient(registry_uri=_cfg["registry_uri"])
        # ensure experiment exists
        self.experiment_id = mlflow.set_experiment(_cfg["experiment_name"]).experiment_id

    def start_run(self, **kwargs):
        return mlflow.start_run(experiment_id=self.experiment_id, **kwargs)

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict, step: int = None):
        for k, v in metrics.items():
            mlflow.log_metric(k, v, step=step)

    def log_model(self, model, artifact_path: str = "model"):
        # automatically pick correct flavor if sklearn-like
        mlflow.sklearn.log_model(model, artifact_path=artifact_path)

    def register_model(self, run_id: str, artifact_path: str, model_name: str):
        """Registers the model output of a run as a new Model Version."""
        source = f"runs:/{run_id}/{artifact_path}"
        # create model (if not exists)
        try:
            self.client.create_registered_model(model_name)
        except mlflow.exceptions.RestException:
            # already exists
            pass
        mv = self.client.create_model_version(name=model_name, source=source, run_id=run_id)
        return mv
