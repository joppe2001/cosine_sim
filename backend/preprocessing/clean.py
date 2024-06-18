# preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer  # type: ignore
import os
from columns import ColumnNames # type: ignore

def load_data(filename: str, na_values=None) -> pd.DataFrame:
    if na_values is None:
        na_values = ["", " "]
    return pd.read_csv(filename, na_values=na_values)


def preprocess_data(
    df: pd.DataFrame, feature_columns: list[str], column_weights=None
):
    if column_weights is None:
        column_weights = {}

    mlbs = {}
    feature_matrices = []

    # Handle duration column if it exists
    if ColumnNames.DURATION.value in df.columns:
        duration_column = ColumnNames.DURATION.value
        df[duration_column] = (
            df[duration_column].str.extract("(\d+)").astype(float)
        )  # Extract the number from the duration string
        df[duration_column].fillna(df[duration_column].mean(), inplace=True)

    if ColumnNames.RATING.value in df.columns:
        rating_column = ColumnNames.RATING.value
        df[rating_column] = df[rating_column].str.extract("(\d+)").astype(float)
        df[rating_column].fillna(df[rating_column].mean(), inplace=True)

        # Normalize the favorites column if it exists
    if ColumnNames.FAVORITES.value in df.columns:
        favorites_column = ColumnNames.FAVORITES.value
        df[favorites_column] = df[favorites_column].str.replace(
            ",", ""
        )  # Remove commas from the string
        df[favorites_column] = df[favorites_column].astype(float)  # Convert the string to float
        scaler = MinMaxScaler()
        df[favorites_column] = scaler.fit_transform(
            df[[favorites_column]]
        )  # Scale the favorites column

    for col in feature_columns:
        df[col] = df[col].astype(str)
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
    df.to_csv(os.path.join(base_path, "../cleaned_datasets/clean_set.csv"), index=False)

    return df, features_matrix, mlbs
