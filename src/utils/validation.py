"""
Validation utilities for the Grade Evaluation System.
"""

import re

def validate_email(email):
    """Validate email format for EECP domain."""
    pattern = r'^[a-zA-Z0-9._%+-]+@eecp\.edu\.ph$'
    return bool(re.match(pattern, email))

def validate_mobile(mobile):
    """Validate mobile number format (must start with 09 and be 11 digits)."""
    pattern = r'^09\d{9}$'
    return bool(re.match(pattern, mobile))

def validate_required_fields(fields):
    """Validate that all required fields are filled."""
    for field_name, field_value in fields.items():
        if not field_value:
            return False
    return True
