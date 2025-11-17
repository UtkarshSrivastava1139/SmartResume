"""
Form sections for user input in SmartResume AI
"""

import streamlit as st
from utils.validators import (
    validate_email, validate_phone, validate_url, 
    validate_linkedin, validate_year, validate_cgpa, validate_percentage
)

def render_personal_info_form():
    """Render personal information form section"""
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", 
                            value=st.session_state.get('name', ''),
                            placeholder="John Doe",
                            key="name")
        
        email = st.text_input("Email Address *", 
                             value=st.session_state.get('email', ''),
                             placeholder="john.doe@email.com",
                             key="email")
        
        linkedin = st.text_input("LinkedIn Profile URL", 
                                value=st.session_state.get('linkedin', ''),
                                placeholder="https://linkedin.com/in/johndoe",
                                key="linkedin")
    
    with col2:
        phone = st.text_input("Phone Number *", 
                             value=st.session_state.get('phone', ''),
                             placeholder="+91-9876543210",
                             key="phone")
        
        location = st.text_input("Location *", 
                                value=st.session_state.get('location', ''),
                                placeholder="Bangalore, India",
                                key="location")
        
        portfolio = st.text_input("Portfolio/Website", 
                                 value=st.session_state.get('portfolio', ''),
                                 placeholder="https://yourportfolio.com",
                                 key="portfolio")
    
    # Validation
    errors = []
    if name and not name.strip():
        errors.append("Name cannot be empty")
    if email and not validate_email(email):
        errors.append("Invalid email format")
    if phone and not validate_phone(phone):
        errors.append("Invalid phone number format")
    if linkedin and not validate_linkedin(linkedin):
        errors.append("Invalid LinkedIn URL format")
    if portfolio and not validate_url(portfolio):
        errors.append("Invalid portfolio URL format")
    
    if errors:
        for error in errors:
            st.error(f"{error}")
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'linkedin': linkedin,
        'location': location,
        'portfolio': portfolio
    }

def render_professional_summary_form():
    """Render professional summary form section"""
    st.subheader("Professional Summary")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        target_role = st.text_input("Target Job Role *", 
                                   value=st.session_state.get('target_role', ''),
                                   placeholder="e.g., Software Engineer, Data Analyst",
                                   key="target_role")
    
    with col2:
        experience_years = st.number_input("Years of Experience", 
                                          min_value=0, 
                                          max_value=50,
                                          value=st.session_state.get('experience_years', 0),
                                          key="experience_years")
    
    summary = st.text_area("Professional Summary", 
                          value=st.session_state.get('summary', ''),
                          placeholder="Enter a brief professional summary or click 'Generate with AI' below...",
                          height=120,
                          key="summary")
    
    return {
        'target_role': target_role,
        'experience_years': experience_years,
        'summary': summary
    }

def render_education_form():
    """Render education form section"""
    st.subheader("Education")
    
    # Initialize education list in session state
    if 'education_list' not in st.session_state:
        st.session_state.education_list = []
    
    # Form for adding new education
    with st.expander("Add Education", expanded=len(st.session_state.education_list) == 0):
        col1, col2 = st.columns(2)
        
        with col1:
            degree = st.selectbox("Degree/Qualification", 
                                 ["B.Tech", "M.Tech", "BCA", "MCA", "B.Sc", "M.Sc", 
                                  "MBA", "BBA", "B.Com", "M.Com", "BA", "MA", "PhD", "Other"],
                                 key="new_degree")
            
            institution = st.text_input("Institution Name", 
                                       placeholder="ABC University",
                                       key="new_institution")
            
            field = st.text_input("Field of Study", 
                                 placeholder="Computer Science",
                                 key="new_field")
        
        with col2:
            year = st.number_input("Year of Graduation", 
                                  min_value=1950, 
                                  max_value=2030,
                                  value=2024,
                                  key="new_year")
            
            grade_type = st.radio("Grade Type", ["CGPA", "Percentage"], key="new_grade_type")
            
            if grade_type == "CGPA":
                grade = st.number_input("CGPA", 
                                       min_value=0.0, 
                                       max_value=10.0, 
                                       step=0.1,
                                       format="%.2f",
                                       key="new_grade")
                grade_display = f"{grade}/10.0"
            else:
                grade = st.number_input("Percentage", 
                                       min_value=0.0, 
                                       max_value=100.0, 
                                       step=0.1,
                                       format="%.2f",
                                       key="new_grade")
                grade_display = f"{grade}%"
        
        if st.button("Add Education Entry", key="add_education"):
            if institution and field:
                st.session_state.education_list.append({
                    'degree': degree,
                    'field': field,
                    'institution': institution,
                    'year': year,
                    'grade': grade_display,
                    'grade_type': grade_type
                })
                st.success("Education added!")
                st.rerun()
            else:
                st.error("Please fill in institution and field of study")
    
    # Display added education
    if st.session_state.education_list:
        st.write("**Added Education:**")
        for idx, edu in enumerate(st.session_state.education_list):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**{edu['degree']} in {edu['field']}** - {edu['institution']} ({edu['year']}) - {edu['grade']}")
            with col2:
                if st.button("Delete", key=f"del_edu_{idx}"):
                    st.session_state.education_list.pop(idx)
                    st.rerun()
    
    return st.session_state.education_list

def render_skills_form():
    """Render skills form section"""
    st.subheader(" Skills")
    
    col1, col2 = st.columns(2)
    
    with col1:
        technical_skills = st.text_area("Technical Skills (comma-separated)", 
                                       value=st.session_state.get('technical_skills', ''),
                                       placeholder="Python, JavaScript, React, Node.js, SQL, Git",
                                       height=100,
                                       key="technical_skills")
    
    with col2:
        soft_skills = st.text_area("Soft Skills (comma-separated)", 
                                  value=st.session_state.get('soft_skills', ''),
                                  placeholder="Leadership, Communication, Problem Solving, Teamwork",
                                  height=100,
                                  key="soft_skills")
    
    return {
        'technical_skills': technical_skills,
        'soft_skills': soft_skills
    }

def render_experience_form():
    """Render work experience form section"""
    st.subheader("Work Experience")
    
    # Initialize experience list
    if 'experience_list' not in st.session_state:
        st.session_state.experience_list = []
    
    # Form for adding new experience
    with st.expander("Add Work Experience", expanded=len(st.session_state.experience_list) == 0):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("Company Name", 
                                   placeholder="ABC Technologies",
                                   key="new_company")
            
            job_title = st.text_input("Job Title", 
                                     placeholder="Software Engineer",
                                     key="new_job_title")
            
            start_date = st.text_input("Start Date", 
                                      placeholder="January 2022",
                                      key="new_start_date")
        
        with col2:
            location_exp = st.text_input("Location", 
                                        placeholder="Bangalore, India",
                                        key="new_location_exp")
            
            is_current = st.checkbox("Currently working here", key="new_is_current")
            
            if not is_current:
                end_date = st.text_input("End Date", 
                                        placeholder="December 2023",
                                        key="new_end_date")
            else:
                end_date = "Present"
        
        responsibilities = st.text_area("Key Responsibilities", 
                                       placeholder="Describe your main responsibilities and tasks...",
                                       height=100,
                                       key="new_responsibilities")
        
        if st.button("Add Experience Entry", key="add_experience"):
            if company and job_title and start_date and responsibilities:
                st.session_state.experience_list.append({
                    'company': company,
                    'job_title': job_title,
                    'location': location_exp,
                    'start_date': start_date,
                    'end_date': end_date,
                    'is_current': is_current,
                    'responsibilities': responsibilities,
                    'bullet_points': []  # Will be filled by AI or manual entry
                })
                st.success("Experience added!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    # Display added experiences
    if st.session_state.experience_list:
        st.write("**Added Work Experience:**")
        for idx, exp in enumerate(st.session_state.experience_list):
            col1, col2 = st.columns([5, 1])
            with col1:
                duration = f"{exp['start_date']} - {exp['end_date']}"
                st.write(f"**{exp['job_title']}** at {exp['company']} ({duration})")
            with col2:
                if st.button("Delete", key=f"del_exp_{idx}"):
                    st.session_state.experience_list.pop(idx)
                    st.rerun()
    
    return st.session_state.experience_list

def render_projects_form():
    """Render projects form section"""
    st.subheader("Projects")
    
    # Initialize projects list
    if 'projects_list' not in st.session_state:
        st.session_state.projects_list = []
    
    # Form for adding new project
    with st.expander("Add Project", expanded=len(st.session_state.projects_list) == 0):
        col1, col2 = st.columns(2)
        
        with col1:
            project_title = st.text_input("Project Title", 
                                         placeholder="AI Chatbot Application",
                                         key="new_project_title")
            
            duration = st.text_input("Duration", 
                                    placeholder="Jan 2023 - Mar 2023",
                                    key="new_duration")
        
        with col2:
            technologies = st.text_input("Technologies Used", 
                                        placeholder="Python, TensorFlow, React",
                                        key="new_technologies")
            
            project_url = st.text_input("Project URL/GitHub (optional)", 
                                       placeholder="https://github.com/username/project",
                                       key="new_project_url")
        
        description = st.text_area("Project Description", 
                                  placeholder="Describe what the project does, your role, and key achievements...",
                                  height=100,
                                  key="new_description")
        
        if st.button("Add Project Entry", key="add_project"):
            if project_title and description:
                st.session_state.projects_list.append({
                    'title': project_title,
                    'duration': duration,
                    'technologies': technologies,
                    'url': project_url,
                    'description': description,
                    'enhanced_description': ''  # Will be filled by AI
                })
                st.success("Project added!")
                st.rerun()
            else:
                st.error("Please fill in project title and description")
    
    # Display added projects
    if st.session_state.projects_list:
        st.write("**Added Projects:**")
        for idx, proj in enumerate(st.session_state.projects_list):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**{proj['title']}** ({proj['duration']})")
            with col2:
                if st.button("Delete", key=f"del_proj_{idx}"):
                    st.session_state.projects_list.pop(idx)
                    st.rerun()
    
    return st.session_state.projects_list

def render_certifications_form():
    """Render certifications and achievements form section"""
    st.subheader("Certifications & Achievements")
    
    certifications = st.text_area("Certifications & Achievements (one per line)", 
                                 value=st.session_state.get('certifications', ''),
                                 placeholder="AWS Certified Solutions Architect (2023)\nFirst Prize in National Hackathon (2022)\nPublished research paper in IEEE Journal",
                                 height=120,
                                 key="certifications")
    
    return certifications
