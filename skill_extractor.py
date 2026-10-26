
import pandas as pd
import re
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "skill_dictionary.csv"


def extract_skills(text):
    """
    Identify skills from resume text using a CSV dictionary.
    Returns the detected skill names and their categories.
    """

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Skill dictionary not found: {DATA_FILE}"
        )

    skills_df = pd.read_csv(DATA_FILE)
    detected_skills = []

    for _, row in skills_df.iterrows():
        skill = str(row["skill"]).strip()

        # Match whole terms while allowing flexible whitespace.
        escaped_skill = re.escape(skill)
        pattern = (
            r"(?<!\w)" +
            escaped_skill.replace(r"\ ", r"\s+") +
            r"(?!\w)"
        )

        if re.search(pattern, text, flags=re.IGNORECASE):
            detected_skills.append({
                "skill": skill,
                "category": row["category"]
            })

    return detected_skills
