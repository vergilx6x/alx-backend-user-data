#!/usr/bin/env python3
""" A module that contains:
filter_datum function"""

import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Filters sensitive fields in a message
    by replacing them with a redaction string."""
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\g<field>=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt

    def get_db() -> mysql.connector.connection.MySQLConnection:
        """ Creates a database connector. """
        db_host = os.getenv("PERSONAL_DATA_DB_HOST", "Localhost")
        db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
        db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
        db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
        connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pwd,
            database=db_name
        )
        return connection
