import yaml
from sklearn.model_selection import ParameterGrid
from training_scripts import train_agent  # your existing entrypoint
from model_evaluation import evaluate_agent

def load_config(path="config/hp_search.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()
    param_grid = list(ParameterGrid(cfg["hyperparameters"]))
    best_score, best_params = -float("inf"), None

    for params in param_grid:
        print(f"→ Training with params: {params}")
        model = train_agent(**params)
        score = evaluate_agent(model, cfg["eval_dataset"])
        print(f"   Score: {score:.4f}")

        if score > best_score:
            best_score, best_params = score, params

    print(f"✅ Best score: {best_score:.4f} @ {best_params}")
    # dump best_params to disk
    with open("best_params.yaml", "w") as f:
        yaml.safe_dump(best_params, f)

if __name__ == "__main__":
    main()
