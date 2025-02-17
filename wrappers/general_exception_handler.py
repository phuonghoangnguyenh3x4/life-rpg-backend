from typing import Callable
from flask import make_response
import logging

def general_exception_handler(error_msg: str = 'An error occurred') -> Callable:
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.exception(e)
                return make_response(error_msg, 500)
        return wrapper
    return decorator
