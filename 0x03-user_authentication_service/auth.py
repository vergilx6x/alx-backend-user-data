#!/usr/bin/env python3
""" Module contains a password hashing method."""
import bcrypt
from db import DB
from db import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ This method takes a 'password' string argument,
    and hashing it using 'bycrypt.hashpw',
    returns bytes"""
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()  # Generate a random salt
    return bcrypt.hashpw(password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ This method takes two arguments,
        email: User email,
        password: User password,
        and register a user by adding them into the database"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User with email '{email}' already exists.")

        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user
