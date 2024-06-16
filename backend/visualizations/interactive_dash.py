import dash # type: ignore
import dash_core_components as dcc # type: ignore
import dash_html_components as html # type: ignore
import pandas as pd 
import plotly.express as px # type: ignore
import os

base_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(
    base_path, "../models/model1/dataframe.pkl"
)  # Change this to your dataset path

# Load the data
df = pd.read_pickle(filename)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Anime Recommendation Dashboard"),
    
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in df['genres'].explode().dropna().unique()],
        multi=True,
        placeholder="Select genres"
    ),
    
    dcc.Graph(id='genre-distribution')
])

# Callback to update the genre distribution chart based on selected genres
@app.callback(
    dash.dependencies.Output('genre-distribution', 'figure'),
    [dash.dependencies.Input('genre-dropdown', 'value')]
)
def update_genre_distribution(selected_genres):
    if selected_genres is None or len(selected_genres) == 0:
        filtered_df = df
    else:
        filtered_df = df[df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]
    
    genre_counts = filtered_df['genres'].explode().value_counts()
    fig = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genres', 'y': 'Count'})
    fig.update_layout(title='Distribution of Selected Anime Genres')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
