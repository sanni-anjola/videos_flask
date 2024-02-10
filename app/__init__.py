from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.videos
movies = db.movies

app = Flask(__name__)









# from app.views import my_view
# from app.auth import auth_view

# app.register_blueprint(my_view)
# app.register_blueprint(auth_view)


from . import routes

