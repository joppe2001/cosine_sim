# preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer # type: ignore
import os

def load_data(filename, na_values=None):
    if na_values is None:
        na_values = ["", " "]
    return pd.read_csv(filename, na_values=na_values)

def preprocess_data(df, feature_columns, column_weights=None):
    if column_weights is None:
        column_weights = {}
    
    mlbs = {}
    feature_matrices = []

    # Handle duration column if it exists
    if "duration" in df.columns:
        df["duration"] = (
            df["duration"].str.extract("(\d+)").astype(float)
        )  # Extract the number from the duration string
        df["duration"].fillna(df["duration"].mean(), inplace=True)

    for col in feature_columns:
        df[col] = df[col].str.split(",")
        df[col].fillna("", inplace=True)
        mlb = MultiLabelBinarizer()
        encoded_data = mlb.fit_transform(df[col])
        
        # Apply column-specific weights if provided
        weight = column_weights.get(col, 1.0)
        encoded_data = encoded_data * weight
        
        feature_matrices.append(encoded_data)
        mlbs[col] = mlb
    

    features_matrix = np.hstack(feature_matrices)
    base_path = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(os.path.join(base_path, '../cleaned_datasets/clean_set.csv'), index=False)

    return df, features_matrix, mlbs
