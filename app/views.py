from bson import ObjectId
from flask import jsonify, request

from app.auth.roles_required import roles_required
from app.auth.models import UserRole
from .models import Movie
from app import movies, users
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def get_one_movie(id: str):
    try:
        user = users.find_one({"username": get_jwt_identity()})
        if (user['roles'].count('SUPER_USER') == 0):
            movie = movies.find_one({"_id": ObjectId(id), "user": get_jwt_identity()})
        else:
            movie = movies.find_one({"_id": ObjectId(id)})

        if not movie:
            return "Movie not found", 404
        movie.pop('_id')
        return jsonify({'id': id, **movie}), 200
    except (TypeError, ValueError):
        return "Invalid movie ID format", 400

@roles_required(UserRole.ADMIN.value)
# @jwt_required()
def add_movie():
    movie_data = request.get_json()  # Access JSON data from request
    movie = Movie(**movie_data, user=get_jwt_identity())  # Create Movie object
    movie_mongo_dict = movie.to_mongo_dict()
    result = movies.insert_one(movie_mongo_dict)
    new_movie_id = result.inserted_id  # Get the inserted ID

    
    # Return the inserted movie data as JSON
    return jsonify({"id": str(new_movie_id), **movie_data}), 201

@jwt_required()
def get_movies():
    """Retrieves all movies with pagination and limit options.

    Supports query parameters:
        - `page`: The page number (starting from 1).
        - `limit`: The number of movies per page (default: 10).
        - `filters`: Additional filtering criteria (optional).
        - `sort`: Sort field (e.g., "title", "-year").


    Returns:
        JSON response containing:
            - `movies`: List of movie dictionaries
            - `total_pages`: Number of pages for all movies
            - `current_page`: Current page number
            - `per_page`: Number of movies per page
    """

    # Get query parameters
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    sort_field = request.args.get("sort", "title")  # Default to title ascending

    # Extract and exclude pagination parameters from filters
    filters = {key: value for key, value in request.args.items() if key not in ("page", "limit", "sort")}
    user = users.find_one({"username": get_jwt_identity()})
    if (user['roles'].count('SUPER_USER') == 0):
        filters["user"] = get_jwt_identity()

    # Calculate skip and offset based on pagination
    skip = (page - 1) * limit
    
    # Sort order (ascending or descending based on prefix)
    sort_direction = 1 if sort_field.startswith("-") else -1
    sort_field = sort_field.strip("-")  # Remove any sort prefix

    # Count total movies (without applying filters yet)
    total_movies = movies.count_documents(filters)
    
    # Apply filters, excluding pagination parameters
    movies_cursor = movies.find(filters, skip=skip, limit=limit).sort([(sort_field, sort_direction)])

    # Convert cursor to list of dictionaries
    movies_list = [{'id': str(movie.pop('_id')), **movie} for movie in movies_cursor]

    # Calculate total pages and ensure valid page number
    total_pages = (total_movies + limit - 1) // limit
    page = min(page, total_pages)

    # Prepare and return JSON response
    response = {
        "movies": movies_list,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": limit,
        "total_count": total_movies
    }
    return jsonify(response), 200

