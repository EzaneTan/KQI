from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from model_registry.registry_manager import log_and_register

def main():
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(n_estimators=10).fit(X, y)
    params = model.get_params()
    metrics = {"accuracy": model.score(X, y)}

    mv = log_and_register(model, params, metrics, model_name="iris-rf")
    print(f"Registered model version: {mv.version} (name={mv.name})")

if __name__ == "__main__":
    main()
