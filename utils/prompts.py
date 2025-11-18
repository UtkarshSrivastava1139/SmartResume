"""
AI Prompt Templates for SmartResume AI
Contains all prompt templates for different resume sections
"""

def get_summary_prompt(name, target_role, experience_years, key_skills, education, education_status="Completed"):
    """Generate prompt for professional summary"""
    if education_status == "Pursuing":
        edu_context = f"Currently pursuing {education}"
    else:
        edu_context = f"{education} graduate"
    
    return f"""You are an expert resume writer. Generate a compelling professional summary for a resume.

Candidate Details:
- Name: {name}
- Target Role: {target_role}
- Years of Experience: {experience_years}
- Key Skills: {key_skills}
- Education: {edu_context}

Requirements:
1. Write a 3-4 line professional summary (50-70 words)
2. Highlight key strengths and expertise
3. Include relevant keywords for ATS optimization
4. Use confident and professional tone
5. Focus on value proposition to employer
6. Make it concise and impactful
7. Do not use first person pronouns (I, me, my)
8. CRITICAL: If status is "Pursuing", the candidate is CURRENTLY A STUDENT, not a graduate. Use phrases like "pursuing", "student", or "seeking opportunities while completing degree"
9. CRITICAL: If status is "Completed", the candidate has graduated. Use phrases like "graduate", "holds degree", or "completed"
10. Do NOT use any markdown formatting (no **, *, _, etc.)
11. Use plain text only

Generate only the professional summary text, no additional commentary:"""

def get_experience_prompt(job_title, company, duration, responsibilities):
    """Generate prompt for experience bullet points"""
    return f"""You are an expert resume writer specializing in creating impact-driven bullet points.

Job Details:
- Job Title: {job_title}
- Company: {company}
- Duration: {duration}
- Basic Responsibilities: {responsibilities}

Transform these responsibilities into 3-5 professional bullet points that:
1. Start with strong action verbs (Led, Developed, Implemented, Achieved, Designed, etc.)
2. Include quantifiable metrics where possible (%, numbers, time saved, users impacted)
3. Highlight technical skills and tools used
4. Show impact and results achieved
5. Follow ATS-friendly formatting
6. Use past tense for previous roles
7. Do NOT use any markdown formatting (no **, *, _, etc.)
8. Use plain text only

Generate only the bullet points (one per line, no bullet characters needed), no additional commentary:"""

def get_project_prompt(project_title, duration, technologies, description):
    """Generate prompt for project description"""
    return f"""You are a technical resume writer specializing in creating impact-driven project descriptions using the STAR methodology.

Project Information:
- Title: {project_title}
- Duration: {duration}
- Technologies: {technologies}
- Basic Description: {description}

Transform this into 2-3 professional bullet points following the STAR methodology:
- Situation: Brief context/problem being solved
- Task: What needed to be accomplished
- Action: Specific technical actions and technologies used
- Result: Measurable outcomes, impact, or achievements

Requirements:
1. Create 2-3 bullet points that follow STAR structure
2. Start each bullet with strong action verbs (Developed, Engineered, Built, Implemented, Designed, Created, etc.)
3. Include specific technologies and frameworks mentioned
4. Add quantifiable metrics where possible (performance improvements, users served, data processed, etc.)
5. Highlight technical complexity and architectural decisions
6. Show impact and results achieved
7. Use past tense consistently
8. Keep each bullet concise (15-25 words)
9. Do NOT use any markdown formatting (no **, *, _, etc.)
10. Use plain text only

Generate only the bullet points (one per line, no bullet characters needed), no additional commentary:"""

def get_skills_suggestion_prompt(target_role, current_skills, industry="Technology"):
    """Generate prompt for skills suggestions"""
    return f"""You are a career advisor and ATS expert. Suggest additional skills for a resume.

Current Information:
- Target Role: {target_role}
- Existing Skills: {current_skills}
- Industry: {industry}

Suggest 5-8 relevant skills that would strengthen this resume for the target role.
Include a mix of:
1. Technical skills relevant to the role
2. Industry-standard tools and technologies
3. Popular frameworks or libraries
4. Relevant methodologies (e.g., Agile, DevOps, CI/CD)

Requirements:
- Only suggest skills that are genuinely relevant
- Don't repeat existing skills
- Focus on in-demand, marketable skills
- Keep skill names concise and standard

Return only skill names, comma-separated, no additional commentary:"""

def get_cover_letter_prompt(name, email, phone, job_title, company="", job_description="", skills="", summary="", additional_notes="", education_status="Completed"):
    """Generate prompt for cover letter"""
    if education_status == "Pursuing":
        status_context = "currently pursuing my degree as a student"
    else:
        status_context = "a recent graduate who has completed my degree"
    
    return f"""You are a professional career coach and cover letter writer. 
Using the information below, generate a concise, compelling cover letter addressed to the hiring manager. 
The tone should be formal, confident, and enthusiastic. The content should be ATS-optimized and free of any markdown or special characters.

Candidate Details:
- Name: {name}
- Contact: {email}, {phone}
- Target Job Title: {job_title}
- Target Company: {company if company else "Not specified"}
- Education Status: {status_context}

Job Description/Requirements:
{job_description if job_description else "Not provided - use general best practices for the role"}

Skills and Strengths: {skills if skills else "Not specified"}
Professional Summary: {summary if summary else "Not provided"}

Additional Context: {additional_notes if additional_notes else "None"}

Instructions:
1. Write exactly 3-4 paragraphs with the following structure:
   - Paragraph 1: Strong opening - express enthusiasm for the role and briefly introduce yourself
   - Paragraph 2-3: Highlight 2-3 key qualifications, skills, or achievements that make you ideal for this role
   - Paragraph 4: Professional closing with call to action (expressing interest in interview/discussion)
2. Keep total length between 300-400 words
3. Include keywords and phrases relevant to {job_title} roles for ATS optimization
4. Use professional, confident tone without being overly casual
5. CRITICAL: If education status says "pursuing" or "student", they are CURRENTLY STUDYING, not graduated. Use appropriate language.
6. CRITICAL: If education status says "graduate" or "completed", they have finished their degree. Use past tense.
7. Do NOT use any markdown formatting (no **, *, _, etc.)
8. Use plain text only - no special characters or bullets
9. Make it personalized and compelling, not generic
10. If company name is provided, mention it naturally in the content
11. Avoid clichés and overused phrases

Generate only the cover letter body text (do not include "Dear Hiring Manager" salutation or signature block), no additional commentary:"""

def get_achievement_prompt(achievement_description):
    """Generate prompt for achievement enhancement"""
    return f"""You are an expert resume writer. Enhance this achievement/certification description.

Achievement/Certification: {achievement_description}

Enhance this into a professional one-line statement that:
1. Clearly states the achievement or certification
2. Includes relevant details (issuing organization, date, etc.)
3. Highlights significance or impact if applicable
4. Uses professional language
5. Is concise (10-15 words)

Generate only the enhanced achievement text, no additional commentary:"""
