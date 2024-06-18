from enum import Enum

class  Weights(Enum):
    genres = 1.5
    themes = 1.5
    studios = 1.2
    allRank = 1.2
    rating = 1.2
    favorites = 1.2