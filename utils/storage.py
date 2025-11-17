"""
Local Storage Utilities for SmartResume AI
Handles saving/loading resume data to browser session and JSON files
"""

import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional


class LocalStorage:
    """Manages local storage of resumes and cover letters"""
    
    def __init__(self):
        """Initialize local storage in session state"""
        if 'saved_resumes' not in st.session_state:
            st.session_state['saved_resumes'] = []
        if 'saved_cover_letters' not in st.session_state:
            st.session_state['saved_cover_letters'] = []
    
    def save_resume(self, resume_name: str, resume_data: Dict) -> bool:
        """
        Save resume to session state
        
        Args:
            resume_name: Name for the resume
            resume_data: Complete resume data dictionary
            
        Returns:
            bool: True if saved successfully
        """
        try:
            # Check if resume with same name exists
            existing_index = None
            for i, resume in enumerate(st.session_state['saved_resumes']):
                if resume['name'] == resume_name:
                    existing_index = i
                    break
            
            resume_entry = {
                'name': resume_name,
                'target_role': resume_data.get('target_role', ''),
                'data': resume_data,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if existing_index is not None:
                # Update existing resume
                resume_entry['created_at'] = st.session_state['saved_resumes'][existing_index]['created_at']
                st.session_state['saved_resumes'][existing_index] = resume_entry
            else:
                # Add new resume
                st.session_state['saved_resumes'].append(resume_entry)
            
            return True
        except Exception as e:
            st.error(f"Error saving resume: {str(e)}")
            return False
    
    def get_all_resumes(self) -> List[Dict]:
        """Get all saved resumes"""
        return st.session_state.get('saved_resumes', [])
    
    def get_resume(self, resume_name: str) -> Optional[Dict]:
        """
        Get a specific resume by name
        
        Args:
            resume_name: Name of the resume
            
        Returns:
            Resume dictionary or None
        """
        for resume in st.session_state.get('saved_resumes', []):
            if resume['name'] == resume_name:
                return resume
        return None
    
    def delete_resume(self, resume_name: str) -> bool:
        """
        Delete a resume
        
        Args:
            resume_name: Name of the resume to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            st.session_state['saved_resumes'] = [
                r for r in st.session_state.get('saved_resumes', [])
                if r['name'] != resume_name
            ]
            
            # Also delete associated cover letters
            st.session_state['saved_cover_letters'] = [
                cl for cl in st.session_state.get('saved_cover_letters', [])
                if cl.get('resume_name') != resume_name
            ]
            
            return True
        except Exception as e:
            st.error(f"Error deleting resume: {str(e)}")
            return False
    
    def save_cover_letter(self, cover_letter_name: str, resume_name: str, 
                         company: str, job_title: str, content: str) -> bool:
        """
        Save cover letter to session state
        
        Args:
            cover_letter_name: Name for the cover letter
            resume_name: Associated resume name
            company: Company name
            job_title: Job title
            content: Cover letter content
            
        Returns:
            bool: True if saved successfully
        """
        try:
            # Check if cover letter with same name exists
            existing_index = None
            for i, cl in enumerate(st.session_state['saved_cover_letters']):
                if cl['name'] == cover_letter_name:
                    existing_index = i
                    break
            
            cover_letter_entry = {
                'name': cover_letter_name,
                'resume_name': resume_name,
                'company': company,
                'job_title': job_title,
                'content': content,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if existing_index is not None:
                # Update existing
                cover_letter_entry['created_at'] = st.session_state['saved_cover_letters'][existing_index]['created_at']
                st.session_state['saved_cover_letters'][existing_index] = cover_letter_entry
            else:
                # Add new
                st.session_state['saved_cover_letters'].append(cover_letter_entry)
            
            return True
        except Exception as e:
            st.error(f"Error saving cover letter: {str(e)}")
            return False
    
    def get_cover_letters_for_resume(self, resume_name: str) -> List[Dict]:
        """Get all cover letters for a specific resume"""
        return [
            cl for cl in st.session_state.get('saved_cover_letters', [])
            if cl.get('resume_name') == resume_name
        ]
    
    def export_all_data(self) -> str:
        """
        Export all saved data as JSON string
        
        Returns:
            JSON string of all data
        """
        data = {
            'resumes': st.session_state.get('saved_resumes', []),
            'cover_letters': st.session_state.get('saved_cover_letters', []),
            'export_date': datetime.now().isoformat()
        }
        return json.dumps(data, indent=2)
    
    def import_data(self, json_str: str) -> bool:
        """
        Import data from JSON string
        
        Args:
            json_str: JSON string to import
            
        Returns:
            bool: True if imported successfully
        """
        try:
            data = json.loads(json_str)
            
            if 'resumes' in data:
                st.session_state['saved_resumes'] = data['resumes']
            if 'cover_letters' in data:
                st.session_state['saved_cover_letters'] = data['cover_letters']
            
            return True
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
            return False
    
    def clear_all_data(self) -> bool:
        """Clear all saved data"""
        try:
            st.session_state['saved_resumes'] = []
            st.session_state['saved_cover_letters'] = []
            return True
        except Exception as e:
            st.error(f"Error clearing data: {str(e)}")
            return False
