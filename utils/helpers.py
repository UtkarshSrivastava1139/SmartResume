"""
Helper utility functions for SmartResume AI
"""

from datetime import datetime

def format_phone_number(phone):
    """
    Format phone number for display
    
    Args:
        phone (str): Phone number
        
    Returns:
        str: Formatted phone number
    """
    # Remove all non-digit characters except +
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    return cleaned

def format_date_range(start_date, end_date=None, is_current=False):
    """
    Format date range for display
    
    Args:
        start_date (str): Start date
        end_date (str): End date
        is_current (bool): Whether this is a current position
        
    Returns:
        str: Formatted date range
    """
    if is_current:
        return f"{start_date} - Present"
    elif end_date:
        return f"{start_date} - {end_date}"
    else:
        return start_date

def calculate_duration(start_date, end_date=None):
    """
    Calculate duration between dates
    
    Args:
        start_date (str): Start date (format: "Month Year")
        end_date (str): End date (format: "Month Year") or None for current
        
    Returns:
        str: Duration string (e.g., "2 years 3 months")
    """
    try:
        # Simple duration calculation
        # This is a simplified version - could be enhanced
        if end_date:
            return ""  # Could implement actual date parsing
        else:
            return ""
    except:
        return ""

def truncate_text(text, max_length=100, suffix="..."):
    """
    Truncate text to maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].strip() + suffix

def generate_filename(name):
    """
    Generate PDF filename from name
    
    Args:
        name (str): Person's name
        
    Returns:
        str: Sanitized filename
    """
    # Remove special characters and replace spaces
    filename = ''.join(c if c.isalnum() or c.isspace() else '' for c in name)
    filename = '_'.join(filename.split())
    return f"{filename}_Resume.pdf"

def split_skills_string(skills_string):
    """
    Split comma-separated skills string into list
    
    Args:
        skills_string (str): Comma-separated skills
        
    Returns:
        list: List of individual skills
    """
    if not skills_string:
        return []
    skills = [s.strip() for s in skills_string.split(',')]
    return [s for s in skills if s]  # Remove empty strings

def join_skills_list(skills_list):
    """
    Join list of skills into comma-separated string
    
    Args:
        skills_list (list): List of skills
        
    Returns:
        str: Comma-separated skills string
    """
    if not skills_list:
        return ""
    return ", ".join(skills_list)

def get_current_year():
    """Get current year"""
    return datetime.now().year

def get_current_month_year():
    """Get current month and year formatted"""
    return datetime.now().strftime("%B %Y")

def clean_bullet_points(text):
    """
    Clean and format bullet points from AI output
    
    Args:
        text (str): Text with bullet points
        
    Returns:
        list: List of cleaned bullet points
    """
    if not text:
        return []
    
    lines = text.strip().split('\n')
    bullet_points = []
    
    for line in lines:
        line = line.strip()
        # Remove common bullet point markers
        line = line.lstrip('•-*→▸▪ ')
        if line:
            bullet_points.append(line)
    
    return bullet_points

def format_bullet_point(text):
    """
    Format a single bullet point
    
    Args:
        text (str): Bullet point text
        
    Returns:
        str: Formatted bullet point
    """
    text = text.strip()
    # Ensure it starts with capital letter
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    # Ensure it ends with period
    if text and text[-1] not in '.!?':
        text += '.'
    return text
