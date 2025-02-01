import pandas as pd
from models.strategy_predictor import StrategyPredictor
from training.data_preprocessing import preprocess_data

# Load data
data = pd.read_csv("data/strategy_data.csv")
X, y = preprocess_data(data)

# Train the model
predictor = StrategyPredictor()
predictor.train(X, y)