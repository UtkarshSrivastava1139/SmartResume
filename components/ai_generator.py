"""
AI Content Generator for SmartResume AI
Handles all AI-powered content generation
"""

import streamlit as st
from utils.ai_client import AIClient
from utils.prompts import (
    get_summary_prompt, get_experience_prompt, 
    get_project_prompt, get_skills_suggestion_prompt
)
from utils.helpers import clean_bullet_points

class AIGenerator:
    """Class to handle AI content generation"""
    
    def __init__(self):
        """Initialize AI generator with AI client"""
        try:
            self.client = AIClient()
            self.is_available = True
        except Exception as e:
            st.error(f"Failed to initialize AI: {str(e)}")
            self.is_available = False
    
    def generate_professional_summary(self, name, target_role, experience_years, 
                                     key_skills, education):
        """
        Generate professional summary using AI
        
        Args:
            name (str): Candidate name
            target_role (str): Target job role
            experience_years (int): Years of experience
            key_skills (str): Key skills
            education (str): Education background
            
        Returns:
            str: Generated professional summary
        """
        if not self.is_available:
            return "AI service is not available. Please enter summary manually."
        
        if not target_role:
            return "Please enter a target job role first."
        
        # Prepare education string
        if isinstance(education, list) and education:
            edu_str = f"{education[0]['degree']} in {education[0]['field']}"
        else:
            edu_str = "Bachelor's Degree"
        
        prompt = get_summary_prompt(name, target_role, experience_years, 
                                   key_skills, edu_str)
        
        with st.spinner("🤖 Generating professional summary..."):
            result = self.client.generate_content(prompt)
        
        return result
    
    def generate_experience_bullets(self, job_title, company, duration, responsibilities):
        """
        Generate experience bullet points using AI
        
        Args:
            job_title (str): Job title
            company (str): Company name
            duration (str): Employment duration
            responsibilities (str): Basic responsibilities
            
        Returns:
            list: Generated bullet points
        """
        if not self.is_available:
            return ["AI service is not available. Please enter bullet points manually."]
        
        if not responsibilities:
            return ["Please enter basic responsibilities first."]
        
        prompt = get_experience_prompt(job_title, company, duration, responsibilities)
        
        with st.spinner("🤖 Generating professional bullet points..."):
            result = self.client.generate_content(prompt)
        
        # Clean and format bullet points
        bullets = clean_bullet_points(result)
        return bullets if bullets else [result]
    
    def enhance_project_description(self, project_title, duration, technologies, description):
        """
        Enhance project description using AI
        
        Args:
            project_title (str): Project title
            duration (str): Project duration
            technologies (str): Technologies used
            description (str): Basic description
            
        Returns:
            str: Enhanced project description
        """
        if not self.is_available:
            return "AI service is not available. Using original description."
        
        if not description:
            return "Please enter a basic project description first."
        
        prompt = get_project_prompt(project_title, duration, technologies, description)
        
        with st.spinner("🤖 Enhancing project description..."):
            result = self.client.generate_content(prompt)
        
        return result
    
    def suggest_skills(self, target_role, current_skills):
        """
        Suggest additional skills using AI
        
        Args:
            target_role (str): Target job role
            current_skills (str): Current skills (comma-separated)
            
        Returns:
            list: Suggested skills
        """
        if not self.is_available:
            return []
        
        if not target_role:
            return []
        
        prompt = get_skills_suggestion_prompt(target_role, current_skills)
        
        with st.spinner("🤖 Suggesting relevant skills..."):
            result = self.client.generate_content(prompt)
        
        # Parse comma-separated skills
        if result and not result.startswith("Please") and not result.startswith("Rate") and not result.startswith("Invalid"):
            skills = [s.strip() for s in result.split(',')]
            return [s for s in skills if s]  # Remove empty strings
        
        return []
    
    def optimize_entire_resume(self, resume_data):
        """
        Comprehensive AI optimization of entire resume for target role
        
        Args:
            resume_data (dict): Complete resume data
            
        Returns:
            dict: Optimized resume data with AI enhancements
        """
        if not self.is_available:
            return None
        
        target_role = resume_data.get('target_role', '')
        if not target_role:
            return None
        
        optimizations = {}
        
        with st.spinner("AI is analyzing and optimizing your resume..."):
            # 1. Generate/Enhance Summary
            if not resume_data.get('summary') or len(resume_data.get('summary', '')) < 50:
                summary = self.generate_professional_summary(
                    name=resume_data.get('name', 'Candidate'),
                    target_role=target_role,
                    experience_years=resume_data.get('experience_years', 0),
                    key_skills=resume_data.get('technical_skills', ''),
                    education=resume_data.get('education_list', [])
                )
                if summary and not summary.startswith("Please"):
                    optimizations['summary'] = summary
            
            # 2. Enhance ALL Experiences
            if resume_data.get('experience_list'):
                enhanced_experiences = []
                for exp in resume_data['experience_list']:
                    responsibilities = exp.get('responsibilities', '')
                    if responsibilities:
                        bullets = self.generate_experience_bullets(
                            job_title=exp['job_title'],
                            company=exp['company'],
                            duration=f"{exp.get('start_date', '')} - {exp.get('end_date', '')}",
                            responsibilities=responsibilities
                        )
                        if bullets and not bullets[0].startswith("Please"):
                            exp_copy = exp.copy()
                            exp_copy['bullet_points'] = bullets
                            enhanced_experiences.append(exp_copy)
                        else:
                            enhanced_experiences.append(exp)
                    else:
                        enhanced_experiences.append(exp)
                
                if enhanced_experiences:
                    optimizations['experience_list'] = enhanced_experiences
            
            # 3. Enhance ALL Projects
            if resume_data.get('projects_list'):
                enhanced_projects = []
                for proj in resume_data['projects_list']:
                    description = proj.get('description', '')
                    if description and len(description) > 10:
                        enhanced_desc = self.enhance_project_description(
                            project_title=proj['title'],
                            duration=proj.get('duration', ''),
                            technologies=proj.get('technologies', ''),
                            description=description
                        )
                        if enhanced_desc and not enhanced_desc.startswith("Please"):
                            proj_copy = proj.copy()
                            proj_copy['enhanced_description'] = enhanced_desc
                            enhanced_projects.append(proj_copy)
                        else:
                            enhanced_projects.append(proj)
                    else:
                        enhanced_projects.append(proj)
                
                if enhanced_projects:
                    optimizations['projects_list'] = enhanced_projects
            
            # 4. Suggest Additional Skills
            current_skills = resume_data.get('technical_skills', '')
            suggested = self.suggest_skills(target_role, current_skills)
            if suggested:
                optimizations['suggested_skills'] = suggested
        
        return optimizations
    
    def analyze_resume_quality(self, resume_data):
        """
        Analyze resume and provide feedback
        
        Args:
            resume_data (dict): Resume data
            
        Returns:
            str: Analysis and suggestions
        """
        if not self.is_available:
            return "AI service not available"
        
        prompt = f"""
        Analyze this resume and provide constructive feedback:
        
        Target Role: {resume_data.get('target_role', 'Not specified')}
        Experience: {resume_data.get('experience_years', 0)} years
        Summary: {resume_data.get('summary', 'Not provided')}
        Skills: {resume_data.get('technical_skills', 'Not provided')}
        Education: {len(resume_data.get('education_list', []))} entries
        Work Experience: {len(resume_data.get('experience_list', []))} entries
        Projects: {len(resume_data.get('projects_list', []))} entries
        
        Provide:
        1. Overall strength assessment (1-10)
        2. What's working well (2-3 points)
        3. What needs improvement (2-3 specific suggestions)
        4. ATS optimization tips (2-3 keywords/phrases to add)
        
        Format as a clear, actionable report.
        """
        
        with st.spinner("AI is analyzing your resume..."):
            result = self.client.generate_content(prompt)
        
        return result

def render_ai_buttons():
    """Render AI generation buttons in the UI"""
    st.markdown("---")
    st.subheader("AI Content Enhancement")
    
    # Primary Action - Optimize Everything
    st.markdown("**Complete AI Optimization**")
    optimize_all = st.button(
        "✨ Optimize Entire Resume with AI",
        use_container_width=True,
        type="primary",
        key="btn_optimize_all",
        help="AI will analyze and enhance your entire resume for your target role"
    )
    
    st.markdown("---")
    st.markdown("**Individual Enhancements**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        generate_summary = st.button("Generate Summary", 
                                    use_container_width=True,
                                    key="btn_generate_summary")
    
    with col2:
        enhance_experience = st.button("Enhance All Experience", 
                                      use_container_width=True,
                                      key="btn_enhance_experience",
                                      help="Generate professional bullet points for ALL work experiences")
    
    with col3:
        suggest_skills = st.button("Suggest Skills", 
                                  use_container_width=True,
                                  key="btn_suggest_skills")
    
    col4, col5 = st.columns(2)
    
    with col4:
        enhance_projects = st.button("Enhance All Projects",
                                    use_container_width=True,
                                    key="btn_enhance_projects",
                                    help="Improve ALL project descriptions with AI")
    
    with col5:
        analyze_resume = st.button("Analyze Resume Quality",
                                  use_container_width=True,
                                  key="btn_analyze",
                                  help="Get AI feedback and improvement suggestions")
    
    return {
        'optimize_all': optimize_all,
        'generate_summary': generate_summary,
        'enhance_experience': enhance_experience,
        'suggest_skills': suggest_skills,
        'enhance_projects': enhance_projects,
        'analyze_resume': analyze_resume
    }

def handle_ai_generation_pre_render(ai_generator):
    """
    Handle AI generation requests BEFORE widgets are rendered
    This avoids session state widget conflicts
    """
    # Check for pending AI generation flags
    if st.session_state.get('_generate_summary_pending'):
        resume_data = {
            'name': st.session_state.get('name', ''),
            'target_role': st.session_state.get('target_role', ''),
            'experience_years': st.session_state.get('experience_years', 0),
            'technical_skills': st.session_state.get('technical_skills', ''),
            'soft_skills': st.session_state.get('soft_skills', ''),
            'education_list': st.session_state.get('education_list', [])
        }
        
        if resume_data.get('target_role'):
            # Get key skills
            all_skills = f"{resume_data['technical_skills']}, {resume_data['soft_skills']}".strip(', ')
            
            summary = ai_generator.generate_professional_summary(
                name=resume_data.get('name', 'Candidate'),
                target_role=resume_data['target_role'],
                experience_years=resume_data.get('experience_years', 0),
                key_skills=all_skills if all_skills else 'Various technical skills',
                education=resume_data.get('education_list', [])
            )
            
            if summary and not summary.startswith("Please") and not summary.startswith("Rate") and not summary.startswith("Invalid"):
                st.session_state['summary'] = summary
                st.success("Professional summary generated!")
            else:
                st.error(summary)
        else:
            st.warning("Please enter a target job role first.")
        
        # Clear the flag
        st.session_state['_generate_summary_pending'] = False
    
    # Check for pending optimize all flag
    if st.session_state.get('_optimize_all_pending'):
        resume_data = {
            'name': st.session_state.get('name', ''),
            'target_role': st.session_state.get('target_role', ''),
            'experience_years': st.session_state.get('experience_years', 0),
            'technical_skills': st.session_state.get('technical_skills', ''),
            'soft_skills': st.session_state.get('soft_skills', ''),
            'education_list': st.session_state.get('education_list', []),
            'experience_list': st.session_state.get('experience_list', []),
            'projects_list': st.session_state.get('projects_list', []),
            'summary': st.session_state.get('summary', '')
        }
        
        if resume_data.get('target_role'):
            with st.spinner("AI is optimizing your entire resume... This may take a moment."):
                optimizations = ai_generator.optimize_entire_resume(resume_data)
                
                if optimizations:
                    # Apply all optimizations
                    if 'summary' in optimizations:
                        st.session_state['summary'] = optimizations['summary']
                    
                    if 'experience_list' in optimizations:
                        st.session_state['experience_list'] = optimizations['experience_list']
                    
                    if 'projects_list' in optimizations:
                        st.session_state['projects_list'] = optimizations['projects_list']
                    
                    if 'suggested_skills' in optimizations:
                        current_skills = st.session_state.get('technical_skills', '')
                        new_skills = ', '.join(optimizations['suggested_skills'])
                        combined = f"{current_skills}, {new_skills}" if current_skills else new_skills
                        st.session_state['technical_skills'] = combined
                    
                    st.success("Resume optimized successfully! All sections enhanced with AI.")
                    st.balloons()
                else:
                    st.error("Could not optimize resume. Please check your inputs and try again.")
        else:
            st.warning("Please enter a target job role first to optimize your resume.")
        
        # Clear the flag
        st.session_state['_optimize_all_pending'] = False

def handle_ai_generation(ai_buttons, ai_generator, resume_data):
    """
    Handle AI generation button clicks - Comprehensive AI enhancement system
    
    Args:
        ai_buttons (dict): Button states
        ai_generator (AIGenerator): AI generator instance
        resume_data (dict): Current resume data
    """
    
    # OPTIMIZE ENTIRE RESUME - Most comprehensive option
    if ai_buttons.get('optimize_all'):
        # Set flag and rerun to handle before widget render
        st.session_state['_optimize_all_pending'] = True
        st.rerun()
    
    # Generate Professional Summary
    if ai_buttons['generate_summary']:
        # Set flag and rerun to handle before widget render
        st.session_state['_generate_summary_pending'] = True
        st.rerun()
    
    # Enhance ALL Experiences (not just empty ones)
    if ai_buttons['enhance_experience']:
        if resume_data.get('experience_list'):
            enhanced_count = 0
            
            with st.spinner("Enhancing all work experiences with AI..."):
                for idx, exp in enumerate(st.session_state.experience_list):
                    responsibilities = exp.get('responsibilities', '')
                    
                    # Generate bullets for ALL experiences that have responsibilities
                    if responsibilities:
                        bullets = ai_generator.generate_experience_bullets(
                            job_title=exp['job_title'],
                            company=exp['company'],
                            duration=f"{exp.get('start_date', '')} - {exp.get('end_date', '')}",
                            responsibilities=responsibilities
                        )
                        
                        if bullets and not bullets[0].startswith("Please") and not bullets[0].startswith("Rate") and not bullets[0].startswith("Invalid"):
                            st.session_state.experience_list[idx]['bullet_points'] = bullets
                            enhanced_count += 1
            
            if enhanced_count > 0:
                st.success(f"Enhanced {enhanced_count} experience entries with professional bullet points!")
                st.rerun()
            else:
                st.warning("Please add responsibilities to your work experiences first.")
        else:
            st.warning("Please add work experience first.")
        return
    
    # Enhance ALL Projects
    if ai_buttons.get('enhance_projects'):
        if resume_data.get('projects_list'):
            enhanced_count = 0
            
            with st.spinner("Enhancing all project descriptions with AI..."):
                for idx, proj in enumerate(st.session_state.projects_list):
                    description = proj.get('description', '')
                    
                    if description and len(description) > 10:
                        enhanced_desc = ai_generator.enhance_project_description(
                            project_title=proj['title'],
                            duration=proj.get('duration', ''),
                            technologies=proj.get('technologies', ''),
                            description=description
                        )
                        
                        if enhanced_desc and not enhanced_desc.startswith("Please"):
                            st.session_state.projects_list[idx]['enhanced_description'] = enhanced_desc
                            enhanced_count += 1
            
            if enhanced_count > 0:
                st.success(f"Enhanced {enhanced_count} project descriptions!")
                st.rerun()
            else:
                st.warning("Please add project descriptions first.")
        else:
            st.warning("Please add projects first.")
        return
    
    # Suggest Skills
    if ai_buttons['suggest_skills']:
        if resume_data.get('target_role'):
            current_skills = resume_data.get('technical_skills', '')
            
            with st.spinner("AI is suggesting relevant skills..."):
                suggested = ai_generator.suggest_skills(
                    target_role=resume_data['target_role'],
                    current_skills=current_skills
                )
            
            if suggested:
                st.success("Suggested Skills:")
                st.write(", ".join(suggested))
                
                # Option to add suggested skills
                if st.button("Add These Skills"):
                    current = st.session_state.get('technical_skills', '')
                    new_skills = ", ".join(suggested)
                    combined = current + ", " + new_skills if current else new_skills
                    st.session_state.technical_skills = combined
                    st.rerun()
            else:
                st.info("No additional skills suggested.")
        else:
            st.warning("Please enter a target job role first.")
        return
    
    # Analyze Resume Quality
    if ai_buttons.get('analyze_resume'):
        if not resume_data.get('target_role'):
            st.warning("Please enter a target job role for accurate analysis.")
            return
        
        with st.spinner("AI is analyzing your resume quality..."):
            analysis = ai_generator.analyze_resume_quality(resume_data)
        
        if analysis:
            st.markdown("### Resume Analysis Report")
            st.markdown(analysis)
        return
