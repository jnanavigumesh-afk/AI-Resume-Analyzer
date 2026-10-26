
from resume_parser import extract_resume_text
from skill_extractor import extract_skills

# Use the resume file located in your project folder.
resume_text = extract_resume_text("sample_resume.pdf")

skills = extract_skills(resume_text)

print("\n===== SKILLS DETECTED IN RESUME =====")

if skills:
    for item in skills:
        print(f"{item['skill']} - {item['category']}")
else:
    print("No matching skills found.")

print(f"\nTotal skills detected: {len(skills)}")
