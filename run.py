from validator import timer, log_call
import time

@timer 
@log_call
def validate(data):
    time.sleep(1)

    if not isinstance(data, dict):
        raise ValueError("input must be a dict")
    return all(bool(v) for v in data.values())

sample_data = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
}

validate(sample_data)
