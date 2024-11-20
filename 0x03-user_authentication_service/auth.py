#!/usr/bin/env python3
""" Module contains a password hashing method."""
import bcrypt


def _hash_password(self, password: str) -> bytes:
    """ This method takes a 'password' string argument,
    and hashing it using 'bycrypt.hashpw',
    returns bytes"""
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()  # Generate a random salt
    return bcrypt.hashpw(password, salt)

# password = "my_secure_password".encode('utf-8')  # Convert to bytes
# salt = bcrypt.gensalt()  # Generate a random salt
# hashed = bcrypt.hashpw(password, salt)
# print(hashed)

_hash_password(password='Testpwd')