from pymongo import MongoClient

class Imdb():
    def __init__(self, imdb_id, rating, votes) -> None:
        self.imdb_id = imdb_id
        self.rating = rating
        self.votes = votes

    def to_json(self):
        return {
            'imdb_id': self.imdb_id,
            'rating': self.rating,
            'votes': self.votes
        }
    
class Cast:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def to_mongo_dict(self):
        return {"name": self.name, "character": self.character}
class Movie:
    # def __init__(self, title, year, genres, embedded_data, dynamic_data=None, dynamic_embedded_data=None):
    def __init__(self, title, year, genres, casts = None):
        self.title: str = title
        self.year: int = year
        self.genres: str = genres
        # self.imdb: Imdb = imdb
        self.casts = [Cast(**cast) for cast in casts]
        # self.dynamic_data = dynamic_data
        # self.dynamic_embedded_data = dynamic_embedded_data

    def to_mongo_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            "casts": [cast.to_mongo_dict() for cast in self.casts],
            # "imdb": self.imdb,
            # **self.dynamic_data,  # Unpack dictionary
            # **{key: value.to_mongo_dict() for key, value in self.dynamic_embedded_data.items()}  # Handle embedded dict/class instances
        }