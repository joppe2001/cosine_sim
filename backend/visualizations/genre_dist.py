import matplotlib.pyplot as plt # type: ignore
import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(
    base_path, "../models/model1/dataframe.pkl"
)  # Change this to your dataset path
# Load the data
df = pd.read_pickle(filename)

# Preprocess genres for visualization
all_genres = df['genres'].explode().dropna()
genre_counts = all_genres.value_counts()

# Plot the genre distribution
plt.figure(figsize=(12, 8))
genre_counts.plot(kind='bar')
plt.title('Distribution of Anime Genres')
plt.xlabel('Genres')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

