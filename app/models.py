class Cast:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def to_mongo_dict(self):
        return {"name": self.name, "character": self.character}
    
class Movie:
    # def __init__(self, title, year, genres, embedded_data, dynamic_data=None, dynamic_embedded_data=None):
    def __init__(self, title, year, genres, user, casts = None):
        self.title: str = title
        self.year: int = year
        self.genres: str = genres
        self.user: str = user
        self.casts = [Cast(**cast) for cast in casts]

    def to_mongo_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            "user": self.user,
            "casts": [cast.to_mongo_dict() for cast in self.casts],
        }