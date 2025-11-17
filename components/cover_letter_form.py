"""
Cover Letter Form Component for SmartResume AI
Renders the cover letter input form with all required fields
"""

import streamlit as st


def render_cover_letter_personal_info():
    """
    Render quick personal information section for cover letter
    Uses same session state as resume builder for consistency
    """
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input(
            "Full Name *",
            value=st.session_state.get('name', ''),
            key='name',
            placeholder="John Doe"
        )
        
        phone = st.text_input(
            "Phone Number",
            value=st.session_state.get('phone', ''),
            key='phone',
            placeholder="(123) 456-7890"
        )
    
    with col2:
        email = st.text_input(
            "Email Address *",
            value=st.session_state.get('email', ''),
            key='email',
            placeholder="john.doe@email.com"
        )
        
        location = st.text_input(
            "Location",
            value=st.session_state.get('location', ''),
            key='location',
            placeholder="City, State"
        )


def render_cover_letter_form():
    """
    Render the cover letter input form
    Stores all inputs in session state with 'cl_' prefix to avoid conflicts
    """
    st.subheader("Cover Letter Details")
    
    # Job Title (Required)
    job_title = st.text_input(
        "Target Job Title *",
        value=st.session_state.get('cl_job_title', st.session_state.get('target_role', '')),
        key='cl_job_title',
        placeholder="e.g., Senior Software Engineer, Marketing Manager",
        help="The job position you're applying for"
    )
    
    # Company Name (Optional)
    company = st.text_input(
        "Company Name",
        value=st.session_state.get('cl_company', ''),
        key='cl_company',
        placeholder="e.g., Google, Microsoft, Startup Inc.",
        help="Leave blank if applying to multiple companies"
    )
    
    # Job Description (Optional but recommended)
    st.markdown("#### Job Description (Optional)")
    st.caption("Paste the job posting here for better AI customization. The more details you provide, the better the cover letter will be tailored.")
    
    job_description = st.text_area(
        "Job Description",
        value=st.session_state.get('cl_job_description', ''),
        key='cl_job_description',
        height=150,
        placeholder="Paste the job description here, or leave blank for a general cover letter...",
        label_visibility="collapsed"
    )
    
    # Additional Notes (Optional)
    st.markdown("#### Additional Notes (Optional)")
    st.caption("Add any specific points you want to highlight or context about why you're interested in this role.")
    
    additional_notes = st.text_area(
        "Additional Notes",
        value=st.session_state.get('cl_additional_notes', ''),
        key='cl_additional_notes',
        height=100,
        placeholder="e.g., Referred by John Doe, Passionate about the company's mission, Relocating to the area...",
        label_visibility="collapsed"
    )
    
    # Info box about data sources
    with st.expander("Where does the AI get information from?"):
        st.info("""
        The AI will use information from:
        - **Your Name & Contact**: From Personal Information section above
        - **Skills**: From your resume Skills section (if filled in Resume Builder)
        - **Professional Summary**: From your resume Summary section (if filled in Resume Builder)
        - **Job Details**: From the fields in this section
        
        **Tip**: For best results, fill out your resume in the "Build Resume" tab first, 
        or at minimum fill in your personal information above!
        """)


def render_cover_letter_content():
    """
    Render the generated cover letter content area
    Allows editing and displays the current draft
    """
    st.subheader("Your Cover Letter")
    
    # Initialize cover letter content if not exists
    if 'cover_letter_content' not in st.session_state:
        st.session_state['cover_letter_content'] = ""
    
    # Editable text area for cover letter
    cover_letter = st.text_area(
        "Cover Letter Content",
        value=st.session_state.get('cover_letter_content', ''),
        key='cover_letter_content',
        height=400,
        placeholder="Your AI-generated cover letter will appear here. You can edit it after generation.\n\nClick 'Generate Cover Letter' button above to create your personalized cover letter.",
        help="Edit the generated cover letter as needed. Changes are saved automatically."
    )
    
    # Character count
    if cover_letter:
        word_count = len(cover_letter.split())
        char_count = len(cover_letter)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"Words: {word_count}")
        with col2:
            st.caption(f"Characters: {char_count}")
        with col3:
            # Color code based on recommended length (300-400 words)
            if 250 <= word_count <= 450:
                st.caption("✓ Good length")
            elif word_count < 250:
                st.caption("⚠ Consider adding more detail")
            else:
                st.caption("⚠ Consider being more concise")


def render_cover_letter_preview():
    """
    Render a formatted preview of the cover letter
    Shows how it will appear in the final document
    """
    st.subheader("Preview")
    
    cover_letter = st.session_state.get('cover_letter_content', '')
    
    if not cover_letter:
        st.info("Generate a cover letter to see the preview here.")
        return
    
    # Get personal info for header
    name = st.session_state.get('name', 'Your Name')
    email = st.session_state.get('email', 'your.email@example.com')
    phone = st.session_state.get('phone', '(123) 456-7890')
    location = st.session_state.get('location', '')
    
    # Today's date
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    
    # Company and job info
    company = st.session_state.get('cl_company', '[Company Name]')
    job_title = st.session_state.get('cl_job_title', '[Job Title]')
    
    # Escape HTML in user content to prevent injection
    import html
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_phone = html.escape(phone)
    safe_location = html.escape(location) if location else ''
    safe_company = html.escape(company)
    safe_job_title = html.escape(job_title)
    safe_cover_letter = html.escape(cover_letter)
    
    # Build contact line
    contact_parts = [safe_email, safe_phone]
    if safe_location:
        contact_parts.append(safe_location)
    contact_line = " | ".join(contact_parts)
    
    # Render preview
    with st.container():
        st.markdown(f"""
        <div style='border: 1px solid #ddd; padding: 20px; background-color: white; color: black;'>
            <div style='text-align: right; margin-bottom: 20px;'>
                <strong>{safe_name}</strong><br>
                {contact_line}
            </div>
            
            <div style='margin-bottom: 20px;'>
                {today}
            </div>
            
            <div style='margin-bottom: 20px;'>
                Hiring Manager<br>
                {safe_company}<br>
            </div>
            
            <div style='margin-bottom: 20px;'>
                <strong>Re: Application for {safe_job_title}</strong>
            </div>
            
            <div style='margin-bottom: 20px;'>
                Dear Hiring Manager,
            </div>
            
            <div style='white-space: pre-wrap; line-height: 1.6;'>
{safe_cover_letter}
            </div>
            
            <div style='margin-top: 20px;'>
                Sincerely,<br>
                {safe_name}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_cover_letter_actions():
    """
    Render action buttons for download and clear
    """
    st.subheader("Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download as TXT button
        if st.session_state.get('cover_letter_content'):
            cover_letter = st.session_state['cover_letter_content']
            name = st.session_state.get('name', 'User')
            job_title = st.session_state.get('cl_job_title', 'Position')
            
            # Create filename
            filename = f"CoverLetter_{name.replace(' ', '_')}_{job_title.replace(' ', '_')}.txt"
            
            st.download_button(
                label="Download as TXT",
                data=cover_letter,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        # Download as PDF button (will be implemented)
        if st.session_state.get('cover_letter_content'):
            st.button(
                "Download as PDF",
                use_container_width=True,
                disabled=False,
                key='download_cover_letter_pdf_btn'
            )
    
    with col3:
        # Clear button
        if st.session_state.get('cover_letter_content'):
            if st.button("Clear Cover Letter", use_container_width=True, type="secondary"):
                st.session_state['cover_letter_content'] = ""
                st.session_state['cl_job_title'] = ""
                st.session_state['cl_company'] = ""
                st.session_state['cl_job_description'] = ""
                st.session_state['cl_additional_notes'] = ""
                st.rerun()


