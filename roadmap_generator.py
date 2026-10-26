
import pandas as pd
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "job_roles.csv"


def analyze_skill_gap(detected_skills, selected_role):
    jobs = pd.read_csv(DATA_FILE).fillna("")

    matching_jobs = jobs[
        jobs["job_role"].str.casefold()
        == selected_role.casefold()
    ]

    if matching_jobs.empty:
        raise ValueError("Selected job role was not found.")

    required = [
        skill.strip()
        for skill in matching_jobs.iloc[0]["required_skills"].split(",")
        if skill.strip()
    ]

    found = {item["skill"].casefold() for item in detected_skills}

    matched = [skill for skill in required if skill.casefold() in found]
    missing = [skill for skill in required if skill.casefold() not in found]

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "required_skills": required
    }


def generate_roadmap(missing_skills):
    if not missing_skills:
        return ["Your resume contains all the listed skills for this role."]

    return [
        f"Learn the fundamentals of {skill}."
        for skill in missing_skills
    ]
