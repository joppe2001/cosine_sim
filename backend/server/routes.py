from flask import request, jsonify
from server.recommender import recommend_anime # type: ignore

def register_routes(app, df, cosine_sim):

    @app.route("/", methods=["POST"])
    def get_recommendations():
        """
        Registers routes for the Flask application.

        Args:
            app (Flask): The Flask application instance.
            df (pandas.DataFrame): The DataFrame containing the anime data.
            cosine_sim (numpy.ndarray): The cosine similarity matrix.

        Returns:
            None

        Endpoints:
            - "/": Endpoint for fetching anime recommendations.
                - Method: POST
                - Request Body: JSON object with "user_history" key containing a list of anime names.
                - Response: JSON object with a list of anime recommendations. Each recommendation is a dictionary with the following keys:
                    - "name": The name of the anime.
                    - "score": The score of the anime.
                    - "url": The URL of the anime.
                    - "genres": The genres of the anime.
                    - "themes": The themes of the anime.
                    - "producer": The producer of the anime.
                    - "studios": The studios of the anime.
                    - "allRank": The rank of the anime.
                    - "rating": The rating of the anime.
                    - "favorites": The number of favorites of the anime.
                    - "similarity_percentage": The similarity percentage of the anime.
        """
        user_history = request.json.get("user_history", [])
        recommendations = recommend_anime(df, cosine_sim, user_history)
        result = [
            {
                "name": name,
                "score": score,
                "url": url,
                "genres": genres,
                "themes": themes,
                "producer": producer,
                "studios": studios,
                "allRank": allRank,
                "rating": rating,
                "favorites": favorites,
                "similarity_percentage": similarity_percentage
            }
            for name, score, url, genres, themes, producer, studios, allRank, rating, favorites, similarity_percentage in recommendations.values
        ]
        return jsonify(result)