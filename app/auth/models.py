from typing import List
from passlib.hash import bcrypt
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    CUSTOMER = "CUSTOMER"

    def __repr__(self) -> str:
        return self.value
class User:
    def __init__(self, username, password, roles=None):
        self.username = username
        self.password_hash = bcrypt.hash(password)
        self.roles: List[UserRole] = roles

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)