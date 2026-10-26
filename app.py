
import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import recommend_jobs
from roadmap_generator import analyze_skill_gap, generate_roadmap


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
/* Overall page */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #25205b 0%, transparent 36%),
        radial-gradient(ellipse at 95% 15%, #103c50 0%, transparent 30%),
        #0a1020;
    color: #eef3ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Typography */
h1, h2, h3 {
    color: #f4f7ff !important;
}

p, label {
    color: #cbd5e8;
}

/* Hero banner */
.hero {
    background: linear-gradient(120deg, #28205c, #17365b 65%, #10505c);
    border: 1px solid #43527e;
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 26px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, .25);
}

.hero .eyebrow {
    color: #67e8f9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    font-size: clamp(28px, 4vw, 44px);
    font-weight: 800;
    margin: 12px 0;
    line-height: 1.15;
}

.hero p {
    color: #d5e5ff;
    font-size: 16px;
    margin-bottom: 0;
}

/* Metrics and containers */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #18233c, #111a2c);
    border: 1px solid #334463;
    padding: 18px;
    border-radius: 16px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #334463;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stFileUploader"] {
    background: #111b30;
    border: 1px dashed #647de8;
    border-radius: 16px;
    padding: 16px;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #7157ed, #238dc9);
    color: white !important;
    border: 0;
    border-radius: 10px;
    font-weight: 650;
    min-height: 42px;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(1.15);
    border: 1px solid #75e5f4;
}

/* Select box */
div[data-baseweb="select"] > div {
    background: #151f35;
    border-color: #405276;
    border-radius: 10px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #10172a;
    border-right: 1px solid #293753;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 22px;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("AI Resume Analyzer & Job Recommendation System")
st.write(
    "Upload your resume to identify skills, discover suitable job roles, "
    "and create a learning roadmap."
)

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("Please upload a resume smaller than 5 MB.")
        st.stop()

    suffix = Path(uploaded_file.name).suffix.lower()

    try:
        with tempfile.NamedTemporaryFile(
            suffix=suffix, delete=False
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = Path(temp_file.name)

        try:
            resume_text = extract_resume_text(temp_path)
        finally:
            temp_path.unlink(missing_ok=True)

        cleaned_text = clean_text(resume_text)
        skills = extract_skills(cleaned_text)

        
        st.success("Resume processed successfully!")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric("Skills Identified", len(skills))

        with metric2:
            st.metric(
                "Job Roles Analysed",
                len(recommend_jobs(skills))
            )

        with metric3:
            st.metric(
                "Resume Status",
                "Ready" if resume_text.strip() else "Empty"
            )

        st.success("Resume processed successfully!")

        st.subheader("1. Extracted Skills")

        if skills:
            skills_df = pd.DataFrame(skills)
            st.dataframe(skills_df, width="stretch")
            st.metric("Skills detected", len(skills))
        else:
            st.warning(
                "No dictionary skills were detected. "
                "Check whether the resume contains readable text."
            )

        st.subheader("2. Recommended Job Roles")

        recommendations = recommend_jobs(skills)
        top_jobs = recommendations.head(3)

        st.dataframe(
            top_jobs[["job_role", "match_score"]],
            use_container_width=True
        )

        st.bar_chart(
            top_jobs.set_index("job_role")["match_score"]
        )

        st.caption(
            "Match scores are text-similarity estimates, not hiring "
            "probabilities or measures of a candidate's worth."
        )

        st.subheader("3. Skill-Gap Analysis")

        jobs_df = pd.read_csv(
            Path(__file__).parent / "data" / "job_roles.csv"
        )
        selected_role = st.selectbox(
            "Choose a job role",
            jobs_df["job_role"].tolist()
        )

        gap = analyze_skill_gap(skills, selected_role)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Skills found in your resume**")
            st.write(gap["matched_skills"] or ["None detected"])

        with col2:
            st.write("**Skills not mentioned in your resume**")
            st.write(gap["missing_skills"] or ["None"])

        st.subheader("4. Suggested Learning Roadmap")

        for index, step in enumerate(
            generate_roadmap(gap["missing_skills"]), start=1
        ):
            st.write(f"{index}. {step}")

        st.subheader("5. Download Analysis")

        report_lines = [
            "AI RESUME ANALYSIS REPORT",
            "",
            f"Resume file: {uploaded_file.name}",
            "",
            "DETECTED SKILLS:"
        ]

        report_lines.extend(
            f"- {item['skill']} ({item['category']})"
            for item in skills
        )

        report_lines.extend(["", "TOP JOB RECOMMENDATIONS:"])

        report_lines.extend(
            f"- {row.job_role}: {row.match_score}% similarity"
            for row in top_jobs.itertuples()
        )

        report_lines.extend([
            "",
            f"SKILL GAP FOR: {selected_role}",
            "",
            "MATCHED SKILLS:"
        ])
        report_lines.extend(
            f"- {skill}" for skill in gap["matched_skills"]
        )
        report_lines.extend(["", "SKILLS NOT MENTIONED:"])
        report_lines.extend(
            f"- {skill}" for skill in gap["missing_skills"]
        )
        report_lines.extend(["", "LEARNING ROADMAP:"])
        report_lines.extend(
            f"- {step}" for step in generate_roadmap(gap["missing_skills"])
        )

        st.download_button(
            "Download Analysis Report",
            data="\n".join(report_lines),
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )

    except Exception as error:
        st.error(f"Could not analyze this resume: {error}")
        st.info(
            "Check the file format, skill dictionary, job-role dataset, "
            "and terminal error message."
        )
