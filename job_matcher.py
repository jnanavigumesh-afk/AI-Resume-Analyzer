
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = Path(__file__).parent / "data" / "job_roles.csv"


def recommend_jobs(detected_skills):
    jobs = pd.read_csv(DATA_FILE).fillna("")

    if not detected_skills:
        return jobs.assign(match_score=0.0)

    resume_skills = " ".join(
        item["skill"] for item in detected_skills
    )

    job_texts = jobs["required_skills"].tolist()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [resume_skills] + job_texts
    )

    scores = cosine_similarity(
        vectors[0:1], vectors[1:]
    )[0]

    jobs["match_score"] = (scores * 100).round(2)

    return jobs.sort_values(
        "match_score", ascending=False
    ).reset_index(drop=True)
