import mlflow

from pathlib import Path
import yaml

# Load config
cfg = yaml.safe_load(Path(__file__).parent / "config.yaml")["mlflow"]
mlflow.set_tracking_uri(cfg["tracking_uri"])

class MLflowClientWrapper:
    def __init__(self):
        self.client = mlflow.tracking.MlflowClient(registry_uri=cfg["registry_uri"])

    def start_run(self, **kwargs):
        return mlflow.start_run(**kwargs)

    def log_params(self, params: dict):
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict, step=None):
        mlflow.log_metrics(metrics, step=step)

    def log_model(self, model, artifact_path: str):
        mlflow.sklearn.log_model(model, artifact_path)

    def register_model(self, run_id: str, name: str):
        return self.client.create_registered_model(name) \
            if name not in [m.name for m in self.client.list_registered_models()] \
            else None, \
            self.client.create_model_version(name, f"runs:/{run_id}/{artifact_path}")
    # …and any other thin MLflow API wrappers you need
