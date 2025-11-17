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

### 📊 ATS-Optimized Output
- Clean, parseable PDF format
- Standard section headings
- No complex graphics or tables
- Proper font choices (Arial/Calibri)
- Consistent formatting

### ⚡ User-Friendly Interface
- Simple, intuitive forms
- Real-time resume preview
- One-click PDF download
- Mobile-responsive design
- Dark mode support

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API Key (free tier available)

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

4. **Get your Gemini API Key**
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the generated key

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
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
- **AI Engine**: Google Gemini API (`gemini-2.0-flash-exp`)
- **PDF Generation**: FPDF2
- **Language**: Python 3.10+
- **Additional Libraries**: 
  - google-generativeai
  - python-dotenv
  - Pillow

## 📁 Project Structure

```
smartresume-ai/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── components/                     # UI components
│   ├── __init__.py
│   ├── form_sections.py           # Input forms
│   ├── ai_generator.py            # AI content generation
│   ├── preview.py                 # Resume preview
│   └── pdf_exporter.py            # PDF generation
│
├── templates/                      # Resume templates
│   ├── __init__.py
│   └── classic_template.py        # Classic template
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── gemini_client.py           # Gemini API wrapper
│   ├── validators.py              # Input validation
│   ├── prompts.py                 # AI prompt templates
│   └── helpers.py                 # Helper functions
│
└── assets/                         # Static assets
    └── styles/
        └── custom.css             # Custom styling
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
- [ ] Cover letter generation
- [ ] LinkedIn integration
- [ ] Resume version control
- [ ] Collaboration features

---

**Version 1.0.0** - Academic Project
