# AI Job Application Tracker — Phase 2

React + FastAPI + PostgreSQL job application tracker.

## Phase 2 features
- Authentication with JWT
- Persistent PostgreSQL data
- Application CRUD
- Search and status filtering
- Dashboard analytics
- Response, interview and offer rates
- Interview scheduling and deletion
- Resume version tracking
- Responsive desktop/mobile layout
- Docker Compose local development

## Run
```bash
docker compose build --no-cache
docker compose up
```

Open http://localhost:5173

API docs: http://localhost:8000/docs

## Important
Do not use `docker compose down -v` unless you intentionally want to delete the local PostgreSQL volume.

Phase 3 will add resume parsing, job-description analysis, AI match scoring and skill-gap recommendations.


## Phase 3 — AI Analysis

Phase 3 adds PDF/DOCX resume parsing, automatic skill extraction and normalization, job-description skill extraction, explainable resume-to-job matching, skill-gap recommendations, and persistent AI analysis history. The matching engine runs locally and requires no paid AI API. It uses a weighted 80% skill-overlap + 20% high-signal keyword score so results are reproducible and easy to explain in a project demo.

### Phase 3 API
- `POST /api/ai/resume/upload` — upload and parse PDF/DOCX resume
- `GET /api/ai/resume/{resume_id}` — retrieve resume analysis
- `POST /api/ai/job-description` — analyze pasted job description
- `GET /api/ai/job-descriptions` — list analyzed JDs
- `POST /api/ai/match` — calculate match score and skill gaps
- `GET /api/ai/matches` — recent match history

Uploaded resumes are persisted in `backend/uploads/resumes` and mounted into the Docker backend container.
