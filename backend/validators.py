import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(email) and bool(EMAIL_RE.match(email))


def validate_trek_numbers(data):
    errors = []
    if "duration_days" in data and (not isinstance(data["duration_days"], (int, float)) or data["duration_days"] < 1):
        errors.append("duration_days must be a positive number")
    if "price" in data and (not isinstance(data["price"], (int, float)) or data["price"] < 0):
        errors.append("price must be a non-negative number")
    if "slots" in data and (not isinstance(data["slots"], (int, float)) or data["slots"] < 0):
        errors.append("slots must be a non-negative number")
    return errors
