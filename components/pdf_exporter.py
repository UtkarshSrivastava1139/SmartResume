"""
PDF Exporter for SmartResume AI
Generates ATS-friendly PDF resumes
"""

from fpdf import FPDF
from utils.helpers import split_skills_string, generate_filename
import unicodedata

def sanitize_text(text):
    """
    Sanitize text to remove Unicode characters not supported by standard fonts
    and remove markdown formatting
    
    Args:
        text (str): Input text
        
    Returns:
        str: Sanitized text with only Latin-1 compatible characters
    """
    if not text:
        return ""
    
    # Remove markdown formatting
    import re
    # Remove bold/italic markers (**text**, *text*, __text__, _text_)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
    text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
    
    # Replace common Unicode characters with ASCII equivalents
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '--',  # em dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '-',   # bullet
        '\u2026': '...',  # ellipsis
        '\u00a0': ' ',   # non-breaking space
        '\u2122': '(TM)',  # trademark
        '\u00ae': '(R)',   # registered trademark
        '\u00a9': '(c)',   # copyright
    }
    
    # Apply replacements
    for unicode_char, replacement in replacements.items():
        text = text.replace(unicode_char, replacement)
    
    # Remove any remaining non-Latin-1 characters
    text = ''.join(char if ord(char) < 256 else '?' for char in text)
    
    return text

class ResumePDF(FPDF):
    """Custom PDF class for resume generation"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=10, top=10, right=10)
    
    def header(self):
        """Override header to prevent automatic header on new pages"""
        # Only add header spacing on pages after the first
        if self.page_no() > 1:
            self.set_y(10)  # Set top margin for continuation pages
    
    def footer(self):
        """Override footer to prevent automatic footer"""
        pass  # No footer needed
    
    def header_section(self, name, email, phone, location, linkedin='', portfolio=''):
        """Add header with personal information"""
        # Sanitize all inputs
        name = sanitize_text(name)
        email = sanitize_text(email)
        phone = sanitize_text(phone)
        location = sanitize_text(location)
        linkedin = sanitize_text(linkedin)
        portfolio = sanitize_text(portfolio)
        
        # Name
        self.set_font('Arial', 'B', 20)
        self.set_text_color(31, 119, 180)  # Blue color
        self.cell(0, 10, name.upper(), 0, 1, 'C')
        
        # Contact information - Line 1
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        
        contact_line_1 = f"{email} | {phone} | {location}"
        self.cell(0, 5, contact_line_1, 0, 1, 'C')
        
        # Contact information - Line 2 (Links)
        if linkedin or portfolio:
            self.set_font('Arial', 'U', 10)
            self.set_text_color(31, 119, 180)
            
            links = []
            if linkedin:
                links.append(linkedin)
            if portfolio:
                links.append(portfolio)
            
            # Center the links
            link_text = ' | '.join(links)
            self.cell(0, 5, link_text, 0, 1, 'C', link=linkedin if linkedin else portfolio)
        self.ln(5)
    
    def section_title(self, title):
        """Add section title"""
        title = sanitize_text(title)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(31, 119, 180)
        self.cell(0, 6, title.upper(), 0, 1)
        
        # Add underline
        self.set_draw_color(31, 119, 180)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        
        self.set_text_color(0, 0, 0)
    
    def add_text(self, text, font_size=11, style=''):
        """Add regular text"""
        text = sanitize_text(text)
        self.set_font('Arial', style, font_size)
        # Ensure we're within margins
        self.set_x(self.l_margin)
        self.multi_cell(0, 5, text)
        self.ln(2)
    
    def add_bullet_point(self, text, indent=5):
        """Add bullet point"""
        text = sanitize_text(text)
        self.set_font('Arial', '', 11)
        
        # Get margins
        left_margin = self.l_margin
        right_margin = self.r_margin
        page_width = self.w
        
        # Calculate effective width for text
        bullet_x = left_margin + indent
        text_x = bullet_x + 5
        text_width = page_width - text_x - right_margin
        
        # Save position
        y = self.get_y()
        
        # Add dash
        self.set_xy(bullet_x, y)
        self.cell(5, 5, "-")
        
        # Add text with explicit width
        self.set_xy(text_x, y)
        self.multi_cell(text_width, 5, text)
    
    def add_subsection(self, title, meta='', indent=0):
        """Add subsection with title and metadata"""
        title = sanitize_text(title)
        meta = sanitize_text(meta)
        
        self.set_font('Arial', 'B', 11)
        
        # Calculate available width
        available_width = self.w - self.l_margin - self.r_margin - indent
        if available_width < 10:  # Minimum width check
            available_width = self.w - self.l_margin - self.r_margin
            indent = 0
        
        self.set_x(self.l_margin + indent)
        self.multi_cell(available_width, 5, title)
        
        if meta:
            self.set_font('Arial', 'I', 10)
            self.set_text_color(100, 100, 100)
            self.set_x(self.l_margin + indent)
            self.multi_cell(available_width, 5, meta)
            self.set_text_color(0, 0, 0)
        
        # Reset X position to left margin after subsection
        self.set_x(self.l_margin)

def generate_resume_pdf(resume_data):
    """
    Generate PDF resume from resume data
    
    Args:
        resume_data (dict): Resume data
        
    Returns:
        bytes: PDF file bytes
    """
    pdf = ResumePDF()
    pdf.add_page()
    
    # Header
    pdf.header_section(
        name=resume_data.get('name', 'Your Name'),
        email=resume_data.get('email', 'email@example.com'),
        phone=resume_data.get('phone', '+91-XXXXXXXXXX'),
        location=resume_data.get('location', 'City, Country'),
        linkedin=resume_data.get('linkedin', ''),
        portfolio=resume_data.get('portfolio', '')
    )
    
    # Professional Summary
    summary = resume_data.get('summary', '')
    if summary:
        pdf.section_title('Professional Summary')
        pdf.add_text(summary)
        pdf.ln(3)
    
    # Education
    education_list = resume_data.get('education_list', [])
    if education_list:
        pdf.section_title('Education')
        for edu in education_list:
            title = f"{edu['degree']} in {edu['field']}"
            status = edu.get('status', 'Completed')
            status_label = 'Graduated' if status == 'Completed' else 'Expected'
            meta = f"{edu['institution']} | {status_label}: {edu['year']} | Grade: {edu['grade']}"
            pdf.add_subsection(title, meta)
            pdf.ln(2)
        pdf.ln(2)
    
    # Skills
    tech_skills = resume_data.get('technical_skills', '')
    soft_skills = resume_data.get('soft_skills', '')
    
    if tech_skills or soft_skills:
        pdf.section_title('Skills')
        
        if tech_skills:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 5, 'Technical Skills:', 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.set_x(pdf.l_margin)
            skills_text = ' - '.join(split_skills_string(tech_skills))
            pdf.multi_cell(0, 5, skills_text)
            pdf.ln(2)
        
        if soft_skills:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 5, 'Soft Skills:', 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.set_x(pdf.l_margin)
            skills_text = ' - '.join(split_skills_string(soft_skills))
            pdf.multi_cell(0, 5, skills_text)
            pdf.ln(2)
        
        pdf.ln(2)
    
    # Work Experience
    experience_list = resume_data.get('experience_list', [])
    if experience_list:
        pdf.section_title('Work Experience')
        for exp in experience_list:
            title = f"{exp['job_title']} | {exp['company']}"
            duration = f"{exp['start_date']} - {exp['end_date']}"
            if exp.get('location'):
                meta = f"{duration} | {exp['location']}"
            else:
                meta = duration
            
            pdf.add_subsection(title, meta)
            
            # Add bullet points
            bullets = exp.get('bullet_points', [])
            if bullets:
                for bullet in bullets:
                    pdf.add_bullet_point(bullet)
            elif exp.get('responsibilities'):
                # Split responsibilities into sentences
                resp_lines = exp['responsibilities'].split('.')
                for line in resp_lines:
                    line = line.strip()
                    if line:
                        pdf.add_bullet_point(line + '.')
            
            pdf.ln(3)
        pdf.ln(2)
    
    # Projects
    projects_list = resume_data.get('projects_list', [])
    if projects_list:
        pdf.section_title('Projects')
        for proj in projects_list:
            title = proj['title']
            
            meta_parts = []
            if proj.get('duration'):
                meta_parts.append(proj['duration'])
            if proj.get('technologies'):
                meta_parts.append(f"Technologies: {proj['technologies']}")
            
            meta = ' | '.join(meta_parts) if meta_parts else ''
            pdf.add_subsection(title, meta)
            
            # Add bullet points if available (STAR methodology)
            bullet_points = proj.get('bullet_points', [])
            if bullet_points:
                for bullet in bullet_points:
                    pdf.add_bullet_point(bullet)
            else:
                # Fallback to description if no bullets
                description = proj.get('description', '')
                if description:
                    pdf.set_font('Arial', '', 11)
                    pdf.set_x(pdf.l_margin)
                    pdf.multi_cell(0, 5, description)
            
            if proj.get('url'):
                pdf.set_font('Arial', 'I', 10)
                pdf.set_text_color(31, 119, 180)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 5, f"URL: {proj['url']}")
                pdf.set_text_color(0, 0, 0)
            
            pdf.ln(3)
        pdf.ln(2)
    
    # Certifications & Achievements
    certifications = resume_data.get('certifications', '')
    if certifications:
        pdf.section_title('Certifications & Achievements')
        cert_lines = certifications.split('\n')
        for cert in cert_lines:
            cert = cert.strip()
            if cert:
                pdf.add_bullet_point(cert)
        pdf.ln(2)
    
    # Return PDF as bytes
    pdf_output = pdf.output(dest='S')
    # FPDF2 returns bytearray, convert to bytes if needed
    return bytes(pdf_output) if isinstance(pdf_output, bytearray) else pdf_output

def create_download_button(resume_data):
    """
    Create download button for PDF
    
    Args:
        resume_data (dict): Resume data
        
    Returns:
        tuple: (pdf_bytes, filename)
    """
    import streamlit as st
    
    try:
        pdf_bytes = generate_resume_pdf(resume_data)
        filename = generate_filename(resume_data.get('name', 'Resume'))
        
        return pdf_bytes, filename
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"Error generating PDF: {str(e)}")
        st.text(error_details)  # Show full traceback for debugging
        return None, None


class CoverLetterPDF(FPDF):
    """Custom PDF class for cover letter generation"""
    
    def header(self):
        """Override header to prevent automatic header on new pages"""
        pass
    
    def footer(self):
        """Override footer to prevent automatic footer"""
        pass


def generate_cover_letter_pdf(name, email, phone, location, company, job_title, cover_letter_content):
    """
    Generate a professional cover letter PDF
    
    Args:
        name (str): Candidate's name
        email (str): Email address
        phone (str): Phone number
        location (str): Location (optional)
        company (str): Target company
        job_title (str): Target job title
        cover_letter_content (str): The cover letter body text
        
    Returns:
        bytes: PDF file content
    """
    from datetime import datetime
    
    pdf = CoverLetterPDF()
    pdf.add_page()
    
    # Set margins (1 inch = 25.4mm)
    pdf.set_margins(25.4, 25.4, 25.4)
    pdf.set_auto_page_break(auto=True, margin=25.4)
    
    # Header - Contact Info (right-aligned)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 6, sanitize_text(name), ln=True, align='R')
    
    pdf.set_font('Arial', '', 10)
    contact_line = f"{sanitize_text(email)} | {sanitize_text(phone)}"
    if location:
        contact_line += f" | {sanitize_text(location)}"
    pdf.cell(0, 5, contact_line, ln=True, align='R')
    pdf.ln(10)
    
    # Date
    today = datetime.now().strftime("%B %d, %Y")
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 5, today, ln=True)
    pdf.ln(3)
    
    # Recipient Address
    pdf.cell(0, 5, "Hiring Manager", ln=True)
    if company:
        pdf.cell(0, 5, sanitize_text(company), ln=True)
    pdf.ln(3)
    
    # Subject Line
    pdf.set_font('Arial', 'B', 11)
    subject = f"Re: Application for {sanitize_text(job_title)}"
    pdf.cell(0, 5, subject, ln=True)
    pdf.ln(3)
    
    # Salutation
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 5, "Dear Hiring Manager,", ln=True)
    pdf.ln(3)
    
    # Cover Letter Body
    pdf.set_font('Arial', '', 11)
    
    # Sanitize and split into paragraphs
    clean_content = sanitize_text(cover_letter_content)
    paragraphs = clean_content.split('\n\n')
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Use multi_cell for paragraph wrapping
            pdf.multi_cell(0, 5.5, paragraph.strip())
            pdf.ln(2.5)  # Space between paragraphs
    
    # Closing - minimal spacing to keep on one page
    pdf.ln(1)
    pdf.cell(0, 5, "Sincerely,", ln=True)
    pdf.ln(2)  # Minimal spacing between "Sincerely" and name
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, sanitize_text(name), ln=True)
    
    # Generate PDF output
    pdf_output = pdf.output(dest='S')
    return bytes(pdf_output) if isinstance(pdf_output, bytearray) else pdf_output


def create_cover_letter_download_button(name, email, phone, location, company, job_title, cover_letter_content):
    """
    Create download button for cover letter PDF
    
    Args:
        name (str): Candidate's name
        email (str): Email address
        phone (str): Phone number  
        location (str): Location
        company (str): Target company
        job_title (str): Target job title
        cover_letter_content (str): Cover letter text
        
    Returns:
        tuple: (pdf_bytes, filename) or (None, None) on error
    """
    import streamlit as st
    
    try:
        pdf_bytes = generate_cover_letter_pdf(
            name=name,
            email=email,
            phone=phone,
            location=location,
            company=company,
            job_title=job_title,
            cover_letter_content=cover_letter_content
        )
        
        # Generate filename
        safe_name = name.replace(' ', '_')
        safe_job = job_title.replace(' ', '_')
        filename = f"CoverLetter_{safe_name}_{safe_job}.pdf"
        
        return pdf_bytes, filename
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"Error generating cover letter PDF: {str(e)}")
        st.text(error_details)
        return None, None

