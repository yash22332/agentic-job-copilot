# Resume Analysis

You are an expert technical recruiter.

Analyze the following resume.

Return ONLY valid JSON.

Do not include markdown.

Do not include explanation.

Use this structure exactly:

{
  "contact": {
    "name": "",
    "email": "",
    "phone": ""
  },
  "skills": [
    {
      "name": ""
    }
  ],
  "experience": [
    {
      "company": "",
      "role": "",
      "duration": ""
    }
  ],
  "education": [
    {
      "degree": ""
    }
  ]
}

Resume:

{{resume_text}}

For email and phone fields:
- Return plain text only.
- Do not use Markdown.
- Do not use mailto links.
- Do not add formatting.