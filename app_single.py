"""
SmartResume AI - AI-Powered Resume Builder
Single-file version with all features integrated
"""

import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Page configuration
st.set_page_config(
    page_title="SmartResume AI - AI-Powered Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #155a8a;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .preview-box {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 2rem;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    }
    .resume-name {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .resume-contact {
        text-align: center;
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .resume-section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.3rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        'personal': {},
        'summary': '',
        'education': [],
        'skills': [],
        'experience': [],
        'projects': [],
        'certifications': []
    }

# AI Generation Function
def generate_with_ai(prompt):
    """Generate content using Gemini AI"""
    if not GEMINI_API_KEY:
        return "⚠️ Please configure your Gemini API key in the .env file"
    
    # Try multiple models in order of preference
    models_to_try = ['gemini-2.5-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 1024,
                }
            )
            return response.text.strip()
        except Exception as e:
            error_str = str(e).lower()
            print(f"Tried {model_name}, Error: {str(e)}")
            
            # If it's not a model availability issue, return the error
            if "quota" in error_str or "resource_exhausted" in error_str:
                return "⚠️ API rate limit reached. Please wait a minute and try again."
            elif "api" in error_str and "key" in error_str:
                return f"⚠️ API Key Error: {str(e)}"
            
            # Otherwise, try the next model
            continue
    
    return "⚠️ All models failed. Please check your API key and internet connection."

# PDF Generation
def generate_pdf(data):
    """Generate ATS-friendly resume PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Name (Large and Bold)
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(31, 119, 180)
    pdf.cell(0, 10, data['personal'].get('name', 'Your Name').upper(), ln=True, align='C')
    
    # Contact Info
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    contact_parts = [
        data['personal'].get('email', ''),
        data['personal'].get('phone', ''),
        data['personal'].get('location', '')
    ]
    if data['personal'].get('linkedin'):
        contact_parts.insert(2, 'LinkedIn')
    if data['personal'].get('portfolio'):
        contact_parts.insert(-1, 'Portfolio')
    
    contact = " | ".join([p for p in contact_parts if p])
    pdf.cell(0, 5, contact, ln=True, align='C')
    pdf.ln(5)
    
    # Professional Summary
    if data.get('summary'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "PROFESSIONAL SUMMARY", ln=True)
        pdf.set_draw_color(31, 119, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, data['summary'])
        pdf.ln(3)
    
    # Education
    if data.get('education'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "EDUCATION", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)
        
        for edu in data['education']:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 6, f"{edu.get('degree', '')} - {edu.get('field', '')}", ln=True)
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"{edu.get('institution', '')} | {edu.get('year', '')} | CGPA: {edu.get('cgpa', '')}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        pdf.ln(2)
    
    # Skills
    if data.get('skills'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "SKILLS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        skills_text = " - ".join(data['skills'])
        pdf.multi_cell(0, 5, skills_text)
        pdf.ln(3)
    
    # Work Experience
    if data.get('experience'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "WORK EXPERIENCE", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experience']:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 6, f"{exp.get('title', '')} | {exp.get('company', '')}", ln=True)
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"{exp.get('duration', '')} | {exp.get('location', '')}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=11)
            
            if exp.get('responsibilities'):
                for line in exp['responsibilities'].split('\n'):
                    line = line.strip()
                    if line:
                        # Add bullet point
                        pdf.cell(10, 5, "-")  # Dash instead of bullet
                        pdf.multi_cell(0, 5, line)
            pdf.ln(2)
        pdf.ln(2)
    
    # Projects
    if data.get('projects'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "PROJECTS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)
        
        for proj in data['projects']:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 6, f"{proj.get('title', '')} | {proj.get('duration', '')}", ln=True)
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"Technologies: {proj.get('technologies', '')}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=11)
            
            if proj.get('description'):
                pdf.multi_cell(0, 5, proj['description'])
            pdf.ln(2)
        pdf.ln(2)
    
    # Certifications
    if data.get('certifications'):
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(31, 119, 180)
        pdf.cell(0, 6, "CERTIFICATIONS & ACHIEVEMENTS", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)
        
        for cert in data['certifications']:
            pdf.cell(10, 5, "-")  # Dash instead of bullet
            pdf.multi_cell(0, 5, cert)
    
    return pdf.output(dest='S').encode('latin-1')

# Main Application
def main():
    # Header
    st.markdown('<div class="main-header">🎯 SmartResume AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Build Your Professional Resume with AI in Minutes</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=80)
        st.title("📋 Navigation")
        
        st.markdown("---")
        st.markdown("### ✨ Features")
        st.markdown("""
        - 🤖 AI-Powered Content
        - 📊 ATS-Friendly Format
        - ⚡ Instant PDF Download
        - 🎨 Professional Design
        - 🔄 Real-Time Preview
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        1. Fill in your details
        2. Use AI enhancement
        3. Review the preview
        4. Download PDF
        """)
        
        st.markdown("---")
        if not GEMINI_API_KEY:
            st.warning("⚠️ AI features disabled. Configure .env file with your Gemini API key.")
        else:
            st.success("✅ AI features enabled!")
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">📝 Resume Information</div>', unsafe_allow_html=True)
        
        # Personal Information
        with st.expander("👤 Personal Information", expanded=True):
            name = st.text_input("Full Name *", 
                               value=st.session_state.resume_data['personal'].get('name', ''),
                               placeholder="John Doe")
            email = st.text_input("Email *", 
                                value=st.session_state.resume_data['personal'].get('email', ''),
                                placeholder="john.doe@email.com")
            phone = st.text_input("Phone Number *", 
                                value=st.session_state.resume_data['personal'].get('phone', ''),
                                placeholder="+91-9876543210")
            linkedin = st.text_input("LinkedIn URL", 
                                   value=st.session_state.resume_data['personal'].get('linkedin', ''),
                                   placeholder="https://linkedin.com/in/johndoe")
            portfolio = st.text_input("Portfolio/Website", 
                                    value=st.session_state.resume_data['personal'].get('portfolio', ''),
                                    placeholder="https://yourportfolio.com")
            location = st.text_input("Location *", 
                                   value=st.session_state.resume_data['personal'].get('location', ''),
                                   placeholder="Bangalore, India")
            
            st.session_state.resume_data['personal'] = {
                'name': name, 'email': email, 'phone': phone,
                'linkedin': linkedin, 'portfolio': portfolio, 'location': location
            }
        
        # Professional Summary
        with st.expander("💼 Professional Summary", expanded=True):
            target_role = st.text_input("Target Job Role", 
                                       placeholder="e.g., Software Engineer, Data Analyst")
            experience_years = st.number_input("Years of Experience", 
                                             min_value=0, max_value=50, value=0)
            key_skills_input = st.text_input("Key Skills (comma-separated)", 
                                            placeholder="Python, JavaScript, React, SQL")
            
            col_ai1, col_ai2 = st.columns([1, 1])
            with col_ai1:
                if st.button("🤖 Generate AI Summary", use_container_width=True):
                    if target_role:
                        with st.spinner("🔄 Generating professional summary..."):
                            prompt = f"""Generate a compelling professional summary for a resume:
                            - Name: {name}
                            - Target Role: {target_role}
                            - Experience: {experience_years} years
                            - Key Skills: {key_skills_input}
                            
                            Requirements:
                            1. Write 3-4 lines (50-70 words)
                            2. Professional and confident tone
                            3. Include relevant keywords for ATS
                            4. Focus on value and expertise
                            5. Do not use first-person pronouns
                            
                            Generate only the summary text:"""
                            
                            summary = generate_with_ai(prompt)
                            if not summary.startswith("⚠️"):
                                st.session_state.resume_data['summary'] = summary
                                st.success("✅ Summary generated!")
                                st.rerun()
                            else:
                                st.error(summary)
                    else:
                        st.warning("⚠️ Please enter a target job role first")
            
            summary_text = st.text_area("Professional Summary", 
                                       value=st.session_state.resume_data.get('summary', ''),
                                       height=120,
                                       placeholder="Enter your professional summary or use AI to generate...")
            st.session_state.resume_data['summary'] = summary_text
        
        # Education
        with st.expander("🎓 Education"):
            st.write("**Add Education Entry:**")
            degree = st.selectbox("Degree/Qualification", 
                                ["B.Tech", "M.Tech", "BCA", "MCA", "B.Sc", "M.Sc", 
                                 "MBA", "BBA", "B.Com", "M.Com", "BA", "MA", "PhD", "Other"],
                                key="edu_degree")
            field = st.text_input("Field of Study", 
                                placeholder="Computer Science",
                                key="edu_field")
            institution = st.text_input("Institution Name", 
                                      placeholder="ABC University",
                                      key="edu_inst")
            year = st.text_input("Graduation Year", 
                               placeholder="2024",
                               key="edu_year")
            cgpa = st.text_input("CGPA/Percentage", 
                               placeholder="8.5/10.0 or 85%",
                               key="edu_cgpa")
            
            if st.button("➕ Add Education", use_container_width=True):
                if degree and field and institution:
                    st.session_state.resume_data['education'].append({
                        'degree': degree, 'field': field, 'institution': institution,
                        'year': year, 'cgpa': cgpa
                    })
                    st.success("✅ Education added!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in degree, field, and institution")
            
            # Display added education
            if st.session_state.resume_data['education']:
                st.write("**Added Education:**")
                for idx, edu in enumerate(st.session_state.resume_data['education']):
                    col_e1, col_e2 = st.columns([4, 1])
                    with col_e1:
                        st.write(f"• {edu['degree']} in {edu['field']} - {edu['institution']}")
                    with col_e2:
                        if st.button("🗑️", key=f"del_edu_{idx}"):
                            st.session_state.resume_data['education'].pop(idx)
                            st.rerun()
        
        # Skills
        with st.expander("💡 Skills"):
            new_skill = st.text_input("Add a skill", 
                                    placeholder="Python, JavaScript, React...",
                                    key="new_skill")
            
            col_s1, col_s2 = st.columns([1, 1])
            with col_s1:
                if st.button("➕ Add Skill", use_container_width=True):
                    if new_skill:
                        skills = [s.strip() for s in new_skill.split(',')]
                        for skill in skills:
                            if skill and skill not in st.session_state.resume_data['skills']:
                                st.session_state.resume_data['skills'].append(skill)
                        st.success(f"✅ Added {len(skills)} skill(s)!")
                        st.rerun()
            
            with col_s2:
                if st.button("🤖 Suggest Skills", use_container_width=True):
                    if target_role:
                        with st.spinner("🔄 Suggesting relevant skills..."):
                            current_skills = ", ".join(st.session_state.resume_data['skills'])
                            prompt = f"""Suggest 5-8 relevant skills for a {target_role} position.
                            
                            Current skills: {current_skills}
                            
                            Suggest additional technical and professional skills that would be valuable.
                            Return only skill names, comma-separated, no explanations:"""
                            
                            suggestions = generate_with_ai(prompt)
                            if not suggestions.startswith("⚠️"):
                                st.info(f"💡 Suggested: {suggestions}")
                            else:
                                st.error(suggestions)
                    else:
                        st.warning("⚠️ Please enter a target job role first")
            
            # Display skills
            if st.session_state.resume_data['skills']:
                st.write("**Current Skills:**")
                st.write(", ".join(st.session_state.resume_data['skills']))
                if st.button("🗑️ Clear All Skills"):
                    st.session_state.resume_data['skills'] = []
                    st.rerun()
        
        # Work Experience
        with st.expander("💼 Work Experience"):
            st.write("**Add Work Experience:**")
            exp_title = st.text_input("Job Title", 
                                    placeholder="Software Engineer",
                                    key="exp_title")
            exp_company = st.text_input("Company Name", 
                                      placeholder="ABC Technologies",
                                      key="exp_company")
            exp_duration = st.text_input("Duration", 
                                       placeholder="Jan 2022 - Present",
                                       key="exp_duration")
            exp_location = st.text_input("Location", 
                                       placeholder="Bangalore, India",
                                       key="exp_location")
            exp_resp = st.text_area("Responsibilities (basic description)", 
                                  height=100,
                                  placeholder="Describe your key responsibilities and achievements...",
                                  key="exp_resp")
            
            col_exp1, col_exp2 = st.columns([1, 1])
            with col_exp1:
                if st.button("🤖 Generate Bullet Points", use_container_width=True):
                    if exp_title and exp_resp:
                        with st.spinner("🔄 Generating professional bullet points..."):
                            prompt = f"""Transform these job responsibilities into 3-5 professional bullet points:
                            
                            Job Title: {exp_title}
                            Company: {exp_company}
                            Responsibilities: {exp_resp}
                            
                            Requirements:
                            1. Start with strong action verbs (Led, Developed, Implemented, etc.)
                            2. Include quantifiable metrics where possible
                            3. Show impact and results
                            4. Use past tense
                            5. Make each point concise and impactful
                            
                            Generate bullet points (one per line, starting with •):"""
                            
                            bullets = generate_with_ai(prompt)
                            if not bullets.startswith("⚠️"):
                                st.session_state.exp_bullets = bullets
                                st.success("✅ Bullet points generated! Review below.")
                                st.rerun()
                            else:
                                st.error(bullets)
                    else:
                        st.warning("⚠️ Please enter job title and responsibilities first")
            
            # Show generated bullets if available
            if hasattr(st.session_state, 'exp_bullets'):
                exp_resp_enhanced = st.text_area("Enhanced Responsibilities (Edit if needed)", 
                                               value=st.session_state.exp_bullets, 
                                               height=150, 
                                               key="exp_resp_edit")
            else:
                exp_resp_enhanced = exp_resp
            
            with col_exp2:
                if st.button("➕ Add Experience", use_container_width=True):
                    if exp_title and exp_company:
                        st.session_state.resume_data['experience'].append({
                            'title': exp_title, 
                            'company': exp_company,
                            'duration': exp_duration, 
                            'location': exp_location,
                            'responsibilities': exp_resp_enhanced
                        })
                        # Clear generated bullets
                        if hasattr(st.session_state, 'exp_bullets'):
                            delattr(st.session_state, 'exp_bullets')
                        st.success("✅ Experience added!")
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in job title and company")
            
            # Display added experiences
            if st.session_state.resume_data['experience']:
                st.write("**Added Experiences:**")
                for idx, exp in enumerate(st.session_state.resume_data['experience']):
                    col_ex1, col_ex2 = st.columns([4, 1])
                    with col_ex1:
                        st.write(f"• {exp['title']} at {exp['company']}")
                    with col_ex2:
                        if st.button("🗑️", key=f"del_exp_{idx}"):
                            st.session_state.resume_data['experience'].pop(idx)
                            st.rerun()
        
        # Projects
        with st.expander("🚀 Projects"):
            st.write("**Add Project:**")
            proj_title = st.text_input("Project Title", 
                                     placeholder="AI Chatbot Application",
                                     key="proj_title")
            proj_duration = st.text_input("Duration", 
                                        placeholder="Jan 2023 - Mar 2023",
                                        key="proj_duration")
            proj_tech = st.text_input("Technologies Used", 
                                    placeholder="Python, TensorFlow, React",
                                    key="proj_tech")
            proj_desc = st.text_area("Description", 
                                   height=100,
                                   placeholder="Describe what the project does and your role...",
                                   key="proj_desc")
            
            col_p1, col_p2 = st.columns([1, 1])
            with col_p1:
                if st.button("🤖 Enhance Description", use_container_width=True):
                    if proj_title and proj_desc:
                        with st.spinner("🔄 Enhancing project description..."):
                            prompt = f"""Enhance this project description for a resume:
                            
                            Title: {proj_title}
                            Technologies: {proj_tech}
                            Description: {proj_desc}
                            
                            Create a professional 2-3 line description (40-60 words) that:
                            1. Clearly explains the project purpose
                            2. Highlights technical complexity
                            3. Mentions key technologies
                            4. Shows impact or results
                            
                            Generate only the enhanced description:"""
                            
                            enhanced = generate_with_ai(prompt)
                            if not enhanced.startswith("⚠️"):
                                st.session_state.proj_enhanced = enhanced
                                st.success("✅ Description enhanced! Review below.")
                                st.rerun()
                            else:
                                st.error(enhanced)
                    else:
                        st.warning("⚠️ Please enter project title and description first")
            
            # Show enhanced description if available
            if hasattr(st.session_state, 'proj_enhanced'):
                proj_desc_final = st.text_area("Enhanced Description (Edit if needed)", 
                                             value=st.session_state.proj_enhanced,
                                             height=100, 
                                             key="proj_desc_edit")
            else:
                proj_desc_final = proj_desc
            
            with col_p2:
                if st.button("➕ Add Project", use_container_width=True):
                    if proj_title:
                        st.session_state.resume_data['projects'].append({
                            'title': proj_title, 
                            'duration': proj_duration,
                            'technologies': proj_tech, 
                            'description': proj_desc_final
                        })
                        # Clear enhanced description
                        if hasattr(st.session_state, 'proj_enhanced'):
                            delattr(st.session_state, 'proj_enhanced')
                        st.success("✅ Project added!")
                        st.rerun()
                    else:
                        st.error("⚠️ Please enter project title")
            
            # Display added projects
            if st.session_state.resume_data['projects']:
                st.write("**Added Projects:**")
                for idx, proj in enumerate(st.session_state.resume_data['projects']):
                    col_pr1, col_pr2 = st.columns([4, 1])
                    with col_pr1:
                        st.write(f"• {proj['title']}")
                    with col_pr2:
                        if st.button("🗑️", key=f"del_proj_{idx}"):
                            st.session_state.resume_data['projects'].pop(idx)
                            st.rerun()
        
        # Certifications
        with st.expander("🏆 Certifications & Achievements"):
            cert = st.text_input("Add certification or achievement", 
                               placeholder="AWS Certified Solutions Architect (2023)",
                               key="new_cert")
            if st.button("➕ Add Certification", use_container_width=True):
                if cert:
                    st.session_state.resume_data['certifications'].append(cert)
                    st.success("✅ Certification added!")
                    st.rerun()
            
            # Display certifications
            if st.session_state.resume_data['certifications']:
                st.write("**Added Certifications:**")
                for idx, c in enumerate(st.session_state.resume_data['certifications']):
                    col_c1, col_c2 = st.columns([4, 1])
                    with col_c1:
                        st.write(f"• {c}")
                    with col_c2:
                        if st.button("🗑️", key=f"del_cert_{idx}"):
                            st.session_state.resume_data['certifications'].pop(idx)
                            st.rerun()
    
    # Preview Column
    with col2:
        st.markdown('<div class="section-header">👁️ Live Preview</div>', unsafe_allow_html=True)
        
        data = st.session_state.resume_data
        
        # Resume Preview
        st.markdown('<div class="preview-box">', unsafe_allow_html=True)
        
        # Name and Contact
        st.markdown(f'<div class="resume-name">{data["personal"].get("name", "Your Name")}</div>', 
                   unsafe_allow_html=True)
        
        contact_parts = [
            data["personal"].get("email", ""),
            data["personal"].get("phone", ""),
            data["personal"].get("location", "")
        ]
        if data["personal"].get("linkedin"):
            contact_parts.insert(2, 'LinkedIn')
        if data["personal"].get("portfolio"):
            contact_parts.insert(-1, 'Portfolio')
        
        contact_text = " | ".join([p for p in contact_parts if p])
        st.markdown(f'<div class="resume-contact">{contact_text}</div>', unsafe_allow_html=True)
        
        # Professional Summary
        if data.get('summary'):
            st.markdown('<div class="resume-section-title">PROFESSIONAL SUMMARY</div>', 
                       unsafe_allow_html=True)
            st.write(data['summary'])
        
        # Education
        if data.get('education'):
            st.markdown('<div class="resume-section-title">EDUCATION</div>', unsafe_allow_html=True)
            for edu in data['education']:
                st.markdown(f"**{edu.get('degree', '')} - {edu.get('field', '')}**")
                st.write(f"*{edu.get('institution', '')} | {edu.get('year', '')} | CGPA: {edu.get('cgpa', '')}*")
                st.write("")
        
        # Skills
        if data.get('skills'):
            st.markdown('<div class="resume-section-title">SKILLS</div>', unsafe_allow_html=True)
            st.write(" • ".join(data['skills']))
        
        # Work Experience
        if data.get('experience'):
            st.markdown('<div class="resume-section-title">WORK EXPERIENCE</div>', unsafe_allow_html=True)
            for exp in data['experience']:
                st.markdown(f"**{exp.get('title', '')} | {exp.get('company', '')}**")
                st.write(f"*{exp.get('duration', '')} | {exp.get('location', '')}*")
                if exp.get('responsibilities'):
                    for line in exp['responsibilities'].split('\n'):
                        line = line.strip()
                        if line and not line.startswith('•'):
                            st.write(f"• {line}")
                        elif line:
                            st.write(line)
                st.write("")
        
        # Projects
        if data.get('projects'):
            st.markdown('<div class="resume-section-title">PROJECTS</div>', unsafe_allow_html=True)
            for proj in data['projects']:
                st.markdown(f"**{proj.get('title', '')} | {proj.get('duration', '')}**")
                st.write(f"*Technologies: {proj.get('technologies', '')}*")
                st.write(proj.get('description', ''))
                st.write("")
        
        # Certifications
        if data.get('certifications'):
            st.markdown('<div class="resume-section-title">CERTIFICATIONS & ACHIEVEMENTS</div>', 
                       unsafe_allow_html=True)
            for cert in data['certifications']:
                st.write(f"• {cert}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Button
        st.markdown("---")
        if st.button("📥 Download PDF Resume", use_container_width=True, type="primary"):
            if not data['personal'].get('name') or not data['personal'].get('email'):
                st.error("⚠️ Please fill in at least Name and Email to generate PDF")
            else:
                try:
                    with st.spinner("🔄 Generating your professional resume..."):
                        pdf_bytes = generate_pdf(data)
                        filename = f"{data['personal'].get('name', 'Resume').replace(' ', '_')}_Resume.pdf"
                        
                        st.download_button(
                            label="💾 Click Here to Download PDF",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.markdown('<div class="success-box">✅ <strong>Resume generated successfully!</strong> Click the button above to download.</div>', 
                                   unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Error generating PDF: {str(e)}")

if __name__ == "__main__":
    main()
