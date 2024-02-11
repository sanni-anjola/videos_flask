from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from .models import User
from app import users

# Custom decorator for role-based authorization
def roles_required(*roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            user = users.find_one({"username": current_user})
            user_roles = user['roles']
            if any(role in user_roles for role in roles):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Unauthorized"), 403
        return decorator
    return wrapper