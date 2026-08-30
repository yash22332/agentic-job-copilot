# 🤖 Agentic Job Copilot

An AI-powered job search assistant that analyzes a user's resume, retrieves real job listings through MCP, and compares selected jobs against the candidate's resume.

## Features

- Resume analysis using an LLM
- Real job search using MCP + Adzuna
- Real job listing links for View / Apply
- Resume-to-job match analysis
- Match score, matching skills, missing skills, and recommendations
- FastAPI backend
- Streamlit frontend
- Automated tests with pytest

## Architecture

```text
                    Streamlit
                        |
                      FastAPI
                 _______|_______
                |               |
                v               v
        Resume Analysis     Job Search
                |               |
                v               v
               LLM          MCP Client
                                |
                                v
                           MCP Server
                                |
                                v
                           Adzuna API
                                |
                                v
                         Real Job Listings
                                |
                                v
                         View / Apply
                                |
                                v
                         Analyze Match
                                |
                                v
                              LLM
                                |
                                v
                    Score + Skills + Gaps

Tech Stack
Python
FastAPI
Streamlit
LangGraph
MCP
Pydantic
Gemini
Adzuna API
pytest
Project Structure
app/
├── api/
├── mcp/
├── models/
├── prompts/
├── services/
├── workflows/
├── config.py
├── llm.py
├── llm_factory.py
├── dev_llm.py
└── resume_parser.py

frontend/
└── app.py

tests/
└── test_*.py

data/
├── sample_resume.pdf
└── sample_resume.txt
Setup

Clone the repository:

git clone https://github.com/yash22332/agentic-job-copilot.git
cd agentic-job-copilot

Create and activate a virtual environment:

Windows
python -m venv .venv
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file:

GEMINI_API_KEY=
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.6-flash
LLM_MODE=fake

ADZUNA_APP_ID=
ADZUNA_APP_KEY=
LLM Modes

For development:

LLM_MODE=fake

This uses deterministic development responses and does not consume Gemini API quota.

For real LLM usage:

LLM_MODE=real

Make sure a valid Gemini API key is configured.

Run Tests
python -m pytest
Run the Application

Start the FastAPI backend:

python -m uvicorn app.api.app:app --reload

In another terminal, start Streamlit:

streamlit run frontend/app.py

Open:

http://localhost:8501
How It Works
Upload a resume.
Analyze the resume.
Enter a job title, location, and optional skills.
Search real job listings through MCP and Adzuna.
Open the original listing using View / Apply.
Click Analyze Match on a selected job.
The system compares the resume with the job description and returns a match score, matching skills, missing skills, and recommendations.
MCP

The application keeps external job access behind an MCP client/server boundary.

The MCP tool:

search_jobs(query, location)

retrieves job listings from Adzuna and returns normalized job data to the application.

Notes
Adzuna credentials are required for real job search.
Gemini credentials are required for real LLM mode.
.env should never be committed to Git.
Runtime uploaded resumes are stored temporarily and cleaned up after processing.