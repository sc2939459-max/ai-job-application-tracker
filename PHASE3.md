# AI Job Tracker — Phase 3

## What was added

1. PDF/DOCX resume upload and text extraction
2. Automatic technical skill detection and normalization
3. Job-description analyzer
4. Explainable resume-to-job match score
5. Skill-gap analysis
6. Keyword overlap analysis
7. Recommendations
8. Persistent AI analysis history in PostgreSQL
9. New **AI Analysis** page in React
10. Docker upload volume so uploaded resumes survive container recreation

## Matching formula

Overall score = 80% skill overlap + 20% high-signal job-keyword overlap.

This is intentionally explainable and deterministic for a portfolio project. It does not require an external paid AI API.

## Run

```bash
cd ~/Downloads/ai-job-tracker
docker compose down
docker compose build --no-cache
docker compose up
```

Open http://localhost:5173.

## Demo flow

1. Open **AI Analysis**.
2. Upload a PDF or DOCX resume.
3. Paste a real job description.
4. Link it to an application if desired.
5. Click **Analyze Job Description**.
6. Click **Run AI Match**.
7. Review overall score, matched skills, missing skills and recommendations.

## API docs

After the backend starts:
http://localhost:8000/api/docs

AI endpoints:
- POST `/api/ai/resume/upload`
- GET `/api/ai/resume/{resume_id}`
- POST `/api/ai/job-description`
- GET `/api/ai/job-descriptions`
- POST `/api/ai/match`
- GET `/api/ai/matches`

## Important

Do not run `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and all stored database data.
