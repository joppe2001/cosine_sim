import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
from preprocessing.clean import load_data, preprocess_data  # type: ignore


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


def main(filename, feature_columns, column_weights=None):
    df = load_data(filename)

    df, features_matrix, _ = preprocess_data(df, feature_columns, column_weights)

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(features_matrix).astype(np.float16)

    # Determine the next model directory
    save_directory = get_next_model_directory()

    # Save the DataFrame and cosine similarity matrix
    with open(os.path.join(save_directory, "dataframe.pkl"), "wb") as f:
        pickle.dump(df, f, protocol=4)

    with open(os.path.join(save_directory, "cosine_similarity_matrix.pkl"), "wb") as f:
        pickle.dump(cosine_sim, f, protocol=4)

    print(f"Data processed and saved successfully in {save_directory}! Well done :)")


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(
        base_path, "../data/anime_list.csv"
    )  # Change this to your dataset path
    feature_columns = [
        "genres",
        "themes",
        "studios",
        "allRank",
    ]  # Change these columns as needed
    column_weights = {"themes": 2.0}  # Adjust weights as needed

    main(filename, feature_columns, column_weights)
