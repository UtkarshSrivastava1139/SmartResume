"""
Input validation functions for SmartResume AI
"""

import re

def validate_email(email):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return False
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it contains only digits and + (for country code)
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, cleaned))

def validate_url(url):
    """
    Validate URL format
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return True  # URL is optional
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$'
    return bool(re.match(pattern, url))

def validate_linkedin(url):
    """
    Validate LinkedIn URL format
    
    Args:
        url (str): LinkedIn URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return True  # LinkedIn is optional
    pattern = r'^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9-]+/?$'
    return bool(re.match(pattern, url))

def validate_year(year):
    """
    Validate year format
    
    Args:
        year: Year to validate (int or str)
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        year_int = int(year)
        return 1950 <= year_int <= 2030
    except (ValueError, TypeError):
        return False

def validate_cgpa(cgpa, max_cgpa=10):
    """
    Validate CGPA/GPA
    
    Args:
        cgpa: CGPA to validate (float or str)
        max_cgpa (float): Maximum CGPA scale
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        cgpa_float = float(cgpa)
        return 0 <= cgpa_float <= max_cgpa
    except (ValueError, TypeError):
        return False

def validate_percentage(percentage):
    """
    Validate percentage
    
    Args:
        percentage: Percentage to validate (float or str)
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        perc_float = float(percentage)
        return 0 <= perc_float <= 100
    except (ValueError, TypeError):
        return False

def sanitize_text(text):
    """
    Sanitize text input by removing extra whitespace
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    # Remove extra whitespace
    text = " ".join(text.split())
    return text.strip()

def validate_required_field(value, field_name):
    """
    Validate that a required field is not empty
    
    Args:
        value: Value to check
        field_name (str): Name of the field for error message
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not value or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"
    return True, ""
