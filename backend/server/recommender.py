import pandas as pd
import numpy as np
from columns import ColumnNames # type: ignore

def recommend_anime(df, cosine_sim, user_history, N=20):
    """Generates anime recommendations based on user history."""
    user_anime_indices = _get_user_anime_indices(df, user_history)
    recommended_anime = _get_recommendations(df, cosine_sim, user_anime_indices, N * 2)
    recommended_anime = _exclude_user_history(recommended_anime, user_history)
    return recommended_anime.head(N)  # Return only top N recommendations

def _get_user_anime_indices(df: pd.DataFrame, user_history: list):
    indices = []
    for title in user_history:
        matching_anime = df[
            (df[ColumnNames.ENGNAME.value].str.lower() == title.lower()) |
            (df[ColumnNames.SYNONYMSNAME.value].str.contains(title, case=False, na=False))
        ]
        if matching_anime.empty:
            print(f"Warning: Anime titled '{title}' not found in the dataset.")
        else:
            indices.append(matching_anime.index[0])
    return indices

def _get_recommendations(df: pd.DataFrame, cosine_sim: np.ndarray, indices: list, N: int):
    """
    Generate recommendations based on the average cosine similarity and normalized scores.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the anime dataset.
        cosine_sim (np.ndarray): The cosine similarity matrix.
        indices (list): List of indices corresponding to the user's anime history.
        N (int): Number of recommendations to return.

    Returns:
        pd.DataFrame: DataFrame containing the top N recommendations.
    """
    avg_sim_scores = cosine_sim[indices].mean(axis=0)
    max_score = df[ColumnNames.SCORE.value].max()
    normalized_scores = df[ColumnNames.SCORE.value].fillna(0) / max_score
    combined_scores = avg_sim_scores + normalized_scores
    top_indices = combined_scores.nlargest(N * 2).index
    recommended = df.iloc[top_indices][[
        ColumnNames.ENGNAME.value, ColumnNames.SCORE.value, ColumnNames.URL.value, ColumnNames.GENRES.value, ColumnNames.THEMES.value, ColumnNames.PRODUCER.value, ColumnNames.STUDIOS.value, ColumnNames.ALLRANK.value, ColumnNames.RATING.value, ColumnNames.FAVORITES.value
    ]]
    recommended["similarity_percentage"] = (avg_sim_scores[top_indices] * 100).tolist()

    # Remove duplicates based on the main title of 'engName'
    recommended["main_title"] = recommended[ColumnNames.ENGNAME.value].str.split().str[0]
    recommended.drop_duplicates(subset="main_title", keep="first", inplace=True)
    recommended.drop(columns="main_title", inplace=True)

    return recommended.head(N)  # Return only top N recommendations

def _exclude_user_history(recommended, user_history):
    """
    Exclude anime titles from the recommended list that match the user's watched history.

    Parameters:
        recommended (pd.DataFrame): The DataFrame containing the recommended anime.
        user_history (list): A list of anime titles that the user has watched.

    Returns:
        pd.DataFrame: The updated DataFrame with the user's watched anime excluded.
    """
    for title in user_history:
        main_title = title.split(" ")[0]
        matching_indices = recommended[recommended[ColumnNames.ENGNAME.value].str.contains(main_title, case=False)].index
        recommended.drop(matching_indices, inplace=True)
    return recommended
