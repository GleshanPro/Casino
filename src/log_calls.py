from functools import wraps
from loguru import logger

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"[CALL] {func.im_class.__name__} {func.__name__}{args, kwargs}")
        result = func(*args, **kwargs)
        # logger.info(f"[RET] {func.__name__} -> {result}")
        return result
    return wrapper