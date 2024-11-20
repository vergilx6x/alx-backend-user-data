#!/usr/bin/env python3
""" Module contains a password hashing method."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ This method takes a 'password' string argument,
    and hashing it using 'bycrypt.hashpw',
    returns bytes"""
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()  # Generate a random salt
    return bcrypt.hashpw(password, salt)
