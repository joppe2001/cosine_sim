import pickle

def load_from_local(file_path):
    """Loads data from local file."""
    with open(file_path, "rb") as f:
        return pickle.load(f)
