from functools import wraps
from datetime import datetime
import time
from typing import Dict, List, Any, Optional
from valErr import ValidationError
import logging


# --------------------------------------------------
# LOGGER SETUP
# --------------------------------------------------
def setup_logger(name: str, level: int = logging.INFO, logfile: Optional[str] = None) -> logging.Logger:
    # Create or get a logger named "validator"
    logger = logging.getLogger("validator")
    logger.setLevel(logging.DEBUG)  # capture all levels

    # Prevent duplicate logs if logger is re-used
    if logger.hasHandlers():
        logger.handlers.clear()

    # Format for logs (time, level, name, message)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s — %(message)s")

    # Console handler (prints to terminal)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)
    console_log.setFormatter(formatter)

    # File handler (writes logs to validator.log)
    file_handler = logging.FileHandler("validator.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(console_log)
    logger.addHandler(file_handler)

    return logger


# --------------------------------------------------
# VALIDATION FUNCTION
# --------------------------------------------------
def validate(data: Dict[str, Any | None], **rules: str) -> None:
    # Get logger instance
    logger = logging.getLogger("validator")

    # Log start of validation
    logger.info(f"Starting validation for record: {data}")

    # Loop through each field and its expected type
    for field, expected_type in rules.items():

        # Debug log (currently hardcoded message)
        logger.debug(f"Validating field 'name' with expected type 'str'")

        # Check if field exists in data
        if field not in data:
            logger.warning("Missing field: name")
            raise ValidationError(field, f"Missing required field: {field}")

        value = data[field]

        # Check if value is None
        if value is None:
            logger.warning("Field 'name' is None")
            raise ValidationError(field, f"{field} cannot be None")

        # Validate string type
        elif expected_type == "str":
            if not isinstance(value, str) or not value.strip():
                logger.warning("data type is not str ")
                raise ValidationError(field, f"{field} must be a non-empty string")

        # Validate integer type
        elif expected_type == "int":
            if not isinstance(value, int):
                logger.warning("data type is not int ")
                raise ValidationError(field, f"{field} must be an integer")

        # Validate float type
        elif expected_type == "float":
            if not isinstance(value, float):
                logger.warning("data type is not float ")
                raise ValidationError(field, f"{field} must be a number")

        # Handle nested dictionary validation (recursive call)
        elif isinstance(expected_type, dict):
            if isinstance(value, dict):
                # Recursively validate nested fields
                validate(value, **expected_type)
            else:
                raise ValidationError(field, f"{field} must be a dictionary")

        # Unsupported rule type
        else:
            raise ValidationError(field, f"Unsupported type rule: {expected_type}")

        # Log success for each field (currently hardcoded message)
        logger.info("Validation successful for record with fields: name, age")


# --------------------------------------------------
# TIMER DECORATOR
# --------------------------------------------------
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start timer
        start_time = time.perf_counter()

        # Execute function
        res = func(*args, **kwargs)

        # End timer
        end_time = time.perf_counter()

        # Print execution time
        print(f"Elapsed time: {end_time - start_time:.4f} seconds")
        return res
    return wrapper


# --------------------------------------------------
# LOG CALL DECORATOR
# --------------------------------------------------
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Print function call details
        print(f' Calling {func.__name__} with args = {args}, kwargs = {kwargs}')
        print(args, kwargs)

        # Execute function
        result = func(*args, **kwargs)

        # Print return value
        print("Return value:", result)
        return result
    return wrapper


# --------------------------------------------------
# BATCH VALIDATION
# --------------------------------------------------
def validate_batch(records: List[Dict[str, Optional[Any]]], **rules: str) -> None:
    # Get logger (note: different name used here)
    logger = logging.getLogger("validator.log")

    # Log start of batch validation
    logger.info(f"Starting batch validation for {len(records)} records")

    errors = []  # list to store validation errors

    # Loop through each record
    for i, record in enumerate(records, start=1):
        try:
            # Validate each record
            validate(record, **rules)

        except ValidationError as e:
            # Log error (currently does not append to errors list)
            logger.error(f"{len(errors)} record(s) failed validation: {errors}")

        else:
            # Log success (runs for each successful record)
            logger.info("All records passed validation successfully")