from app import jwt
from flask import jsonify
from flask_jwt_extended import create_access_token, JWTError, get_jwt_identity


jwt.jwt_error_handler(token_type="access")  # Handle access token errors gracefully
jwt.jwt_error_handler(token_type="refresh")  # Handle refresh token errors gracefully

@jwt.expired_token_loader
def jwt_expired_token_loader(expired_token):
    try:
        identity = get_jwt_identity()
        new_token = create_access_token(identity=identity, additional_claims={"roles": identity.roles})
        return new_token
    except (JWTError, KeyError):
        return jsonify({"message": "The token is invalid or expired"}), 401