from validator import timer, log_call
import time
from valErr import ValidationError

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

def main():
    raw_record = sample_data

    try: 
        validate_record = validate(raw_record)
    except ValidationError as e:
        print(f"Validation failed for field '{e.field}': {e.message}")

validate(sample_data)
