"""qe_foundations - helpers for QE Foundations."""

from qe_foundations.utils.strings import normalize_whitespace, slugify, is_valid_email
from qe_foundations.utils.numbers import is_positive_int, clamp, percent
from qe_foundations.utils.dates import add_days, is_weekend, timestamp_for_filename
from qe_foundations.utils.data_gen import FIRST_NAMES, ROLES, make_users

__all__ = [
    "normalize_whitespace",
    "slugify",
    "is_valid_email",
    "is_positive_int",
    "clamp",
    "percent",
    "add_days",
    "is_weekend",
    "timestamp_for_filename",
    "FIRST_NAMES",
    "ROLES",
    "make_users",
]