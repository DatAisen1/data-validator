from functools import wraps
from datetime import datetime
import time


def validate(data, **rules):
# data is a dict, rules are field: expected_type pairs     
# # Return a list of error strings (empty = valid)     
    pass

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Elapsed time: {end_time - start_time:.4f} seconds")
        return res
    return wrapper

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f' Calling {func.__name__} with args = {args}, kwargs = {kwargs}')
        print(args, kwargs)
        result = func(*args, **kwargs)
        print("Return value:", result)
        return result
    return wrapper
    
