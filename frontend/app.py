import requests
import streamlit as st


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