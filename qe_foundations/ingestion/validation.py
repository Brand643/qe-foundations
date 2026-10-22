"""qe_foundations/ingestion/validation.py  -  TASK 5 (about 25 min)

validate_record() decides whether ONE raw record is acceptable.

IMPORTANT: this is VALIDATION OF EXTERNAL DATA. Raise exceptions here.
Do NOT use `assert` in this file (assertions can be switched off with `python -O`).
See README Task 5 for the exact rules.
"""
import math
from .exceptions import InvalidValueError, MissingFieldError

REQUIRED_FIELDS = ("id", "title", "status", "duration")
VALID_STATUSES = ("pass", "fail", "blocked")


def validate_record(row, raw):
    """Turn one raw record into a clean dict, or raise a RecordValidationError.

    row : 1-based record number in the file (used in error messages)
    raw : whatever the reader produced for that record (usually a dict)

    Returns {"id": str, "title": str, "status": str, "duration": float}.
    """
    if not isinstance(raw, dict):
        raise InvalidValueError(row, "record", raw, "an object with the test fields")

    # Check that all required fields exist and are not blank.
    for name in REQUIRED_FIELDS:
        value = raw.get(name)

        if value is None or str(value).strip() == "":
            raise MissingFieldError(row, name)

    # Normalize and validate the status.
    status = str(raw["status"]).strip().lower()

    if status not in VALID_STATUSES:
        raise InvalidValueError(row, "status", raw["status"], f"one of {VALID_STATUSES}")

    raw_duration = raw["duration"]

    if isinstance(raw_duration, bool):
        raise InvalidValueError(row, "duration", raw_duration, "a finite number greater than or equal to 0")

    # Convert the duration to a float.
    try:
        duration = float(raw_duration)
    except (ValueError, TypeError) as error:
        raise InvalidValueError(row, "duration", raw_duration, "a finite number greater than or equal to 0") from error

    # Reject NaN, positive/negative infinity, and negative values.
    if not math.isfinite(duration) or duration < 0:
        raise InvalidValueError(row, "duration", raw_duration, "a finite number greater than or equal to 0")

    # Return a new dictionary containing normalized values.
    return {
        "id": str(raw["id"]).strip(),
        "title": str(raw["title"]).strip(),
        "status": status,
        "duration": duration,
    }
