"""qe_foundations/ingestion/exceptions.py  -  TASK 2 (about 25 min)

The exception hierarchy for the data-ingestion module. Target tree:

    IngestionError
    +-- SourceError                 the FILE is unusable      -> stop loading that file
    |   +-- SourceNotFoundError
    |   +-- SourceUnreadableError
    |   +-- UnsupportedFormatError
    |   +-- MalformedSourceError
    |   +-- MissingColumnsError
    +-- RecordValidationError       ONE RECORD is bad         -> reject it, keep going
        +-- MissingFieldError
        +-- InvalidValueError
        +-- DuplicateIdError

Already done for you: IngestionError, SourceError, SourceNotFoundError and
RecordValidationError. They show the pattern (store useful attributes, build a
readable message, call super().__init__).

YOUR JOB: replace every `pass  # TODO` below with a real class body.
See README Task 2 for the exact attributes and message rules.
"""

from pathlib import Path


class IngestionError(Exception):
    """Base class: `except IngestionError` catches everything this module raises."""


# ---- The whole source (file) is unusable ----------------------------------
class SourceError(IngestionError):
    """A file as a whole cannot be used. Carries the path and a detail text."""

    def __init__(self, path, detail):
        self.path = str(path)
        self.detail = detail
        super().__init__(f"{Path(path).name}: {detail}")


class SourceNotFoundError(SourceError):
    """EXAMPLE (done for you): the file does not exist."""

    def __init__(self, path):
        super().__init__(path, "file not found")


class SourceUnreadableError(SourceError):

    def __init__(self, path, os_error):
        detail = f"cannot be read ({type(os_error).__name__})"
        super().__init__(path, detail)


class UnsupportedFormatError(SourceError):

    def __init__(self, path, suffix):
        self.suffix = suffix
        super().__init__(path, f"unsupported file type {suffix}")


class MalformedSourceError(SourceError):

    def __init__(self, path, detail):
        super().__init__(path, detail)


class MissingColumnsError(SourceError):

    def __init__(self, path, missing):
        self.missing = list(missing)
        super().__init__(path, f"missing required columns: {', '.join(self.missing)}")


# ---- One record is invalid -------------------------------------------------
class RecordValidationError(IngestionError):
    """One record is invalid. `row` is the 1-based record number in the file."""

    def __init__(self, row, field_name, message):
        self.row = row
        self.field = field_name
        super().__init__(f"Row {row}: {message}")


class MissingFieldError(RecordValidationError):

    def __init__(self, row, field_name):
        super().__init__(row, field_name, f"missing required field: {field_name}")


class InvalidValueError(RecordValidationError):

    def __init__(self, row, field_name, value, expected):
        self.value = value
        self.expected = expected
        super().__init__(row, field_name, f"invalid value: {value} for field: {field_name}; expected: {expected}")


class DuplicateIdError(RecordValidationError):

    def __init__(self, row, test_id):
        self.test_id = test_id
        super().__init__(row, "id", f"duplicate test id: {test_id}")
