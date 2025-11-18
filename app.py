"""
SmartResume AI - AI-Powered Resume Builder
Main Streamlit Application
"""

import streamlit as st
import os
from components.form_sections import (
    render_personal_info_form,
    render_professional_summary_form,
    render_education_form,
    render_skills_form,
    render_experience_form,
    render_projects_form,
    render_certifications_form
)
from components.ai_generator import AIGenerator, render_ai_buttons, handle_ai_generation, handle_ai_generation_pre_render
from components.preview import render_resume_preview, render_empty_preview
from components.pdf_exporter import create_download_button, create_cover_letter_download_button
from components.cover_letter_form import (
    render_cover_letter_personal_info,
    render_cover_letter_form,
    render_cover_letter_content,
    render_cover_letter_preview,
    render_cover_letter_actions
)
from components.cover_letter_generator import (
    render_cover_letter_generator,
    handle_cover_letter_generation_pre_render
)
from components.resume_manager import (
    handle_resume_load_pre_render,
    render_save_resume_section,
    render_load_resume_section,
    render_export_import_section,
    render_resume_selector_for_cover_letter,
    render_save_cover_letter_section
)

# Page configuration
st.set_page_config(
    page_title="SmartResume AI - AI-Powered Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/UtkarshSrivastava1139/SmartResume',
        'Report a bug': 'https://github.com/UtkarshSrivastava1139/SmartResume/issues',
        'About': '# SmartResume AI\nAI-Powered Resume & Cover Letter Builder with Google Gemini'
    }
)

# Load custom CSS
def load_custom_css():
    """Load custom CSS styling based on theme"""
    theme = st.session_state.get('theme', 'light')
    css_filename = 'dark.css' if theme == 'dark' else 'custom.css'
    css_file = os.path.join(os.path.dirname(__file__), 'assets', 'styles', css_filename)
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_custom_css()

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.theme = 'light'  # Default theme
        st.session_state.name = ''
        st.session_state.email = ''
        st.session_state.phone = ''
        st.session_state.linkedin = ''
        st.session_state.location = ''
        st.session_state.portfolio = ''
        st.session_state.target_role = ''
        st.session_state.experience_years = 0
        st.session_state.summary = ''
        st.session_state.education_list = []
        st.session_state.technical_skills = ''
        st.session_state.soft_skills = ''
        st.session_state.experience_list = []
        st.session_state.projects_list = []
        st.session_state.certifications = ''
        
        # Cover Letter fields
        st.session_state.cl_job_title = ''
        st.session_state.cl_company = ''
        st.session_state.cl_job_description = ''
        st.session_state.cl_additional_notes = ''
        st.session_state.cover_letter_content = ''

initialize_session_state()

# Initialize AI Generator
@st.cache_resource
def get_ai_generator():
    """Get cached AI generator instance"""
    return AIGenerator()

# Main App
def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: #1f77b4; margin-bottom: 0.5rem;'>SmartResume AI</h1>
        <p style='color: #666; font-size: 1.1rem;'>Build Your Professional Resume with AI in Minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=60)
        st.markdown("### Navigation")
        
        page = st.radio(
            "Go to:",
            ["Home", "Build Resume", "Cover Letter", "About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Theme Toggle
        current_theme = st.session_state.get('theme', 'light')
        theme_label = "🌙 Dark Mode" if current_theme == 'light' else "☀️ Light Mode"
        
        if st.button(theme_label, use_container_width=True):
            st.session_state.theme = 'dark' if current_theme == 'light' else 'light'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("""
        - AI-Powered Content
        - ATS-Friendly Format
        - Instant PDF Download
        - Professional Templates
        - Real-Time Preview
        """)
        
        st.markdown("---")
        st.markdown("### Tips")
        st.markdown("""
        1. Fill in all sections
        2. Use AI to enhance content
        3. Review the preview
        4. Download your resume
        """)
        
        st.markdown("---")
        st.info("**Tip**: Use the AI enhancement features to create professional, ATS-optimized content!")
        
        # Show AI Provider at bottom of sidebar
        try:
            ai_gen = get_ai_generator()
            if ai_gen and ai_gen.client:
                provider = ai_gen.client.get_provider_name()
                st.caption(f"🤖 AI Provider: **{provider}**")
        except:
            pass
    
    # Pages
    if page == "Home":
        render_home_page()
    elif page == "Build Resume":
        render_builder_page()
    elif page == "Cover Letter":
        render_cover_letter_page()
    else:
        render_about_page()

def render_home_page():
    """Render home page"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### AI-Powered
        Let Google's Gemini AI write professional resume content for you
        """)
    
    with col2:
        st.markdown("""
        ### Lightning Fast
        Create a complete resume in just 10 minutes
        """)
    
    with col3:
        st.markdown("""
        ### ATS-Friendly
        Optimized to pass Applicant Tracking Systems
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ## Why Choose SmartResume AI?
    
    Creating an effective resume is challenging. **SmartResume AI** solves common problems:
    
    - **Writer's Block?** AI generates compelling content from basic inputs
    - **ATS Rejection?** Our format is optimized for tracking systems
    - **Time-Consuming?** Create professional resumes in minutes, not hours
    - **Lack of Expertise?** AI knows what recruiters want to see
    - **Missing Keywords?** AI suggests relevant skills and optimizes content
    
    ## How It Works
    
    1. **Fill the Form** - Enter your basic information
    2. **AI Enhancement** - Click AI buttons to generate professional content
    3. **Real-Time Preview** - See your resume as you build it
    4. **Download PDF** - Get your ATS-friendly resume instantly
    
    ## Get Started
    
    Ready to build your resume? Click **"Build Resume"** in the sidebar to start!
    """)
    
    if st.button("Start Building Now", use_container_width=True, type="primary"):
        st.session_state.page = "Build Resume"
        st.rerun()

def render_builder_page():
    """Render resume builder page"""
    
    # Get cached AI Generator instance
    ai_generator = get_ai_generator()
    
    # Handle resume loading BEFORE rendering widgets
    handle_resume_load_pre_render()
    
    # Handle any pending AI generation BEFORE rendering widgets
    handle_ai_generation_pre_render(ai_generator)
    
    # Check if API key is configured
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not gemini_key and not openrouter_key:
        st.warning("""
        **AI API Key Not Configured**
        
        To use AI features, configure one of these options:
        
        **Option 1 - Google Gemini (Recommended):**
        1. Get your free API key from https://aistudio.google.com/app/apikey
        2. Add to `.env` file: `GEMINI_API_KEY=your_api_key_here`
        
        **Option 2 - OpenRouter (Free Models Available):**
        1. Get your API key from https://openrouter.ai/keys
        2. Add to `.env` file: `OPENROUTER_API_KEY=your_api_key_here`
        
        You can still use the app, but AI features will be disabled.
        """)
    
    # Create two-column layout
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("### Resume Information")
        
        # Personal Information
        personal_data = render_personal_info_form()
        st.markdown("---")
        
        # Professional Summary
        summary_data = render_professional_summary_form()
        st.markdown("---")
        
        # Education
        education_data = render_education_form()
        st.markdown("---")
        
        # Skills
        skills_data = render_skills_form()
        st.markdown("---")
        
        # Work Experience
        experience_data = render_experience_form()
        st.markdown("---")
        
        # Projects
        projects_data = render_projects_form()
        st.markdown("---")
        
        # Certifications
        certifications_data = render_certifications_form()
        st.markdown("---")
        
        # AI Enhancement Buttons (use same ai_generator instance)
        ai_buttons = render_ai_buttons()
        
        # Collect all resume data
        resume_data = {
            **personal_data,
            **summary_data,
            **skills_data,
            'education_list': education_data,
            'experience_list': experience_data,
            'projects_list': projects_data,
            'certifications': certifications_data
        }
        
        # Update save section with resume data
        with st.expander("💾 Save & Load Resume", expanded=False):
            tab1, tab2, tab3 = st.tabs(["Save", "Load", "Export/Import"])
            
            with tab1:
                render_save_resume_section(resume_data)
            
            with tab2:
                render_load_resume_section()
            
            with tab3:
                render_export_import_section()
        
        # Handle AI generation
        handle_ai_generation(ai_buttons, ai_generator, resume_data)
        
        st.markdown("---")
        
        # Download PDF Button
        st.markdown("### Download Your Resume")
        
        if st.button("Generate & Download PDF", use_container_width=True, type="primary"):
            if not resume_data.get('name') or not resume_data.get('email'):
                st.error("Please fill in at least Name and Email to generate PDF")
            else:
                with st.spinner("Generating PDF..."):
                    pdf_bytes, filename = create_download_button(resume_data)
                    
                    if pdf_bytes:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("Resume PDF generated successfully!")
    
    with col_preview:
        st.markdown("### Live Preview")
        
        # Show preview if there's data
        if resume_data.get('name'):
            render_resume_preview(resume_data)
        else:
            render_empty_preview()

def render_cover_letter_page():
    """Render cover letter generator page"""
    
    # Handle any pending AI generation BEFORE rendering widgets
    handle_cover_letter_generation_pre_render()
    
    # Check if API key is configured
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not gemini_key and not openrouter_key:
        st.warning("""
        **AI API Key Not Configured**
        
        To use AI features, configure one of these options:
        
        **Option 1 - Google Gemini (Recommended):**
        1. Get your free API key from https://aistudio.google.com/app/apikey
        2. Add to `.env` file: `GEMINI_API_KEY=your_api_key_here`
        
        **Option 2 - OpenRouter (Free Models Available):**
        1. Get your API key from https://openrouter.ai/keys
        2. Add to `.env` file: `OPENROUTER_API_KEY=your_api_key_here`
        
        You can still enter cover letter manually, but AI generation will be disabled.
        """)
    
    st.markdown("---")
    st.markdown("## Cover Letter Generator")
    st.caption("Create a professional, ATS-optimized cover letter tailored to your target role")
    
    # Resume Linking Section
    with st.expander("🔗 Link to Resume (Recommended)", expanded=True):
        st.info("📋 Link this cover letter to a saved resume for AI to use your skills, experience, and achievements!")
        render_resume_selector_for_cover_letter()
        
        if st.session_state.get('cl_linked_resume_name'):
            st.success(f"✅ Linked to resume: **{st.session_state['cl_linked_resume_name']}**")
    
    st.markdown("---")
    
    # Personal Information Section (at top)
    render_cover_letter_personal_info()
    
    st.markdown("---")
    
    # Two-column layout
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Form section
        render_cover_letter_form()
        
        st.markdown("---")
        
        # AI Generation button
        render_cover_letter_generator()
        
        st.markdown("---")
        
        # Content editor
        render_cover_letter_content()
        
        st.markdown("---")
        
        # Save cover letter section
        render_save_cover_letter_section()
    
    with col_right:
        # Preview section
        render_cover_letter_preview()
    
    # Actions at bottom (full width)
    st.markdown("---")
    
    # Handle PDF download button
    if st.session_state.get('download_cover_letter_pdf_btn'):
        name = st.session_state.get('name', '')
        email = st.session_state.get('email', '')
        phone = st.session_state.get('phone', '')
        location = st.session_state.get('location', '')
        company = st.session_state.get('cl_company', 'Company')
        job_title = st.session_state.get('cl_job_title', 'Position')
        cover_letter_content = st.session_state.get('cover_letter_content', '')
        
        if not name or not cover_letter_content:
            st.error("Please ensure your Name is filled and cover letter is generated before downloading PDF.")
        else:
            with st.spinner("Generating PDF..."):
                pdf_bytes, filename = create_cover_letter_download_button(
                    name=name,
                    email=email,
                    phone=phone,
                    location=location,
                    company=company,
                    job_title=job_title,
                    cover_letter_content=cover_letter_content
                )
                
                if pdf_bytes:
                    st.download_button(
                        label="Download Cover Letter PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("Cover letter PDF generated successfully!")
    
    render_cover_letter_actions()

def render_about_page():
    """Render about page"""
    st.markdown("---")
    
    st.markdown("""
    ## About SmartResume AI
    
    **SmartResume AI** is an innovative web-based resume builder that leverages Google's Gemini AI 
    to automatically generate professional, ATS-friendly resume content from basic user inputs.
    
    ### Technology Stack
    
    - **Frontend**: Streamlit (Python web framework)
    - **AI Engine**: Google Gemini API
    - **PDF Generation**: FPDF2
    - **Language**: Python 3.10+
    
    ### Key Features
    
    #### 1. AI Content Generation
    - Professional summary generation
    - Experience bullet points enhancement
    - Project description improvement
    - Skills suggestion based on target role
    
    #### 2. ATS Optimization
    - Clean, parseable format
    - Standard section headings
    - No complex graphics or tables
    - Proper font and spacing
    
    #### 3. User-Friendly Interface
    - Simple, intuitive forms
    - Real-time preview
    - One-click PDF download
    - Mobile-responsive design
    
    ### How AI Helps
    
    Our AI integration helps you:
    
    - **Write Better**: Transform basic descriptions into compelling, professional content
    - **Save Time**: Generate content in seconds instead of hours
    - **Optimize Keywords**: Include relevant skills and industry terms
    - **Show Impact**: Create achievement-focused bullet points
    - **Stay Professional**: Maintain consistent tone and style
    
    ### Privacy & Security
    
    - No data is stored on our servers
    - All processing happens in your session
    - API calls are secure and encrypted
    - You own all generated content
    
    ### Getting Help
    
    For issues or questions:
    
    1. Check the sidebar tips
    2. Review the form validation messages
    3. Ensure your API key is configured correctly
    4. Try refreshing the page if issues persist
    
    ### Credits
    
    - Powered by Google Gemini AI
    - Built with Streamlit
    - Icons from Icons8
    
    ### Version
    
    **Version 1.0.0** - Academic Project
    
    ---
    
    Made with for job seekers everywhere
    """)

if __name__ == "__main__":
    main()
