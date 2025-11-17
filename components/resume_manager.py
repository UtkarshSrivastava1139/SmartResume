"""
Resume Management UI Components
Save, load, and manage resumes locally
"""

import streamlit as st
from utils.storage import LocalStorage
from datetime import datetime
import json


def handle_resume_load_pre_render():
    """
    Handle resume loading BEFORE widgets are rendered
    This prevents session state widget conflicts
    Must be called at the top of render_builder_page()
    """
    if st.session_state.get('_load_resume_pending'):
        # Clear the flag
        st.session_state['_load_resume_pending'] = False
        
        # Get the resume to load
        resume = st.session_state.get('_resume_to_load')
        
        if resume:
            # Load all resume data into session state
            for key, value in resume['data'].items():
                st.session_state[key] = value
            
            # Show success message
            st.success(f"✅ Loaded: {resume['name']}")
            
            # Clear the temporary storage
            if '_resume_to_load' in st.session_state:
                del st.session_state['_resume_to_load']


def render_save_resume_section(resume_data: dict):
    """Render save resume section"""
    st.subheader("💾 Save Resume")
    
    storage = LocalStorage()
    
    # Resume name input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        resume_name = st.text_input(
            "Resume Name",
            placeholder="e.g., Software Engineer Resume - Tech Companies 2024",
            help="Give your resume a memorable name",
            key="save_resume_name"
        )
    
    with col2:
        save_btn = st.button("💾 Save", type="primary", use_container_width=True, key="save_resume_btn")
    
    if save_btn:
        if not resume_name.strip():
            st.error("Please enter a resume name")
        elif not resume_data.get('name'):
            st.error("Please fill in your name in Personal Information")
        else:
            if storage.save_resume(resume_name, resume_data):
                st.success(f"✅ Resume '{resume_name}' saved successfully!")
            else:
                st.error("Failed to save resume")


def render_load_resume_section():
    """Render load resume section"""
    st.subheader("📂 Load Saved Resume")
    
    storage = LocalStorage()
    saved_resumes = storage.get_all_resumes()
    
    if not saved_resumes:
        st.info("📭 No saved resumes yet. Create and save a resume first!")
        return
    
    # Create resume selection options
    resume_options = [
        f"{r['name']} - {r['target_role'] or 'No role'} (Updated: {r['updated_at'][:10]})"
        for r in saved_resumes
    ]
    
    selected = st.selectbox(
        "Select Resume",
        options=resume_options,
        help="Choose a resume to load"
    )
    
    if selected:
        # Extract resume name from selection
        resume_name = selected.split(" - ")[0]
        resume = storage.get_resume(resume_name)
        
        if resume:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if st.button("📥 Load Resume", type="primary", use_container_width=True, key=f"load_resume_{resume_name}"):
                    # Set flag to load resume data (will be processed before widgets render)
                    st.session_state['_load_resume_pending'] = True
                    st.session_state['_resume_to_load'] = resume
                    st.rerun()
            
            with col2:
                if st.button("ℹ️ Details", use_container_width=True, key=f"details_{resume_name}"):
                    with st.expander("Resume Details", expanded=True):
                        st.write(f"**Name:** {resume['name']}")
                        st.write(f"**Target Role:** {resume['target_role']}")
                        st.write(f"**Created:** {resume['created_at'][:10]}")
                        st.write(f"**Updated:** {resume['updated_at'][:10]}")
                        
                        # Show cover letters count
                        cover_letters = storage.get_cover_letters_for_resume(resume['name'])
                        st.write(f"**Cover Letters:** {len(cover_letters)}")
            
            with col3:
                if st.button("🗑️ Delete", type="secondary", use_container_width=True, key=f"delete_{resume_name}"):
                    if st.session_state.get(f'confirm_delete_{resume_name}'):
                        if storage.delete_resume(resume_name):
                            st.success("✅ Resume deleted!")
                            del st.session_state[f'confirm_delete_{resume_name}']
                            st.rerun()
                    else:
                        st.session_state[f'confirm_delete_{resume_name}'] = True
                        st.warning("⚠️ Click Delete again to confirm")


def render_export_import_section():
    """Render export/import data section"""
    st.subheader("📤 Export / Import Data")
    
    storage = LocalStorage()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export All Data**")
        st.caption("Download all your resumes and cover letters as a JSON file")
        
        if st.button("📥 Export to File", use_container_width=True, key="export_data_btn"):
            json_data = storage.export_all_data()
            
            st.download_button(
                label="💾 Download JSON File",
                data=json_data,
                file_name=f"smartresume_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.success("✅ Ready to download!")
    
    with col2:
        st.markdown("**Import Data**")
        st.caption("Upload a previously exported JSON file")
        
        uploaded_file = st.file_uploader(
            "Choose JSON file",
            type=['json'],
            help="Upload a backup file to restore your data",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.read().decode('utf-8')
                if storage.import_data(json_str):
                    st.success("✅ Data imported successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to import data")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")


def render_resume_selector_for_cover_letter():
    """Render resume selector for cover letter generation"""
    storage = LocalStorage()
    saved_resumes = storage.get_all_resumes()
    
    if not saved_resumes:
        st.warning("⚠️ No saved resumes found. Please save a resume first in the 'Build Resume' tab.")
        return None
    
    st.info("📋 Select a resume to use for this cover letter:")
    
    # Create resume selection options
    resume_options = {
        f"{r['name']} - {r['target_role'] or 'No role specified'}": r['name']
        for r in saved_resumes
    }
    
    selected = st.selectbox(
        "Choose Resume",
        options=list(resume_options.keys()),
        help="The cover letter will use information from this resume"
    )
    
    if selected:
        resume_name = resume_options[selected]
        resume = storage.get_resume(resume_name)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.caption(f"✅ Selected: {selected}")
        
        with col2:
            if st.button("📥 Load Data", type="primary", use_container_width=True, key="load_resume_data_for_cl"):
                if resume:
                    # Store linked resume info
                    st.session_state['cl_linked_resume_name'] = resume['name']
                    
                    # Load resume data for cover letter generation
                    resume_data = resume['data']
                    
                    # Store for AI generation
                    st.session_state['cl_resume_data'] = resume_data
                    
                    # Pre-fill personal info
                    st.session_state['name'] = resume_data.get('name', '')
                    st.session_state['email'] = resume_data.get('email', '')
                    st.session_state['phone'] = resume_data.get('phone', '')
                    st.session_state['location'] = resume_data.get('location', '')
                    
                    st.success(f"✅ Loaded data from: {resume['name']}")
                    st.rerun()
        
        return resume_name
    
    return None


def render_save_cover_letter_section():
    """Render save cover letter section"""
    if not st.session_state.get('cover_letter_content'):
        st.info("💡 Generate a cover letter first to save it")
        return
    
    st.subheader("💾 Save Cover Letter")
    
    storage = LocalStorage()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        cover_letter_name = st.text_input(
            "Cover Letter Name",
            placeholder="e.g., Google - Web Developer",
            help="Name this cover letter for easy reference",
            key="save_cover_letter_name"
        )
    
    with col2:
        save_btn = st.button("💾 Save", type="primary", use_container_width=True, key="save_cl_btn")
    
    if save_btn:
        if not cover_letter_name.strip():
            st.error("Please enter a name for the cover letter")
        else:
            resume_name = st.session_state.get('cl_linked_resume_name', 'Unlinked')
            company = st.session_state.get('cl_company', '')
            job_title = st.session_state.get('cl_job_title', '')
            content = st.session_state.get('cover_letter_content', '')
            
            if storage.save_cover_letter(cover_letter_name, resume_name, company, job_title, content):
                st.success(f"✅ Cover letter '{cover_letter_name}' saved!")
            else:
                st.error("Failed to save cover letter")
