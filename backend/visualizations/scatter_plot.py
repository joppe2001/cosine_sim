import pandas as pd
import seaborn as sns  # type: ignore
import os
import matplotlib.pyplot as plt

base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base_path, "../models/model1/dataframe.pkl")
# filename = os.path.join(base_path, "../cleaned_datasets/clean_set.csv")
# df = pd.read_csv(filename)
df = pd.read_pickle(filename)

df["allRank"] = df["allRank"].astype(str).str.extract(r"(\d+)").astype(float)
df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["scoredByUser"] = pd.to_numeric(df["scoredByUser"], errors="coerce")
df = df.dropna(subset=["duration", "score", "allRank", "scoredByUser"])

def plot_correlation_heatmap(df):
    """
    Plots a correlation heatmap using the given DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be visualized.

    Returns:
        None
    """
    plt.figure(figsize=(12, 8))
    corr_matrix = df[["duration", "score", "allRank", "scoredByUser"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation Heatmap")
    plt.show()



def plot_scatter(df, x, y, hue=None):
    """
    Plots a scatter plot using the given DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be visualized.
        x (str): The name of the column to be used as the x-axis.
        y (str): The name of the column to be used as the y-axis.
        hue (str, optional): The name of the column to be used as the color hue. Defaults to None.

    Returns:
        None
    """
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x=x, y=y, hue=hue)
    plt.title(f"Scatter Plot of {y} vs {x}")
    plt.show()


def plot_box(df, x, y):
    """
    Plots a box plot using the given DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be visualized.
        x (str): The name of the column to be used as the x-axis.
        y (str): The name of the column to be used as the y-axis.

    Returns:
        None
    """
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x=x, y=y)
    plt.title(f"Box Plot of {y} by {x}")
    plt.xticks(rotation=45)
    plt.show()


plot_correlation_heatmap(df)

plot_scatter(df, "duration", "score")
plot_scatter(df, "allRank", "score")

genres_df = df.explode("genres")
plot_box(genres_df, "genres", "score")
