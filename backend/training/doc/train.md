
# Model Training and Saving Module Documentation

## Overview

This module, designed to load data, preprocess it, compute cosine similarity, and save the results, includes functionalities to manage model directories and save the processed data.

## Dependencies

Ensure the following libraries are installed before using this module:

```bash
pip install numpy scikit-learn pandas
```

## Functions

### `get_next_model_directory(base_dir="models")`

Creates a new directory for the next model, ensuring directories are sequentially numbered.

#### Parameters:
- `base_dir` (str, optional): Base directory where model directories are created. Defaults to `"models"`.

#### Returns:
- `str`: Path to the newly created model directory.

### `main(filename, feature_columns, column_weights=None)`

Main function to load, preprocess data, compute cosine similarity, and save the results.

#### Parameters:
- `filename` (str): Path to the CSV file containing the dataset.
- `feature_columns` (list): List of feature columns to be encoded.
- `column_weights` (dict, optional): Dictionary where keys are column names and values are weights for the encoded features. Defaults to `None`.

## Detailed Description

### Directory Management

The `get_next_model_directory` function ensures model directories are sequentially numbered:

```python
import os

def get_next_model_directory(base_dir="models"):
    os.makedirs(base_dir, exist_ok=True)
    existing_model_dirs = [
        int(name.split("model")[1])
        for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name)) and name.startswith("model")
    ]
    if not existing_model_dirs:
        next_model_num = 1
    else:
        next_model_num = max(existing_model_dirs) + 1
    next_model_dir = os.path.join(base_dir, f"model{next_model_num}")
    os.makedirs(next_model_dir, exist_ok=True)
    return next_model_dir
```

### Main Processing Function

The `main` function performs the following steps:

1. **Load and Preprocess Data**:
    - Utilizes `load_data` and `preprocess_data` functions from the `preprocessing` module.

2. **Compute Cosine Similarity**:
    - Computes the cosine similarity matrix for the feature matrix.

3. **Determine Model Directory**:
    - Uses `get_next_model_directory` to create a new model directory.

4. **Save Data**:
    - Saves the processed DataFrame and cosine similarity matrix using `pickle`.

```python
import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.clean import load_data, preprocess_data

def main(filename, feature_columns, column_weights=None):
    df = load_data(filename)
    df, features_matrix, _ = preprocess_data(df, feature_columns, column_weights)
    cosine_sim = cosine_similarity(features_matrix).astype(np.float16)
    save_directory = get_next_model_directory()
    with open(os.path.join(save_directory, "dataframe.pkl"), "wb") as f:
        pickle.dump(df, f, protocol=4)
    with open(os.path.join(save_directory, "cosine_similarity_matrix.pkl"), "wb") as f:
        pickle.dump(cosine_sim, f, protocol=4)
    print(f"Data processed and saved successfully in {save_directory}! Well done :)")
```

### Example Usage

An example of how to use this module:

```python
if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_path, "../data/anime_list.csv")  # Change this to your dataset path
    feature_columns = ["genres", "themes", "studios", "allRank", "rating", "favorites"]  # Change these columns as needed
    column_weights = {"themes": 1.5, "genres": 1.5, "allRank": 1.2, "favorites": 1.2}  # Adjust weights as needed
    main(filename, feature_columns, column_weights)
```

## Conclusion

This module facilitates the loading, preprocessing, similarity computation, and saving of datasets. It ensures each model's results are stored in a systematically organized directory, ready for further analysis or deployment.
