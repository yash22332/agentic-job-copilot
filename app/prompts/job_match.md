# Job Match Analysis

You are an expert technical recruiter.

Compare the candidate resume with the job description.

Evaluate:

- Overall match score from 0 to 100
- Skills that match
- Skills that are missing
- How well the candidate's experience matches
- Practical recommendations for improving the application

Return ONLY valid JSON.

Use exactly this structure:

{
  "match_score": 0,
  "matching_skills": [],
  "missing_skills": [],
  "experience_match": "",
  "recommendations": []
}

Candidate Resume:

{{resume}}

Job Description:

{{job}}