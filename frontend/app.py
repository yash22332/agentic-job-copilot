import requests
import streamlit as st
import json


if "jobs" not in st.session_state:
    st.session_state.jobs = []

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
    
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
            st.session_state.resume_analysis = result

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

    elif uploaded_file is None:
        st.warning("Please upload a resume first.")
    
    elif st.session_state.resume_analysis is None:
        st.warning("Please analyze your resume first.")

    else:
        with st.spinner("Searching and ranking jobs..."):
                
                response = requests.post(
                f"{API_URL}/jobs/search",
                data={
                    "query": query,
                    "location": search_location.strip(),
                    "resume": json.dumps(
                        st.session_state.resume_analysis
                    ),
                },
                timeout=120,
                )

            

        if response.status_code == 200:
            result = response.json()

            st.session_state.jobs = result.get(
                "jobs",
                [],
            )

        else:
            st.error(
                f"API error: {response.status_code}\n\n"
                f"{response.text}"
            )


# Display Find Jobs button
jobs = st.session_state.jobs

if jobs:

    st.success(
        f"Found {len(jobs)} jobs."
    )

    st.caption("Jobs by Adzuna")

    for index, job in enumerate(
        jobs,
        start=1,
    ):
        st.subheader(
            f"{index}. {job['title']}"
        )

        st.write(
            f"**Company:** {job['company']}"
        )

        st.write(
            f"**Location:** {job['location']}"
        )

        if job.get("salary"):
            st.write(
                f"**Salary:** {job['salary']}"
            )

        st.write(
            job["description"]
        )

        if job.get("url"):
            st.link_button(
                "View / Apply",
                job["url"],
            )

        if st.button(
            "Analyze Match",
            key=f"analyze_match_{index}",
        ):
            st.info("Analyze Match button clicked.")

            job_data = {
                "title": job["title"],
                "company": job["company"],
                "description": job["description"],
                "location": job["location"],
                "experience_required": "",
                "required_skills": [],
            }

            with st.spinner(
                "Analyzing your resume against this job..."
            ):
                match_response = requests.post(
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

            if match_response.status_code == 200:
                match = match_response.json()

                st.success(
                    "Match analysis completed!"
                )

                st.metric(
                    "Resume Match Score",
                    f"{match['match_score']}/100",
                )

                st.write(
                    "**Matching Skills:** "
                    + ", ".join(
                        match["matching_skills"]
                    )
                )

                st.write(
                    "**Missing Skills:** "
                    + ", ".join(
                        match["missing_skills"]
                    )
                )

                st.write(
                    "**Experience Match:** "
                    + match["experience_match"]
                )

                st.write(
                    "**Recommendations:**"
                )

                for recommendation in (
                    match["recommendations"]
                ):
                    st.write(
                        f"- {recommendation}"
                    )

            else:
                st.error(
                    f"API error: "
                    f"{match_response.status_code}\n\n"
                    f"{match_response.text}"
                )

        st.divider()