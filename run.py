from validator import timer, log_call, validate, setup_logger
import time
from valErr import ValidationError
import logging

# List of test records
# Each record is designed to trigger a different type of validation error
test_records = [
    # 1. Missing field (no "name" key)
    {"age": 30, "email": "alice@example.com"},

    # 2. None value (email should not be None)
    {"name": "Bob", "age": 25, "email": None},

    # 3. Wrong type (age should be int, not string)
    {"name": "Charlie", "age": "thirty", "email": "charlie@example.com"},

    # 4. Empty string (name should not be empty or just spaces)
    {"name": "   ", "age": 22, "email": "dana@example.com"},

    # 5. Nested error (address.city should be str, but it's int)
    {"name": "Eve", "age": 28, "email": "eve@example.com", "address": {"city": 123}}
]


@log_call  # logs function name, arguments, and return value
@timer     # measures how long the function runs
def run_validation(data):
    # Rules define what each field should be
    # "address" is a nested rule (dictionary inside dictionary)
    rules = {
        "name": "str",
        "age": "int",
        "email": "str",
        "address": {"city": "str"}
    }
    # Calls validate() to check if data follows the rules
    return validate(data, **rules)


def main():
    # Setup logger (console + file output)
    logger = setup_logger("validator")

    # Loop through each test record
    for i, record in enumerate(test_records, start=1):
        try:
            # Run validation for each record
            run_validation(record)

            # If no error, validation passed
            logger.info(f"Test {i}: Validation successful")

        except ValidationError as e:
            # If validation fails, catch the error and log it
            logger.warning(f"Test {i}: Validation failed for field '{e.field}': {e.message}")


# Entry point of the program
if __name__ == "__main__":
    main()