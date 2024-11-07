#!/usr/bin/env python3
""" A module that contains:
filter_datum function"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Filters sensitive fields in a message
    by replacing them with a redaction string."""
    pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\g<field>=' + redaction, message)
