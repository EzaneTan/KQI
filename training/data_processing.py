import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_data(data: pd.DataFrame) -> tuple:
    """
    Preprocess data for training machine learning models.

    Args:
        data (pd.DataFrame): Raw data containing features and labels.

    Returns:
        tuple: (X, y) where X is the feature matrix and y is the label vector.
    """
    # Handle missing values
    data = data.fillna(data.mean())

    # Encode categorical variables
    categorical_cols = data.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        data[col] = LabelEncoder().fit_transform(data[col])

    # Separate features and labels
    X = data.drop("target", axis=1).values
    y = data["target"].values

    # Normalize features
    X = StandardScaler().fit_transform(X)

    return X, y
