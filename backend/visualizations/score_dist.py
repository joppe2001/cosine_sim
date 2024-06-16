import matplotlib.pyplot as plt # type: ignore
import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(
    base_path, "../models/model1/dataframe.pkl"
)  # Change this to your dataset path

# Load the data
df = pd.read_pickle(filename)

# Plot the score distribution
plt.figure(figsize=(12, 8))
df['score'].plot(kind='hist', bins=20, edgecolor='black')
plt.title('Distribution of Anime Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.show()
