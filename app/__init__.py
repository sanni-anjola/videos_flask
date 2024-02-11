from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.videos
movies = db.movies
users = db.users

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "your_strong_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15)  # Set your desired expiry time
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)  # Set your desired expiry time

jwt = JWTManager(app)








# from app.views import my_view
# from app.auth import auth_view

# app.register_blueprint(my_view)
# app.register_blueprint(auth_view)


from . import routes

