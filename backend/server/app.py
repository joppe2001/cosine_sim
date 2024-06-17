from server.config import create_app # type: ignore
from server.data_loader import load_from_local # type: ignore
from server.routes import register_routes # type: ignore

app = create_app()

# Data loading
df = load_from_local("models/model1/dataframe.pkl")
cosine_sim = load_from_local("models/model1/cosine_similarity_matrix.pkl")

register_routes(app, df, cosine_sim)

# Main application entry point
if __name__ == "__main__":
    app.run(debug=True, port=3000, ssl_context=("localhost.pem", "localhost-key.pem"))
