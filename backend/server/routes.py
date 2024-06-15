from flask import request, jsonify
from server.recommender import recommend_anime # type: ignore

def register_routes(app, df, cosine_sim):
    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/recommend", methods=["POST"])
    def get_recommendations():
        """Endpoint for fetching anime recommendations."""
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
                "similarity_percentage": similarity_percentage,
            }
            for name, score, url, genres, themes, producer, studios, allRank, similarity_percentage in recommendations.values
        ]
        return jsonify(result)

    @app.route("/version")
    def version():
        return "Version 2"
