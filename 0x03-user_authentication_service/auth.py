#!/usr/bin/env python3
""" Module contains a password hashing method."""
import bcrypt
from db import DB
from db import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ This method takes a 'password' string argument,
    and hashing it using 'bycrypt.hashpw',
    returns bytes"""
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()  # Generate a random salt
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """ This method generates a UUID,
    using the uuid model."""
    return str(uuid4())


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
            self._db.find_user_by(email=email)
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Expects two arguments:
        email: user email,
        passworf: user password,
        return True if email matches,
        False in any other case."""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """ This method takes an email string argument,
        and returns session id string."""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """Takes a single argument "email",
        and return the corresponding User or None
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session associated with a given user.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)
