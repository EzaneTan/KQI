from .mlflow_client import MLflowClientWrapper

client = MLflowClientWrapper()

def log_and_register(model, params, metrics, model_name):
    with client.start_run() as run:
        client.log_params(params)
        client.log_metrics(metrics)
        client.log_model(model, artifact_path="model")
        vr = client.register_model(run.info.run_id, model_name)
    return vr
