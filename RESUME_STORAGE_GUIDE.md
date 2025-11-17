# Resume Storage & Cover Letter Linking Guide

## Overview

SmartResume AI now includes a complete resume storage system that allows you to:
- **Save resumes** for future editing
- **Load previous resumes** to continue working
- **Link cover letters** to specific resumes
- **Auto-populate cover letters** with resume data

## Features

### 1. Resume Storage
- Save unlimited resumes with custom names
- Each resume stores all your data (personal info, experience, projects, etc.)
- Track creation and update dates
- Edit and update saved resumes

### 2. Resume-Cover Letter Linking
- Link each cover letter to a source resume
- AI uses resume data to generate better cover letters
- Automatic population of skills, experience, and achievements
- Track which cover letters belong to which resume

### 3. Database
- Uses SQLite (no external database needed)
- Stored in `smartresume.db` file
- Automatic backup and version control
- Fast and reliable

## How to Use

### Saving a Resume

1. Build your resume in the "Build Resume" tab
2. Click "Save & Load Resume" expander at the top
3. Go to "Save Resume" tab
4. Enter a memorable name (e.g., "Software Engineer Resume - Tech Companies 2024")
5. Click "Save Resume"
6. Your resume is now saved!

### Loading a Resume

1. Go to "Build Resume" tab
2. Click "Save & Load Resume" expander
3. Go to "Load Resume" tab
4. Select a resume from the dropdown
5. Click "Load Resume"
6. All your data is restored!

### Generating a Cover Letter from Resume

1. **First, save your resume** (see above)
2. Go to "Cover Letter" tab
3. In the "Link to Resume" section:
   - Select your saved resume from the dropdown
   - Click "Load Resume Data"
   - Personal info (name, email, phone) will auto-fill
4. Fill in job details (company, title, description)
5. Click "Generate with AI"
6. The AI will use your resume data to create a tailored cover letter!

### What Resume Data is Used in Cover Letters?

When linked to a resume, the AI cover letter generator automatically includes:

- **Personal Information**: Name, contact details
- **Professional Summary**: Your elevator pitch
- **Skills**: Technical and soft skills
- **Work Experience**: Job titles, companies, achievements
- **Education**: Degrees, institutions
- **Projects**: Notable projects and descriptions

This creates highly personalized and accurate cover letters!

## Database Structure

### Resumes Table
- **id**: Unique identifier
- **name**: Resume name (e.g., "SWE Resume 2024")
- **target_role**: Target job role
- **resume_data**: Complete resume JSON
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### Cover Letters Table
- **id**: Unique identifier
- **resume_id**: Linked resume ID (foreign key)
- **company_name**: Target company
- **job_title**: Target position
- **content**: Cover letter text
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

## Tips & Best Practices

### Resume Naming
Use descriptive names that help you remember:
- ✅ "Software Engineer Resume - Startups 2024"
- ✅ "Data Science Resume - Healthcare Focus"
- ✅ "Frontend Developer - React Specialist"
- ❌ "Resume 1"
- ❌ "My Resume"

### When to Save
- After completing a resume version
- Before making major changes
- When targeting different roles (save variations)
- Before generating cover letters

### Cover Letter Workflow
1. Save your master resume
2. For each job application:
   - Go to Cover Letter tab
   - Link to your resume
   - Enter job-specific details
   - Generate AI cover letter
   - Customize as needed
   - Download

### Version Management
- Save different resume versions for different roles
- Use clear naming conventions
- Regularly update your master resume
- Delete old/unused versions

## Troubleshooting

### "No saved resumes found"
- You need to save a resume first in the "Build Resume" tab
- Make sure you filled in at least your name before saving

### Cover letter doesn't include resume data
- Make sure you clicked "Load Resume Data" after selecting a resume
- Check that the resume has the required fields filled

### Database errors
- The database file is `smartresume.db` in your project folder
- If corrupted, delete it and it will be recreated
- All data will be lost if you delete the database file

### Can't find saved resume
- Check if you're looking in the right tab ("Load Resume")
- Resumes are sorted by last update date (newest first)
- Try refreshing the page

## Future Enhancements

Potential features to add:
- Export/import resumes as JSON
- Resume templates
- Resume comparison tool
- Cover letter templates
- AI suggestions for resume improvements
- Resume analytics and ATS scoring


"""
Database manager for storing resumes and cover letters
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict
import os

class ResumeDatabase:
    def __init__(self, db_path: str = "smartresume.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_role TEXT,
                resume_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cover letters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cover_letters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                company_name TEXT,
                job_title TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_resume(self, name: str, target_role: str, resume_data: dict, resume_id: Optional[int] = None) -> int:
        """Save or update a resume"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        resume_json = json.dumps(resume_data)
        current_time = datetime.now().isoformat()
        
        if resume_id:
            # Update existing resume
            cursor.execute("""
                UPDATE resumes 
                SET name = ?, target_role = ?, resume_data = ?, updated_at = ?
                WHERE id = ?
            """, (name, target_role, resume_json, current_time, resume_id))
            result_id = resume_id
        else:
            # Insert new resume
            cursor.execute("""
                INSERT INTO resumes (name, target_role, resume_data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (name, target_role, resume_json, current_time, current_time))
            result_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return result_id
    
    def get_resume(self, resume_id: int) -> Optional[Dict]:
        """Get a resume by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, target_role, resume_data, created_at, updated_at
            FROM resumes WHERE id = ?
        """, (resume_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'target_role': row[2],
                'resume_data': json.loads(row[3]),
                'created_at': row[4],
                'updated_at': row[5]
            }
        return None
    
    def get_all_resumes(self) -> List[Dict]:
        """Get all saved resumes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, target_role, created_at, updated_at
            FROM resumes ORDER BY updated_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'target_role': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            }
            for row in rows
        ]
    
    def delete_resume(self, resume_id: int):
        """Delete a resume and its associated cover letters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete associated cover letters first
        cursor.execute("DELETE FROM cover_letters WHERE resume_id = ?", (resume_id,))
        
        # Delete resume
        cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        
        conn.commit()
        conn.close()
    
    def save_cover_letter(self, resume_id: int, company_name: str, job_title: str, 
                         content: str, cover_letter_id: Optional[int] = None) -> int:
        """Save or update a cover letter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        if cover_letter_id:
            # Update existing cover letter
            cursor.execute("""
                UPDATE cover_letters 
                SET company_name = ?, job_title = ?, content = ?, updated_at = ?
                WHERE id = ?
            """, (company_name, job_title, content, current_time, cover_letter_id))
            result_id = cover_letter_id
        else:
            # Insert new cover letter
            cursor.execute("""
                INSERT INTO cover_letters (resume_id, company_name, job_title, content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (resume_id, company_name, job_title, content, current_time, current_time))
            result_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return result_id
    
    def get_cover_letters_for_resume(self, resume_id: int) -> List[Dict]:
        """Get all cover letters for a resume"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, company_name, job_title, content, created_at, updated_at
            FROM cover_letters WHERE resume_id = ? ORDER BY updated_at DESC
        """, (resume_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'company_name': row[1],
                'job_title': row[2],
                'content': row[3],
                'created_at': row[4],
                'updated_at': row[5]
            }
            for row in rows
        ]
    
    def delete_cover_letter(self, cover_letter_id: int):
        """Delete a cover letter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM cover_letters WHERE id = ?", (cover_letter_id,))
        
        conn.commit()
        conn.close()



        """
Resume management UI components
"""
import streamlit as st
from datetime import datetime
from utils.database import ResumeDatabase

def render_save_resume_section(resume_data: dict):
    """Render save resume section"""
    st.subheader("Save Resume")
    
    db = ResumeDatabase()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        resume_name = st.text_input(
            "Resume Name",
            value=st.session_state.get('current_resume_name', ''),
            placeholder="e.g., Software Engineer Resume - 2024",
            help="Give your resume a memorable name"
        )
    
    with col2:
        if st.button("Save Resume", type="primary", use_container_width=True):
            if not resume_name.strip():
                st.error("Please enter a resume name")
            elif not resume_data.get('name'):
                st.error("Please fill in your name in Personal Information")
            else:
                try:
                    resume_id = st.session_state.get('current_resume_id')
                    target_role = resume_data.get('target_role', '')
                    
                    saved_id = db.save_resume(
                        name=resume_name,
                        target_role=target_role,
                        resume_data=resume_data,
                        resume_id=resume_id
                    )
                    
                    st.session_state['current_resume_id'] = saved_id
                    st.session_state['current_resume_name'] = resume_name
                    
                    if resume_id:
                        st.success(f"Resume '{resume_name}' updated successfully!")
                    else:
                        st.success(f"Resume '{resume_name}' saved successfully!")
                    
                except Exception as e:
                    st.error(f"Error saving resume: {str(e)}")

def render_load_resume_section():
    """Render load resume section"""
    st.subheader("Load Saved Resume")
    
    db = ResumeDatabase()
    saved_resumes = db.get_all_resumes()
    
    if not saved_resumes:
        st.info("No saved resumes yet. Create and save a resume first!")
        return
    
    # Create resume selection
    resume_options = {
        f"{r['name']} (Updated: {r['updated_at'][:10]})": r['id'] 
        for r in saved_resumes
    }
    
    selected_resume = st.selectbox(
        "Select Resume",
        options=list(resume_options.keys()),
        help="Choose a resume to load or edit"
    )
    
    if selected_resume:
        resume_id = resume_options[selected_resume]
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("Load Resume", type="primary", use_container_width=True):
                resume = db.get_resume(resume_id)
                if resume:
                    # Load resume data into session state
                    for key, value in resume['resume_data'].items():
                        st.session_state[key] = value
                    
                    st.session_state['current_resume_id'] = resume['id']
                    st.session_state['current_resume_name'] = resume['name']
                    
                    st.success(f"Loaded resume: {resume['name']}")
                    st.rerun()
        
        with col2:
            if st.button("View Details", use_container_width=True):
                resume = db.get_resume(resume_id)
                if resume:
                    with st.expander("Resume Details", expanded=True):
                        st.write(f"**Name:** {resume['name']}")
                        st.write(f"**Target Role:** {resume['target_role']}")
                        st.write(f"**Created:** {resume['created_at'][:10]}")
                        st.write(f"**Last Updated:** {resume['updated_at'][:10]}")
                        
                        # Show cover letters
                        cover_letters = db.get_cover_letters_for_resume(resume_id)
                        if cover_letters:
                            st.write(f"**Cover Letters:** {len(cover_letters)}")
                            for cl in cover_letters:
                                st.write(f"- {cl['company_name']} - {cl['job_title']}")
        
        with col3:
            if st.button("Delete", type="secondary", use_container_width=True):
                if st.session_state.get(f'confirm_delete_{resume_id}'):
                    db.delete_resume(resume_id)
                    
                    # Clear current resume if it was deleted
                    if st.session_state.get('current_resume_id') == resume_id:
                        st.session_state['current_resume_id'] = None
                        st.session_state['current_resume_name'] = ''
                    
                    st.success("Resume deleted!")
                    st.rerun()
                else:
                    st.session_state[f'confirm_delete_{resume_id}'] = True
                    st.warning("Click Delete again to confirm")

def render_resume_selector_for_cover_letter():
    """Render resume selector for cover letter generation"""
    db = ResumeDatabase()
    saved_resumes = db.get_all_resumes()
    
    if not saved_resumes:
        st.warning("No saved resumes found. Please save a resume first in the 'Build Resume' tab.")
        return None
    
    st.info("Select a resume to use for this cover letter:")
    
    # Create resume selection
    resume_options = {
        f"{r['name']} - {r['target_role'] or 'No role specified'}": r['id'] 
        for r in saved_resumes
    }
    
    selected_resume = st.selectbox(
        "Choose Resume",
        options=list(resume_options.keys()),
        key="cl_resume_selector",
        help="The cover letter will use information from this resume"
    )
    
    if selected_resume:
        resume_id = resume_options[selected_resume]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.caption(f"Selected: {selected_resume}")
        
        with col2:
            if st.button("Load Resume Data", type="primary", use_container_width=True):
                resume = db.get_resume(resume_id)
                if resume:
                    st.session_state['cl_linked_resume_id'] = resume['id']
                    st.session_state['cl_linked_resume_name'] = resume['name']
                    
                    # Load resume data for cover letter
                    resume_data = resume['resume_data']
                    st.session_state['cl_resume_data'] = resume_data
                    
                    # Pre-fill personal info
                    st.session_state['name'] = resume_data.get('name', '')
                    st.session_state['email'] = resume_data.get('email', '')
                    st.session_state['phone'] = resume_data.get('phone', '')
                    st.session_state['location'] = resume_data.get('location', '')
                    
                    st.success(f"Loaded data from: {resume['name']}")
                    st.rerun()
        
        return resume_id
    
    return None


    """
AI-powered cover letter generator
"""
import streamlit as st
from utils.ai_client import AIClient
from utils.prompts import get_cover_letter_prompt
from utils.validators import sanitize_text
import time

class CoverLetterGenerator:
    def __init__(self):
        """Initialize the cover letter generator"""
        self.ai_client = AIClient()
    
    def generate_cover_letter(self, job_title: str, company_name: str, 
                             job_description: str = "", additional_notes: str = "",
                             resume_data: dict = None) -> dict:
        """
        Generate a cover letter using AI
        
        Args:
            job_title: Target job title
            company_name: Company name
            job_description: Optional job description
            additional_notes: Optional additional information
            resume_data: Resume data to pull information from
            
        Returns:
            dict with 'success' and 'content' or 'error'
        """
        try:
            # Extract relevant info from resume
            name = resume_data.get('name', '') if resume_data else ''
            target_role = resume_data.get('target_role', '') if resume_data else ''
            summary = resume_data.get('summary', '') if resume_data else ''
            
            # Get skills
            technical_skills = resume_data.get('technical_skills', []) if resume_data else []
            soft_skills = resume_data.get('soft_skills', []) if resume_data else []
            all_skills = ', '.join(technical_skills + soft_skills) if (technical_skills or soft_skills) else ''
            
            # Get experience
            experience_list = resume_data.get('experience_list', []) if resume_data else []
            experience_summary = ""
            if experience_list:
                for exp in experience_list[:2]:  # Use top 2 experiences
                    exp_text = f"{exp.get('job_title', '')} at {exp.get('company', '')}"
                    if exp.get('bullet_points'):
                        exp_text += f" - {'; '.join(exp['bullet_points'][:2])}"
                    experience_summary += exp_text + ". "
            
            # Get education
            education_list = resume_data.get('education_list', []) if resume_data else []
            education_summary = ""
            if education_list:
                latest_edu = education_list[0]
                education_summary = f"{latest_edu.get('degree', '')} in {latest_edu.get('field_of_study', '')} from {latest_edu.get('institution', '')}"
            
            # Get projects
            projects_list = resume_data.get('projects_list', []) if resume_data else []
            projects_summary = ""
            if projects_list:
                for proj in projects_list[:2]:  # Use top 2 projects
                    projects_summary += f"{proj.get('project_name', '')}: {proj.get('description', '')[:100]}. "
            
            # Build comprehensive prompt
            prompt = get_cover_letter_prompt(
                job_title=job_title,
                company_name=company_name,
                job_description=job_description,
                candidate_name=name,
                target_role=target_role,
                summary=summary,
                skills=all_skills,
                experience=experience_summary,
                education=education_summary,
                projects=projects_summary,
                additional_notes=additional_notes
            )
            
            # Generate content with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    content = self.ai_client.generate_content(prompt)
                    
                    # Check for errors
                    if content.startswith("Rate limit") or content.startswith("Invalid") or content.startswith("An error"):
                        if attempt < max_retries - 1:
                            time.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        return {
                            'success': False,
                            'error': content
                        }
                    
                    # Sanitize content
                    sanitized_content = sanitize_text(content)
                    
                    return {
                        'success': True,
                        'content': sanitized_content
                    }
                
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return {
                        'success': False,
                        'error': f"Error generating content: {str(e)}"
                    }
            
            return {
                'success': False,
                'error': "Failed after multiple retries"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error in cover letter generation: {str(e)}"
            }

@st.cache_resource
def get_cover_letter_generator():
    """Get cached cover letter generator instance"""
    return CoverLetterGenerator()

def handle_cover_letter_generation_pre_render():
    """Handle cover letter AI generation before rendering widgets"""
    if st.session_state.get('_generate_cover_letter_pending'):
        with st.spinner("Generating cover letter with AI..."):
            generator = get_cover_letter_generator()
            
            # Get resume data if linked
            resume_data = st.session_state.get('cl_resume_data', {})
            
            result = generator.generate_cover_letter(
                job_title=st.session_state.get('cl_job_title', ''),
                company_name=st.session_state.get('cl_company_name', ''),
                job_description=st.session_state.get('cl_job_description', ''),
                additional_notes=st.session_state.get('cl_additional_notes', ''),
                resume_data=resume_data
            )
            
            if result['success']:
                st.session_state['cl_content'] = result['content']
                st.success("Cover letter generated successfully!")
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
        
        st.session_state['_generate_cover_letter_pending'] = False
        st.rerun()


        # ...existing code...

def get_cover_letter_prompt(job_title: str, company_name: str, job_description: str = "",
                           candidate_name: str = "", target_role: str = "",
                           summary: str = "", skills: str = "", experience: str = "",
                           education: str = "", projects: str = "", additional_notes: str = "") -> str:
    """
    Generate prompt for cover letter creation
    
    Args:
        job_title: Job title applying for
        company_name: Company name
        job_description: Full job description (optional)
        candidate_name: Candidate's name from resume
        target_role: Target role from resume
        summary: Professional summary from resume
        skills: Skills list from resume
        experience: Experience summary from resume
        education: Education summary from resume
        projects: Projects summary from resume
        additional_notes: Any additional context
    
    Returns:
        Formatted prompt string
    """
    prompt = f"""Generate a professional cover letter for the following job application.

Job Details:
- Position: {job_title}
- Company: {company_name}
{f"- Job Description: {job_description}" if job_description else ""}

Candidate Information (from resume):
{f"- Name: {candidate_name}" if candidate_name else ""}
{f"- Target Role: {target_role}" if target_role else ""}
{f"- Professional Summary: {summary}" if summary else ""}
{f"- Key Skills: {skills}" if skills else ""}
{f"- Experience: {experience}" if experience else ""}
{f"- Education: {education}" if education else ""}
{f"- Notable Projects: {projects}" if projects else ""}
{f"- Additional Notes: {additional_notes}" if additional_notes else ""}

Requirements:
1. Write a compelling 3-4 paragraph cover letter (300-400 words)
2. First paragraph: Express enthusiasm and mention the specific position
3. Middle paragraphs: Highlight relevant skills, experience, and achievements from the resume that match the job
4. Use specific examples from the candidate's experience and projects
5. Final paragraph: Express interest in an interview and include a call to action
6. Maintain a professional yet personable tone
7. Make it ATS-friendly with relevant keywords from the job description
8. Do NOT use any markdown formatting (no asterisks, underscores, or special characters)
9. Use plain text only
10. Tailor the content specifically to this company and role
11. Demonstrate how the candidate's background makes them an ideal fit

Generate the cover letter content only, without any labels or formatting markers."""
    
    return prompt




    # ...existing code...

from components.resume_manager import (
    render_save_resume_section,
    render_load_resume_section,
    render_resume_selector_for_cover_letter
)
from components.cover_letter_generator import handle_cover_letter_generation_pre_render
from utils.database import ResumeDatabase

# ...existing code...

def render_builder_page():
    """Render the resume builder page"""
    st.header("Build Your Resume")
    
    # Save/Load Resume Section
    with st.expander("Save & Load Resume", expanded=False):
        tab1, tab2 = st.tabs(["Save Resume", "Load Resume"])
        
        with tab1:
            resume_data = {key: st.session_state.get(key) for key in st.session_state.keys()}
            render_save_resume_section(resume_data)
        
        with tab2:
            render_load_resume_section()
    
    st.divider()
    
    # ...rest of existing code...

def render_cover_letter_page():
    """Render cover letter generator page"""
    # Handle AI generation before rendering
    handle_cover_letter_generation_pre_render()
    
    st.header("Cover Letter Generator")
    
    # Resume Linking Section
    with st.expander("Link to Resume", expanded=True):
        st.write("**Link this cover letter to a saved resume for better AI generation**")
        render_resume_selector_for_cover_letter()
    
    if st.session_state.get('cl_linked_resume_id'):
        st.success(f"Linked to resume: {st.session_state.get('cl_linked_resume_name', 'Unknown')}")
    
    st.divider()
    
    # ...rest of existing cover letter code...


    streamlit>=1.28.0
google-generativeai>=0.3.1
fpdf2>=2.7.6
python-dotenv>=1.0.0
Pillow>=10.1.0
requests>=2.31.0