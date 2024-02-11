from flask import jsonify, request
from .models import User, UserRole
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from passlib.hash import bcrypt
from app import users
from .roles_required import roles_required

@roles_required(UserRole.ADMIN.value)
def home():
    return  "Hello", 200

def signup():
    """Registers a new user with secure password hashing."""

    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return "Missing username or password", 400

    # Check for existing user
    existing_user = users.find_one({"username": username})
    if existing_user:
        return "Username already exists", 409

    # Hash password securely
    hashed_password = bcrypt.hash(password)

     # Create new user document
    new_user = {
        "username": username,
        "password_hash": hashed_password,
        "roles": [UserRole.USER.value]
    }

    # Insert user document into the collection
    users.insert_one(new_user)

    # Optionally send confirmation email or return success message
    return jsonify({"message": "User registered successfully"}), 201



def login():
    username = request.json.get("username")
    password = request.json.get("password")

    
    user = users.find_one({"username": username})
    
    
    if user and bcrypt.verify(password, user['password_hash']):
        access_token = create_access_token(identity=username, additional_claims={"roles": user['roles']})
        refresh_token = create_refresh_token(identity=username, additional_claims={"roles": user['roles']})
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    else:
        return "Invalid credentials", 401
    

@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, additional_claims={"roles": current_user.roles})
    return jsonify({"access_token": new_access_token}), 200