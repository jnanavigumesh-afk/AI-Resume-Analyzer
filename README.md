
# AI Resume Analyzer and Job Recommendation System

## Project Overview
A Python and Streamlit application that analyzes resumes, extracts skills, recommends suitable job roles, identifies potential skill gaps, and provides learning suggestions.

## Features
- Resume upload and text extraction
- Skill identification and categorization
- Job-role recommendations
- Skill-gap analysis
- Learning roadmap
- Analysis report download (if implemented)

## Technologies
- Python
- Streamlit
- Pandas
- pypdf
- python-docx
- Scikit-learn (if used by the matching module)

## Project Structure
- `app.py` — Streamlit application
- `resume_parser.py` — Resume text extraction
- `text_cleaner.py` — Text cleaning
- `skill_extractor.py` — Skill detection
- `job_matcher.py` — Job-role matching
- `roadmap_generator.py` — Learning suggestions
- `data/` — Job-role and skill datasets

## Setup Instructions

1. Install Python.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment.
4. Install the dependencies:

   `pip install -r requirements.txt`

5. Run the application:

   `streamlit run app.py`

## Responsible Use
Recommendations are intended for career guidance. Match scores are estimates, not hiring decisions. Do not upload confidential resumes to a public repository.

## Author
Jnanavi G Umesh
