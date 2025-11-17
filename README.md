# 🎯 SmartResume AI - AI-Powered Resume Builder

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SmartResume AI** is an innovative web-based resume builder that leverages Google's Gemini AI to automatically generate professional, ATS-friendly resume content from basic user inputs.

![SmartResume AI Banner](https://img.icons8.com/fluency/96/000000/resume.png)

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Professional Summaries**: Generate compelling 3-4 line career summaries
- **Experience Bullets**: Transform basic job descriptions into impact-driven bullet points
- **Project Descriptions**: Enhance technical project details with AI
- **Skills Optimization**: Get relevant skill suggestions for your target role
- **Cover Letters**: AI-generated cover letters tailored to job descriptions
- **Resume Integration**: Link cover letters to saved resumes for better AI context

### 📊 ATS-Optimized Output
- Clean, parseable PDF format
- Standard section headings
- No complex graphics or tables
- Proper font choices (Arial/Calibri)
- Consistent formatting
- Professional cover letter layout

### ⚡ User-Friendly Interface
- Simple, intuitive forms
- Real-time resume and cover letter preview
- One-click PDF download
- Save/Load resume functionality
- Export/Import data as JSON
- Mobile-responsive design
- Modern, professional UI

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API Key (free tier available) **OR** OpenRouter API Key (free models available)

### Installation

1. **Clone or download this repository**
```bash
git clone https://github.com/yourusername/smartresume-ai.git
cd smartresume-ai
```

2. **Create a virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Get your AI API Key**
   
   **Option 1: Google Gemini (Recommended)**
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the generated key
   
   **Option 2: OpenRouter (Free Models Available)**
   - Visit: https://openrouter.ai/keys
   - Sign up and create an API key
   - Free models like `google/gemma-2-9b-it:free` available

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your API key:
   ```
   # Option 1: Gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Option 2: OpenRouter
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

6. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Fill Personal Information
- Enter your name, email, phone number
- Add LinkedIn profile and portfolio (optional)
- Provide your location

### Step 2: Add Professional Summary
- Enter your target job role
- Specify years of experience
- Click **"Generate with AI"** for professional summary

### Step 3: Add Education
- Select degree/qualification
- Enter institution and field of study
- Add graduation year and grade
- Click **"Add Education Entry"**

### Step 4: List Your Skills
- Enter technical skills (comma-separated)
- Add soft skills
- Click **"Suggest Skills"** for AI recommendations

### Step 5: Add Work Experience
- Enter company name and job title
- Provide employment dates
- Write basic responsibilities
- Click **"Generate Bullet Points"** for AI enhancement

### Step 6: Add Projects
- Enter project title and duration
- List technologies used
- Write brief description
- Click **"Enhance Description"** for AI improvement

### Step 7: Add Certifications
- List certifications and achievements
- One per line

### Step 8: Download Resume
- Review the live preview
- Click **"Generate & Download PDF"**
- Save your professional resume!

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit 1.28+
- **AI Engines**: 
  - Google Gemini API (`gemini-2.0-flash-exp`)
  - OpenRouter API (free models available)
- **PDF Generation**: FPDF2
- **Language**: Python 3.10+
- **Storage**: Session-based local storage with JSON export/import
- **Additional Libraries**: 
  - google-generativeai
  - requests (for OpenRouter)
  - python-dotenv
  - Pillow

## 📁 Project Structure

```
smartresume-ai/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── PROJECT_INFO.md                 # Detailed project documentation
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── components/                     # UI components
│   ├── __init__.py
│   ├── form_sections.py           # Resume input forms
│   ├── ai_generator.py            # AI resume content generation
│   ├── preview.py                 # Resume preview
│   ├── pdf_exporter.py            # PDF generation (resume & cover letter)
│   ├── cover_letter_form.py       # Cover letter input forms
│   ├── cover_letter_generator.py  # AI cover letter generation
│   └── resume_manager.py          # Save/Load/Export/Import functionality
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── ai_client.py               # Unified AI client (Gemini + OpenRouter)
│   ├── gemini_client.py           # Gemini API wrapper
│   ├── openrouter_client.py       # OpenRouter API wrapper
│   └── storage.py                 # Local storage management
│
└── assets/                         # Static assets
    └── styles/
        └── custom.css             # Custom professional styling
```

## 🎯 Key Features Explained

### AI Content Generation

The app uses carefully crafted prompts to generate professional content:

1. **Professional Summary**: Creates compelling 3-4 line summaries highlighting expertise and career goals
2. **Experience Bullets**: Transforms descriptions into action-verb-led, impact-driven statements
3. **Project Descriptions**: Enhances technical depth and clarity
4. **Skills Suggestions**: Recommends relevant skills based on target role

### ATS Optimization

Generated PDFs follow ATS best practices:
- ✅ Single column layout
- ✅ Standard fonts (Arial, Calibri)
- ✅ No headers/footers
- ✅ No images or graphics
- ✅ Simple bullet points
- ✅ Clear section headings
- ✅ Proper spacing and margins

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
GEMINI_API_KEY=your_api_key_here
```

### API Rate Limits (Free Tier)

- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

## 🐛 Troubleshooting

### Common Issues

**Issue**: "GEMINI_API_KEY not found"
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: "Rate limit exceeded"
- **Solution**: Wait a few seconds and try again (free tier limits)

**Issue**: PDF download not working
- **Solution**: Disable pop-up blocker, try different browser

**Issue**: AI generation not working
- **Solution**: Check internet connection, verify API key

**Issue**: Preview not updating
- **Solution**: Refresh the page or clear browser cache

## 📝 Tips for Best Results

### Content Input
- Be specific when describing experiences
- Include numbers and metrics where possible
- Use clear, concise language
- Proofread AI-generated content

### AI Enhancement
- Provide detailed information for better AI output
- Review and edit AI suggestions
- Add personal touches to make it authentic
- Use AI as a starting point, not final output

### ATS Optimization
- Use standard section headings
- Include keywords from job descriptions
- Avoid fancy formatting
- Keep consistent date formats

## 🤝 Contributing

This is an academic project, but suggestions and feedback are welcome!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://ai.google.dev/)
- Built with [Streamlit](https://streamlit.io/)
- Icons from [Icons8](https://icons8.com/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🌟 Show Your Support

If this project helped you create a great resume, please give it a ⭐ on GitHub!

---

**Made with ❤️ for job seekers everywhere**

## 🚀 Future Enhancements

- [ ] Multiple resume templates
- [ ] Job description analyzer
- [ ] Resume scoring system
- [ ] Multi-language support
- [x] Cover letter generation ✅
- [ ] LinkedIn integration
- [x] Resume version control (Save/Load) ✅
- [ ] Collaboration features
- [ ] Cloud storage integration
- [ ] Resume analytics dashboard

---

**Version 2.0.0** - Enhanced with Cover Letter & Storage Features
