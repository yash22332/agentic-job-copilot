import requests
import streamlit as st
import json


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Agentic Job Copilot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Agentic Job Copilot")
st.subheader("AI-powered Resume Analyzer")

st.write(
    "Upload your resume and get a structured analysis "
    "of your skills, experience, and education."
)

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
)

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing your resume..."):

            response = requests.post(
                f"{API_URL}/resumes/analyze",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                },
                timeout=120,
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Resume analyzed successfully!")

            st.header("Candidate")

            contact = result["contact"]

            st.write(f"**Name:** {contact['name']}")
            st.write(f"**Email:** {contact['email']}")
            st.write(f"**Phone:** {contact['phone']}")

            st.header("Skills")

            skills = [
                skill["name"]
                for skill in result["skills"]
            ]

            st.write(", ".join(skills))

            st.header("Experience")

            for experience in result["experience"]:
                st.write(
                    f"**{experience['role']} — "
                    f"{experience['company']}**"
                )
                st.write(experience["duration"])

            st.header("Education")

            for education in result["education"]:
                st.write(
                    f"**{education['degree']}**"
                )

        else:
            st.error(
                f"API error: {response.status_code}\n\n"
                f"{response.text}"
            )

st.divider()

st.header("🎯 Job Match Analysis")

job_title = st.text_input("Job Title")
job_company = st.text_input("Company")
job_location = st.text_input("Location")
job_experience = st.text_input("Experience Required")
job_description = st.text_area("Job Description")

job_skills = st.text_input(
    "Required Skills",
    placeholder="Python, FastAPI, LangGraph, Docker",
)

if uploaded_file is not None and st.button("Analyze Job Match"):

    required_skills = [
        skill.strip()
        for skill in job_skills.split(",")
        if skill.strip()
    ]

    job_data = {
        "title": job_title,
        "company": job_company,
        "description": job_description,
        "location": job_location,
        "experience_required": job_experience,
        "required_skills": required_skills,
    }

    with st.spinner("Analyzing job match..."):

        response = requests.post(
            f"{API_URL}/jobs/match",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            },
            data={
                "job": json.dumps(job_data),
            },
            timeout=120,
        )

    if response.status_code == 200:

        result = response.json()

        st.success("Job match analysis completed!")

        st.metric(
            "Match Score",
            f"{result['match_score']}/100",
        )

        st.subheader("✅ Matching Skills")
        st.write(", ".join(result["matching_skills"]))

        st.subheader("❌ Missing Skills")
        st.write(", ".join(result["missing_skills"]))

        st.subheader("Experience Match")
        st.write(result["experience_match"])

        st.subheader("Recommendations")

        for recommendation in result["recommendations"]:
            st.write(f"- {recommendation}")

    else:
        st.error(
            f"API error: {response.status_code}\n\n"
            f"{response.text}"
        )

st.divider()

st.header("🔎 Find Jobs")

search_title = st.text_input(
    "Job Title",
    placeholder="Python AI Engineer",
)

search_location = st.text_input(
    "Location",
    placeholder="Bangalore",
)

search_keywords = st.text_input(
    "Skills / Keywords (optional)",
    placeholder="FastAPI, LangGraph, MCP",
)

if st.button("Find Jobs"):

    query = search_title.strip()

    if search_keywords.strip():
        query = f"{query} {search_keywords.strip()}"

    if not query:
        st.warning("Please enter a job title or keyword.")
    else:
        with st.spinner("Searching and ranking jobs..."):

            response = requests.post(
                f"{API_URL}/jobs/search",
                data={
                    "query": query,
                    "location": search_location.strip(),
                },
                timeout=120,
            )

        if response.status_code == 200:

            result = response.json()

            recommendations = result.get(
                "recommendations",
                []
            )

            if not recommendations:
                st.info("No matching jobs found.")
            else:
                st.success(
                    f"Found {len(recommendations)} recommended jobs."
                )

                for index, job in enumerate(
                    recommendations,
                    start=1,
                ):

                    st.subheader(
                        f"{index}. {job['job_role']}"
                    )

                    st.write(
                        f"**Match:** "
                        f"{job['relevance_score']}/100"
                    )

                    st.write(
                        f"**Location:** {job['location']}"
                    )

                    st.write(
                        f"**Experience:** "
                        f"{job['experience']}"
                    )

                    st.write(
                        f"**Salary:** {job['salary']}"
                    )

                    st.write(
                        "**Skills:** "
                        + ", ".join(
                            job["skills_required"]
                        )
                    )

                    st.write("**Why:**")

                    if st.button(
                        "Analyze Match",
                        key=f"analyze_match_{index}",
                    ):
                        with st.spinner("Analyzing your resume against this job..."):

                            response = requests.post(
                                f"{API_URL}/jobs/match",
                                files={
                                    "file": (
                                        uploaded_file.name,
                                        uploaded_file.getvalue(),
                                        "application/pdf",
                                    )
                                },
                                 data={
                                    "job": json.dumps(
                                         {
                                            "title": job["job_role"],
                                            "company": job.get("company", ""),
                                            "description": job.get(
                                                "description",
                                                "",
                                            ),
                                            "location": job["location"],
                                            "experience_required": job[
                                                "experience"
                                            ],
                                            "required_skills": job[
                                                "skills_required"
                                            ],
                                        }
                                    ),
                                },
                                timeout=120,
                            )

    if response.status_code == 200:
        match = response.json()

        st.success("Match analysis completed!")

        st.metric(
            "Match Score",
            f"{match['match_score']}/100",
        )

        st.write(
            "**Matching Skills:** "
            + ", ".join(match["matching_skills"])
        )

        st.write(
            "**Missing Skills:** "
            + ", ".join(match["missing_skills"])
        )

        st.write(
            "**Experience Match:** "
            + match["experience_match"]
        )

        st.write("**Recommendations:**")

        for recommendation in match["recommendations"]:
            st.write(f"- {recommendation}")

    else:
        st.error(
            f"API error: {response.status_code}\n\n"
            f"{response.text}"
        )

        for reason in job["reasons"]:
            st.write(f"- {reason}")

            st.divider()

        else:
            st.error(
                f"API error: {response.status_code}\n\n"
                f"{response.text}"
            )