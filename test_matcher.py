
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import recommend_jobs

resume_text = extract_resume_text("sample_resume.pdf")
skills = extract_skills(resume_text)

recommendations = recommend_jobs(skills)

print("\n===== TOP 3 JOB RECOMMENDATIONS =====")

print(
    recommendations[
        ["job_role", "match_score"]
    ].head(3).to_string(index=False)
)
