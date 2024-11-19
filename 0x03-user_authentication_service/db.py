#!/usr/bin/env python3
"""DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    # def add_user(self, email: str, hashed_password: str) -> User:
    #     """
    #     Adds a user to the database.

    #     Args:
    #     email (str): The email address of the user.
    #     hashed_password (str): The hashed password of the user.

    #     Returns:
    #     User: The User object representing the newly added user.
    #     """
    #     session = self._session
    #     user = User(email=email, hashed_password=hashed_password)
    #     session.add(user)
    #     session.commit()
    #     session.refresh(user)
    #     return user

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Finding an user object based on the passed arguments"""
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates an user which it's 'id' is passed as an argument,
        and update the user's attriutes as passed as arguments,
        and commit to the database."""
        user = self._session.query(User).filter_by(user_id).first()
        if not user:
            return NoResultFound

        for key, value in kwargs:
            if not hasattr(User, key):
                raise ValueError

            setattr(user, key, value)

        self._session.commit()
