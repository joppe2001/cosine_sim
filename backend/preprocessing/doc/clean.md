
# Preprocessing Module Documentation

## Overview

This module, `preprocessing.py`, is designed to load, clean, and preprocess a dataset for machine learning purposes. The main functionalities include loading data from a CSV file, handling missing values, normalizing numerical columns, and encoding categorical features.

## Dependencies

Make sure to install the required libraries before using the module:

```bash
pip install pandas numpy scikit-learn
```

## Functions

### `load_data(filename, na_values=None)`

Loads a CSV file into a Pandas DataFrame.

#### Parameters:
- `filename` (str): Path to the CSV file.
- `na_values` (list, optional): A list of strings that should be considered as NA/NaN values. Defaults to `["", " "]`.

#### Returns:
- `pd.DataFrame`: The loaded DataFrame.

### `preprocess_data(df, feature_columns, column_weights=None)`

Preprocesses the DataFrame by handling missing values, normalizing numerical columns, and encoding categorical features.

#### Parameters:
- `df` (pd.DataFrame): The input DataFrame to be preprocessed.
- `feature_columns` (list): List of feature columns to be encoded.
- `column_weights` (dict, optional): A dictionary where keys are column names and values are weights to apply to the encoded features. Defaults to `{}`.

#### Returns:
- `pd.DataFrame`: The preprocessed DataFrame.
- `np.ndarray`: The features matrix.
- `dict`: Dictionary of `MultiLabelBinarizer` objects used for encoding.

## Detailed Description

### Loading Data

The `load_data` function reads a CSV file into a Pandas DataFrame, replacing specified NA values.

```python
import pandas as pd

def load_data(filename, na_values=None):
    if na_values is None:
        na_values = ["", " "]
    return pd.read_csv(filename, na_values=na_values)
```

### Preprocessing Data

The `preprocess_data` function performs several preprocessing steps:

1. **Handling the `duration` column**:
    - Extracts numeric values from the `duration` column and fills missing values with the column's mean.

2. **Handling the `rating` column**:
    - Extracts numeric values from the `rating` column and fills missing values with the column's mean.

3. **Normalizing the `favorites` column**:
    - Removes commas and converts the `favorites` column to float.
    - Scales the `favorites` column using `MinMaxScaler`.

4. **Encoding Categorical Features**:
    - Splits string values in specified feature columns by commas.
    - Encodes these features using `MultiLabelBinarizer`.
    - Applies column-specific weights if provided.

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
import os
import columns from Columns

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
```

### Saving the Cleaned Data

The preprocessed DataFrame is saved to a new CSV file located in the `cleaned_datasets` directory.

## Example Usage

```python
import preprocessing

# Load the data
df = preprocessing.load_data('data.csv')

# Define feature columns and column weights
feature_columns = ['genre', 'tags']
column_weights = {'genre': 2.0, 'tags': 1.5}

# Preprocess the data
df_clean, features_matrix, mlbs = preprocessing.preprocess_data(df, feature_columns, column_weights)

# Now `df_clean` contains the cleaned data,
# `features_matrix` is the encoded features matrix,
# and `mlbs` is a dictionary of MultiLabelBinarizers used.
```

## Conclusion

This module provides a robust framework for preprocessing datasets, including handling missing values, normalizing numerical columns, and encoding categorical features with optional weighting. It saves the cleaned data to a CSV file for further use in machine learning pipelines.
