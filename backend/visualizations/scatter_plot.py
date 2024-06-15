import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
import os

base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base_path, "../models/model1/dataframe.pkl")  # Change this to your dataset path

# Load the data
df = pd.read_pickle(filename)

# Print initial data info for debugging
print("Initial Data Info:")
print(df.info())

# Inspect the first few rows to understand the data better
print("\nInitial Data Sample:")
print(df.head())

# Inspect unique values in problematic columns
print("\nUnique values in 'duration':")
print(df['duration'].unique())

print("\nUnique values in 'score':")
print(df['score'].unique())

# For 'allRank', let's clean it and ensure it only contains numeric values
# First, let's inspect a sample of the 'allRank' values
print("\nSample values in 'allRank':")
print(df['allRank'].head(20))

# Convert 'allRank' to numeric by removing non-numeric characters and coercing errors
df['allRank'] = df['allRank'].astype(str).str.extract(r'(\d+)').astype(float)

# Ensure numeric columns do not contain lists
# Convert duration and score to numeric
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
df['score'] = pd.to_numeric(df['score'], errors='coerce')

# Drop rows with NaN values in these columns to avoid issues in correlation
df = df.dropna(subset=['duration', 'score', 'allRank'])

# Print data info after processing
print("\nData Info After Processing:")
print(df.info())

# Function to create a correlation heatmap
def plot_correlation_heatmap(df):
    plt.figure(figsize=(12, 8))
    corr_matrix = df[['score', 'duration', 'allRank']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.show()

# Function to create scatter plots
def plot_scatter(df, x, y, hue=None):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x=x, y=y, hue=hue)
    plt.title(f'Scatter Plot of {y} vs {x}')
    plt.show()

# Function to create box plots
def plot_box(df, x, y):
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x=x, y=y)
    plt.title(f'Box Plot of {y} by {x}')
    plt.xticks(rotation=45)
    plt.show()

# Plot correlation heatmap
plot_correlation_heatmap(df)

# Plot scatter plots
plot_scatter(df, 'duration', 'score')
plot_scatter(df, 'allRank', 'score')

# Plot box plots
# For genres, we need to explode the genres column as it is a list
genres_df = df.explode('genres')
plot_box(genres_df, 'genres', 'score')
