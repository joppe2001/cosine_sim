
# Anime Recommendation Module Documentation

## Overview

This module provides functionality to generate anime recommendations based on a user's watch history using cosine similarity.

## Dependencies

Ensure the following libraries are installed before using this module:

```bash
pip install pandas numpy scikit-learn
```

## Functions

### `recommend_anime(df, cosine_sim, user_history, N=20)`

Generates anime recommendations based on user history.

#### Parameters:
- `df` (pd.DataFrame): The DataFrame containing the anime dataset.
- `cosine_sim` (np.ndarray): The cosine similarity matrix.
- `user_history` (list): List of anime titles the user has watched.
- `N` (int, optional): Number of recommendations to return. Defaults to `20`.

#### Returns:
- `pd.DataFrame`: DataFrame containing the top N recommendations.

### `_get_user_anime_indices(df, user_history)`

Finds indices in the DataFrame corresponding to the user's anime history.

#### Parameters:
- `df` (pd.DataFrame): The DataFrame containing the anime dataset.
- `user_history` (list): List of anime titles the user has watched.

#### Returns:
- `list`: List of indices corresponding to the user's anime history.

### `_get_recommendations(df, cosine_sim, indices, N)`

Generates recommendations based on the average cosine similarity of the user's watched anime and normalizes by score.

#### Parameters:
- `df` (pd.DataFrame): The DataFrame containing the anime dataset.
- `cosine_sim` (np.ndarray): The cosine similarity matrix.
- `indices` (list): List of indices corresponding to the user's anime history.
- `N` (int): Number of recommendations to return.

#### Returns:
- `pd.DataFrame`: DataFrame containing the top N recommendations.

### `_exclude_user_history(recommended, user_history)`

Excludes anime already watched by the user from the recommendations.

#### Parameters:
- `recommended` (pd.DataFrame): DataFrame containing the recommended anime.
- `user_history` (list): List of anime titles the user has watched.

#### Returns:
- `pd.DataFrame`: DataFrame with the user's watched anime excluded.

## Detailed Description

### Main Recommendation Function

The `recommend_anime` function generates anime recommendations based on a user's watch history:

```python
def recommend_anime(df, cosine_sim, user_history, N=20):
    user_anime_indices = _get_user_anime_indices(df, user_history)
    recommended_anime = _get_recommendations(df, cosine_sim, user_anime_indices, N * 2)
    recommended_anime = _exclude_user_history(recommended_anime, user_history)
    return recommended_anime.head(N)  # Return only top N recommendations
```

### Helper Functions

1. **Finding User Anime Indices**:
    - The `_get_user_anime_indices` function finds indices in the DataFrame corresponding to the user's anime history:

    ```python
    def _get_user_anime_indices(df, user_history):
        indices = []
        for title in user_history:
            matching_anime = df[
                (df["engName"].str.lower() == title.lower()) |
                (df["synonymsName"].str.contains(title, case=False, na=False))
            ]
            if matching_anime.empty:
                print(f"Warning: Anime titled '{title}' not found in the dataset.")
            else:
                indices.append(matching_anime.index[0])
        return indices
    ```

2. **Generating Recommendations**:
    - The `_get_recommendations` function generates recommendations based on the average cosine similarity and normalized scores:

    ```python
    def _get_recommendations(df, cosine_sim, indices, N):
        avg_sim_scores = cosine_sim[indices].mean(axis=0)
        max_score = df["score"].max()
        normalized_scores = df["score"].fillna(0) / max_score
        combined_scores = avg_sim_scores + normalized_scores
        top_indices = combined_scores.argsort()[-N * 2 - 1 : -1][::-1]
        recommended = df.iloc[top_indices][[
            "engName", "score", "url", "genres", "themes", "producer", "studios", "allRank", "rating", "favorites"
        ]]
        recommended["similarity_percentage"] = (avg_sim_scores[top_indices] * 100).tolist()
        recommended["main_title"] = recommended["engName"].apply(lambda x: x.split(" ")[0])
        recommended.drop_duplicates(subset="main_title", keep="first", inplace=True)
        recommended.drop(columns="main_title", inplace=True)
        return recommended.head(N)  # Return only top N recommendations
    ```

3. **Excluding User History**:
    - The `_exclude_user_history` function excludes anime already watched by the user from the recommendations:

    ```python
    def _exclude_user_history(recommended, user_history):
        for title in user_history:
            main_title = title.split(" ")[0]
            matching_indices = recommended[recommended["engName"].str.contains(main_title, case=False)].index
            recommended.drop(matching_indices, inplace=True)
        return recommended
    ```

## Example Usage

An example of how to use this module:

```python
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load preprocessed data and cosine similarity matrix
df = pd.read_pickle("path_to_dataframe.pkl")
cosine_sim = pickle.load(open("path_to_cosine_similarity_matrix.pkl", "rb"))

user_history = ["Naruto", "Attack on Titan", "Death Note"]  # Example user history

# Generate recommendations
recommendations = recommend_anime(df, cosine_sim, user_history, N=20)

print(recommendations)
```

## Conclusion

This module provides a comprehensive framework for generating personalized anime recommendations based on a user's watch history. It leverages cosine similarity and ensures recommendations are relevant and exclude previously watched titles.
