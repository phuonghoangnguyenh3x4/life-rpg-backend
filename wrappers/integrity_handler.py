from typing import Callable
from flask import make_response
import logging
from sqlite_utils.utils import sqlite3

def integrity_error_handler(error_msg: str) -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.IntegrityError:
                logging.exception(sqlite3.IntegrityError)
                return make_response(error_msg, 400)
        return wrapper
    return decorator