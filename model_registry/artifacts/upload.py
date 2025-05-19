import mlflow

def upload_artifact(path: str, artifact_path: str = None):
    """
    Log any file/directory as an MLflow artifact under the current run.
    """
    mlflow.log_artifact(path, artifact_path=artifact_path)
