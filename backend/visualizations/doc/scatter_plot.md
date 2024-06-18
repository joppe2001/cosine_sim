
# Data Visualization and Analysis with Pandas and Seaborn

This document provides an overview of the code used for visualizing and analyzing a dataset using Pandas and Seaborn. The code includes functions for plotting correlation heatmaps, scatter plots, and box plots.

## Code Overview

### Importing Libraries

The following libraries are imported for data manipulation and visualization:

```python
import pandas as pd
import seaborn as sns  # type: ignore
import os
import matplotlib.pyplot as plt
```

### Loading the Data

The dataset is loaded from a pickle file. The file path is constructed using the `os.path` module to ensure compatibility across different operating systems.

```python
base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base_path, "../models/model1/dataframe.pkl")
df = pd.read_pickle(filename)
```

### Data Cleaning and Preparation

The data is cleaned and prepared for analysis. This includes converting data types and handling missing values.

```python
df["allRank"] = df["allRank"].astype(str).str.extract(r"(\d+)").astype(float)
df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["scoredByUser"] = pd.to_numeric(df["scoredByUser"], errors="coerce")
df = df.dropna(subset=["duration", "score", "allRank", "scoredByUser"])
```

## Visualization Functions

### Correlation Heatmap

The `plot_correlation_heatmap` function plots a heatmap of the correlation matrix for selected columns in the DataFrame.

```python
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
```

### Scatter Plot

The `plot_scatter` function plots a scatter plot for the specified columns in the DataFrame.

```python
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
```

### Box Plot

The `plot_box` function plots a box plot for the specified columns in the DataFrame.

```python
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
```

## Plotting Examples

### Correlation Heatmap

```python
plot_correlation_heatmap(df)
```

### Scatter Plot

Scatter plots for different columns in the DataFrame:

```python
plot_scatter(df, "duration", "score")
plot_scatter(df, "allRank", "score")
```

### Box Plot

Box plot for the `genres` column exploded from the DataFrame:

```python
genres_df = df.explode("genres")
plot_box(genres_df, "genres", "score")
```
