"""
Classic Resume Template
Professional template for resume PDF generation
"""

class ClassicTemplate:
    """Classic resume template configuration"""
    
    # Color scheme (RGB)
    COLORS = {
        'primary': (31, 119, 180),      # Blue
        'text': (0, 0, 0),              # Black
        'meta': (100, 100, 100),        # Gray
        'accent': (52, 73, 94)          # Dark gray
    }
    
    # Font sizes
    FONT_SIZES = {
        'name': 20,
        'section_title': 12,
        'subtitle': 11,
        'body': 11,
        'meta': 10
    }
    
    # Spacing
    SPACING = {
        'section': 5,
        'subsection': 3,
        'paragraph': 2,
        'line': 5
    }
    
    # Margins
    MARGINS = {
        'top': 15,
        'bottom': 15,
        'left': 10,
        'right': 10
    }
    
    @staticmethod
    def get_section_order():
        """Get default section order for resume"""
        return [
            'professional_summary',
            'education',
            'skills',
            'work_experience',
            'projects',
            'certifications'
        ]
    
    @staticmethod
    def get_bullet_character():
        """Get bullet point character"""
        return chr(149)  # •
