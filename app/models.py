from pymongo import MongoClient

class Movie:
    # def __init__(self, title, year, genres, embedded_data, dynamic_data=None, dynamic_embedded_data=None):
    def __init__(self, title, year, genres):
        self.title = title
        self.year = year
        self.genres = genres
        # self.embedded_data = embedded_data
        # self.dynamic_data = dynamic_data
        # self.dynamic_embedded_data = dynamic_embedded_data

    def to_mongo_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            # "embedded_data": self.embedded_data,
            # **self.dynamic_data,  # Unpack dictionary
            # **{key: value.to_mongo_dict() for key, value in self.dynamic_embedded_data.items()}  # Handle embedded dict/class instances
        }