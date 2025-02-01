import pandas as pd
from models.risk_assessor import RiskAssessor
from training.data_preprocessing import preprocess_data

# Load data
data = pd.read_csv("data/risk_data.csv")
X, y = preprocess_data(data)

# Train the model
assessor = RiskAssessor()
assessor.train(X, y)