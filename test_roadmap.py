
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from roadmap_generator import analyze_skill_gap, generate_roadmap

resume_text = extract_resume_text("sample_resume.pdf")
skills = extract_skills(resume_text)

role = "Cybersecurity Analyst"

result = analyze_skill_gap(skills, role)

print("\n===== SKILL GAP ANALYSIS =====")
print("Selected role:", role)
print("Matched skills:", result["matched_skills"])
print("Missing skills:", result["missing_skills"])

print("\n===== LEARNING ROADMAP =====")
for step in generate_roadmap(result["missing_skills"]):
    print("-", step)
