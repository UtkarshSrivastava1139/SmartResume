"""
Cover Letter Generator for SmartResume AI
Handles AI-powered cover letter generation using Google Gemini
"""

import streamlit as st
from utils.ai_client import AIClient
from utils.prompts import get_cover_letter_prompt
import re


class CoverLetterGenerator:
    """Handles cover letter generation using AI (Gemini or OpenRouter)"""
    
    def __init__(self):
        """Initialize the cover letter generator"""
        self.client = AIClient()
    
    def generate_cover_letter(self, name, email, phone, job_title, company="", 
                             job_description="", skills="", summary="", additional_notes="", education_status="Completed"):
        """
        Generate a professional cover letter using AI
        
        Args:
            name (str): Candidate's full name
            email (str): Email address
            phone (str): Phone number
            job_title (str): Target job title/role
            company (str): Target company name (optional)
            job_description (str): Job posting description (optional)
            skills (str): Key skills from resume
            summary (str): Professional summary from resume
            additional_notes (str): Any additional context
            education_status (str): Education status - "Completed" or "Pursuing"
            
        Returns:
            dict: Result with 'success' boolean and 'content' or 'error' message
        """
        try:
            # Validate required inputs
            if not name or not job_title:
                return {
                    'success': False,
                    'error': 'Name and Job Title are required to generate a cover letter.'
                }
            
            # Generate the prompt
            prompt = get_cover_letter_prompt(
                name=name,
                email=email,
                phone=phone,
                job_title=job_title,
                company=company,
                job_description=job_description,
                skills=skills,
                summary=summary,
                additional_notes=additional_notes,
                education_status=education_status
            )
            
            # Call Gemini API
            response = self.client.generate_content(prompt)
            
            # Check if response is an error message
            if response.startswith("Rate limit") or response.startswith("Invalid") or response.startswith("An error"):
                return {
                    'success': False,
                    'error': response
                }
            
            # Sanitize the generated content
            cover_letter_text = self._sanitize_cover_letter(response)
            
            return {
                'success': True,
                'content': cover_letter_text
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error generating cover letter: {str(e)}"
            }
    
    def _sanitize_cover_letter(self, text):
        """
        Remove markdown formatting and clean up the generated text
        
        Args:
            text (str): Raw AI-generated text
            
        Returns:
            str: Sanitized plain text
        """
        if not text:
            return ""
        
        # Remove markdown formatting
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
        text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__
        text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
        
        # Remove any remaining asterisks or underscores that might be markdown
        text = text.replace('**', '').replace('__', '')
        
        # Clean up extra whitespace
        text = re.sub(r'\n\n+', '\n\n', text)  # Multiple newlines to double
        text = text.strip()
        
        return text


def render_cover_letter_generator():
    """
    Render the cover letter generation section with AI button
    This function is meant to be called from the cover letter form page
    """
    st.subheader("AI-Powered Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Generate Cover Letter", type="primary", use_container_width=True):
            st.session_state['_generate_cover_letter_pending'] = True
            st.rerun()
    
    with col2:
        if st.session_state.get('cover_letter_content'):
            if st.button("Regenerate", use_container_width=True):
                st.session_state['_generate_cover_letter_pending'] = True
                st.rerun()


def handle_cover_letter_generation_pre_render():
    """
    Handle cover letter generation BEFORE rendering widgets
    This prevents session state conflicts with text_area widgets
    Must be called at the top of the page render function
    """
    if st.session_state.get('_generate_cover_letter_pending'):
        # Clear the flag
        st.session_state['_generate_cover_letter_pending'] = False
        
        # Get data from session state
        name = st.session_state.get('name', '')
        email = st.session_state.get('email', '')
        phone = st.session_state.get('phone', '')
        job_title = st.session_state.get('cl_job_title', '')
        company = st.session_state.get('cl_company', '')
        job_description = st.session_state.get('cl_job_description', '')
        additional_notes = st.session_state.get('cl_additional_notes', '')
        
        # Get resume data if linked
        resume_data = st.session_state.get('cl_resume_data', {})
        
        # Gather skills and summary from resume data or current session
        if resume_data:
            # Use data from linked resume
            skills_list = resume_data.get('skills', [])
            if isinstance(skills_list, str):
                skills = skills_list
            else:
                skills = ', '.join(skills_list) if skills_list else ''
            summary = resume_data.get('summary', '')
            
            # Get education status from resume data
            education_list = resume_data.get('education_list', [])
            if education_list and isinstance(education_list, list):
                education_status = education_list[0].get('status', 'Completed')
            else:
                education_status = 'Completed'
        else:
            # Fallback to current session state
            skills = ', '.join(st.session_state.get('skills', []))
            summary = st.session_state.get('summary', '')
            
            # Get education status from session state
            education_list = st.session_state.get('education_list', [])
            if education_list and isinstance(education_list, list):
                education_status = education_list[0].get('status', 'Completed')
            else:
                education_status = 'Completed'
        
        # Validate required fields
        if not job_title:
            st.error("Please enter a Job Title before generating the cover letter.")
            return
        
        if not name:
            st.error("Please enter your Name in the Personal Information section before generating the cover letter.")
            return
        
        # Generate cover letter
        with st.spinner("Generating your cover letter with AI..."):
            generator = CoverLetterGenerator()
            result = generator.generate_cover_letter(
                name=name,
                email=email,
                phone=phone,
                job_title=job_title,
                company=company,
                job_description=job_description,
                skills=skills,
                summary=summary,
                additional_notes=additional_notes,
                education_status=education_status
            )
        
        if result['success']:
            st.session_state['cover_letter_content'] = result['content']
            st.success("Cover letter generated successfully!")
        else:
            st.error(result['error'])
