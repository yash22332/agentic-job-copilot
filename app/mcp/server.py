import os

import requests
from mcp.server import MCPServer
from dotenv import load_dotenv

load_dotenv()

mcp = MCPServer("Job Copilot Tools")


@mcp.tool()
def search_jobs(
    query: str,
    location: str = "",
) -> list[dict[str, str]]:
    """Search real jobs using the Adzuna API."""

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise RuntimeError(
            "ADZUNA_APP_ID and ADZUNA_APP_KEY must be configured."
        )

    response = requests.get(
        "https://api.adzuna.com/v1/api/jobs/in/search/1",
        params={
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 10,
            "what": query,
            "where": location,
            "content-type": "application/json",
        },
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("results", []):
        company = job.get("company", {})
        job_location = job.get("location", {})

        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        if salary_min and salary_max:
            salary = f"{salary_min} - {salary_max}"
        elif salary_min:
            salary = f"{salary_min}+"
        else:
            salary = ""

        jobs.append(
            {
                "title": job.get("title", ""),
                "company": company.get(
                    "display_name",
                    "",
                ),
                "location": job_location.get(
                    "display_name",
                    "",
                ),
                "description": job.get(
                    "description",
                    "",
                ),
                "url": job.get(
                    "redirect_url",
                    "",
                ),
                "salary": salary,
            }
        )

    return jobs


if __name__ == "__main__":
    mcp.run()