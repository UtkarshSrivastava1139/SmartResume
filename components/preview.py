"""
Resume Preview Component for SmartResume AI
Renders real-time resume preview
"""

import streamlit as st
from utils.helpers import split_skills_string

def render_resume_preview(resume_data):
    """
    Render resume preview
    
    Args:
        resume_data (dict): Resume data from form inputs
    """
    st.markdown("""
    <style>
    .preview-container {
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
        color: #2c3e50;
    }
    .preview-name {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 8px;
    }
    .preview-contact {
        text-align: center;
        font-size: 11px;
        color: #555;
        margin-bottom: 20px;
    }
    .preview-section-title {
        font-size: 14px;
        font-weight: bold;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        margin-top: 16px;
        margin-bottom: 10px;
        padding-bottom: 4px;
    }
    .preview-content {
        font-size: 11px;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    .preview-subtitle {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    .preview-meta {
        font-size: 10px;
        color: #666;
        font-style: italic;
    }
    .preview-bullet {
        margin-left: 20px;
        margin-bottom: 4px;
    }
    .preview-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .preview-skill-tag {
        background-color: #e8f4f8;
        color: #1f77b4;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    preview_html = '<div class="preview-container">'
    
    # Header - Name and Contact
    name = resume_data.get('name', 'Your Name')
    email = resume_data.get('email', 'email@example.com')
    phone = resume_data.get('phone', '+91-XXXXXXXXXX')
    location = resume_data.get('location', 'City, Country')
    linkedin = resume_data.get('linkedin', '')
    portfolio = resume_data.get('portfolio', '')
    
    preview_html += f'<div class="preview-name">{name.upper()}</div>'
    
    contact_parts = [email, phone]
    if linkedin:
        contact_parts.append('LinkedIn')
    if portfolio:
        contact_parts.append('Portfolio')
    contact_parts.append(location)
    
    preview_html += f'<div class="preview-contact">{" | ".join(contact_parts)}</div>'
    
    # Professional Summary
    summary = resume_data.get('summary', '')
    if summary:
        preview_html += '<div class="preview-section-title">PROFESSIONAL SUMMARY</div>'
        preview_html += f'<div class="preview-content">{summary}</div>'
    
    # Education
    education_list = resume_data.get('education_list', [])
    if education_list:
        preview_html += '<div class="preview-section-title">EDUCATION</div>'
        for edu in education_list:
            preview_html += f'<div class="preview-content">'
            preview_html += f'<div class="preview-subtitle">{edu["degree"]} in {edu["field"]}</div>'
            status = edu.get('status', 'Completed')
            status_label = 'Graduated' if status == 'Completed' else 'Expected'
            preview_html += f'<div class="preview-meta">{edu["institution"]} | {status_label}: {edu["year"]} | Grade: {edu["grade"]}</div>'
            preview_html += '</div>'
    
    # Skills
    tech_skills = resume_data.get('technical_skills', '')
    soft_skills = resume_data.get('soft_skills', '')
    
    if tech_skills or soft_skills:
        preview_html += '<div class="preview-section-title">SKILLS</div>'
        preview_html += '<div class="preview-content">'
        
        if tech_skills:
            preview_html += '<div class="preview-subtitle">Technical Skills</div>'
            preview_html += '<div class="preview-skills">'
            skills_list = split_skills_string(tech_skills)
            for skill in skills_list:
                preview_html += f'<span class="preview-skill-tag">{skill}</span>'
            preview_html += '</div>'
        
        if soft_skills:
            preview_html += '<div class="preview-subtitle" style="margin-top: 8px;">Soft Skills</div>'
            preview_html += '<div class="preview-skills">'
            skills_list = split_skills_string(soft_skills)
            for skill in skills_list:
                preview_html += f'<span class="preview-skill-tag">{skill}</span>'
            preview_html += '</div>'
        
        preview_html += '</div>'
    
    # Work Experience
    experience_list = resume_data.get('experience_list', [])
    if experience_list:
        preview_html += '<div class="preview-section-title">WORK EXPERIENCE</div>'
        for exp in experience_list:
            preview_html += '<div class="preview-content">'
            preview_html += f'<div class="preview-subtitle">{exp["job_title"]} | {exp["company"]}</div>'
            duration = f'{exp["start_date"]} - {exp["end_date"]}'
            if exp.get('location'):
                preview_html += f'<div class="preview-meta">{duration} | {exp["location"]}</div>'
            else:
                preview_html += f'<div class="preview-meta">{duration}</div>'
            
            # Show bullet points if available, otherwise show responsibilities
            bullets = exp.get('bullet_points', [])
            if bullets:
                for bullet in bullets:
                    preview_html += f'<div class="preview-bullet">• {bullet}</div>'
            elif exp.get('responsibilities'):
                # Split responsibilities into sentences for better display
                resp_lines = exp['responsibilities'].split('.')
                for line in resp_lines:
                    line = line.strip()
                    if line:
                        preview_html += f'<div class="preview-bullet">• {line}.</div>'
            
            preview_html += '</div>'
    
    # Projects
    projects_list = resume_data.get('projects_list', [])
    if projects_list:
        preview_html += '<div class="preview-section-title">PROJECTS</div>'
        for proj in projects_list:
            preview_html += '<div class="preview-content">'
            preview_html += f'<div class="preview-subtitle">{proj["title"]}</div>'
            
            meta_parts = []
            if proj.get('duration'):
                meta_parts.append(proj['duration'])
            if proj.get('technologies'):
                meta_parts.append(f"Tech: {proj['technologies']}")
            if meta_parts:
                preview_html += f'<div class="preview-meta">{" | ".join(meta_parts)}</div>'
            
            # Show bullet points if available (STAR methodology)
            bullet_points = proj.get('bullet_points', [])
            if bullet_points:
                preview_html += '<ul style="margin: 8px 0; padding-left: 20px;">'
                for bullet in bullet_points:
                    preview_html += f'<li style="margin: 4px 0;">{bullet}</li>'
                preview_html += '</ul>'
            else:
                # Fallback to description if no bullets
                description = proj.get('description', '')
                if description:
                    preview_html += f'<div style="margin-top: 4px;">{description}</div>'
            
            if proj.get('url'):
                preview_html += f'<div class="preview-meta">URL: {proj["url"]}</div>'
            
            preview_html += '</div>'
    
    # Certifications & Achievements
    certifications = resume_data.get('certifications', '')
    if certifications:
        preview_html += '<div class="preview-section-title">CERTIFICATIONS & ACHIEVEMENTS</div>'
        preview_html += '<div class="preview-content">'
        cert_lines = certifications.split('\n')
        for cert in cert_lines:
            cert = cert.strip()
            if cert:
                preview_html += f'<div class="preview-bullet">• {cert}</div>'
        preview_html += '</div>'
    
    preview_html += '</div>'
    
    st.markdown(preview_html, unsafe_allow_html=True)

def render_empty_preview():
    """Render empty state for preview"""
    st.info("Fill in the form to see your resume preview here")
    st.markdown("""
    ### Get Started
    
    1. **Fill in Personal Information** - Start with your basic details
    2. **Add Education** - Include your academic background
    3. **List Your Skills** - Add technical and soft skills
    4. **Add Experience** - Include your work history
    5. **Add Projects** - Showcase your best work
    6. **Use AI Enhancement** - Let AI improve your content
    7. **Download PDF** - Get your professional resume
    """)
