from flask import Blueprint, jsonify, request
from .models import Movie

# auth_view = Blueprint('auth_view', __name__, url_prefix="/auth")

# @auth_view.route('/')
def home():
    return  "Hello", 200