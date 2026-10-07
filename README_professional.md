# AI Job Tracker

> A full-stack job search and career management platform for organizing job opportunities, tracking applications, managing resumes, preparing for interviews, and analyzing resume-to-job compatibility.

<p align="center">
  <strong>Search jobs. Track applications. Analyze resumes. Prepare for interviews.</strong>
</p>

---

## 📌 Overview

AI Job Tracker is a full-stack web application designed to bring the complete job-search workflow into one focused workspace.

Instead of managing job applications across spreadsheets, emails, browser tabs, resumes, and separate notes, the platform provides a centralized system for:

- 🔎 Job discovery
- 📋 Application tracking
- 📄 Resume management
- 🤖 Resume-to-job matching
- 🎯 Skill-gap identification
- 📅 Interview management
- 🧠 Interview preparation
- 📧 Recruiter email integration
- 📊 Career and application insights

The project was built to explore practical full-stack software engineering, data processing, API integration, authentication, resume analysis, and job-search automation.

---

## ✨ Key Features

### 🔎 Job Search

Search and explore relevant job opportunities from integrated job sources.

Features include:

- Job title / role search
- Location filtering
- Job source information
- Job details
- Required skills
- Job description
- External application links
- Job-to-resume matching workflow

---

### 📋 Application Tracking

Keep your job applications organized from the initial search through the hiring process.

Supported application stages include:

```text
Wishlist
   ↓
Applying
   ↓
Applied
   ↓
Screening
   ↓
Interview
   ↓
Offer
   ↓
Rejected / Withdrawn
```

The application workspace provides a centralized view of:

- Company
- Job role
- Location
- Application status
- Application date
- Salary information
- Required skills
- Notes
- Resume version used

---

### 📄 Resume Management

Upload and manage multiple resume versions from one place.

Supported formats:

- PDF
- DOC
- DOCX

Resume management allows different resume versions to be maintained for different job targets.

This is useful when maintaining separate versions such as:

```text
Python Developer Resume
Data Analyst Resume
Software Developer Resume
Full-Stack Developer Resume
```

---

### 🤖 Resume-to-Job Matching

The AI Analysis workspace compares a selected resume against a job description.

The workflow is:

```text
Select Resume
      ↓
Paste Job Description
      ↓
Analyze Job Requirements
      ↓
Detect Skills & Keywords
      ↓
Match Resume
      ↓
Generate Match Score
      ↓
Identify Matched & Missing Skills
```

The current matching engine uses:

- Technical skill alignment
- Job-description keyword alignment
- Detected resume skills
- Detected job requirements
- Match history

### Current scoring model

| Component | Weight |
|-----------|-------:|
| Technical skill alignment | 80% |
| Job-description keyword alignment | 20% |

The result includes:

- Overall match score
- Skill score
- Keyword score
- Matched skills
- Missing skills
- Recommendations
- Previous match history

The system also tracks the same resume + job combination so repeated analysis does not unnecessarily create duplicate history entries.

---

### 🎯 Skill Gap Identification

The matching system highlights skills that are present in the job description but missing from the selected resume.

Example:

```text
Matched Skills
✓ Python
✓ SQL
✓ Pandas
✓ REST API

Missing Skills
• Docker
• AWS
• Kubernetes
```

This helps identify areas that may require further learning or resume improvement.

> Missing skills are treated as learning / improvement gaps and should not be falsely added to a resume.

---

### 📅 Interview Management

Manage interviews associated with applications.

Interview information can include:

- Company
- Job role
- Interview round
- Interview date
- Interview type
- Interviewer
- Notes
- Preparation information

---

### 🧠 Interview Preparation

The application provides an interview preparation workspace based on the role and interview information.

Preparation includes:

- Pre-interview checklist
- Role-specific questions
- Technical preparation
- HR preparation
- Company research reminders
- Resume review
- Project preparation
- Questions to ask the interviewer
- Personal preparation notes

Example preparation areas:

```text
✓ Research company
✓ Review job description
✓ Review resume
✓ Prepare introduction
✓ Practice technical questions
✓ Prepare questions for interviewer
✓ Test camera / microphone
✓ Keep resume and portfolio ready
```

---

### 📧 Recruiter Messages & Gmail Integration

The project includes a Gmail integration workflow for recruiter and application-related messages.

The intended workflow is:

```text
Gmail
  ↓
Email Sync
  ↓
Recruiter Message Detection
  ↓
Email Classification
  ↓
Application Matching
  ↓
Application Status Update
```

Relevant email signals can include:

| Email signal | Application status |
|--------------|-------------------|
| Application received | Applied |
| Application under review | Screening |
| Interview invitation | Interview |
| Offer letter | Offer |
| Rejection notification | Rejected |

The system is designed to use strong confirmation signals rather than changing application status from generic recruiter emails.

---

## 📸 Product Screenshots

### Dashboard

The main dashboard provides an overview of the job-search workspace, applications, interviews, resumes, and career activity.

![Dashboard](./screenshots/dashboard.png)

---

### Job Search

Search and explore job opportunities based on role, location, and other filters.

![Job Search](./screenshots/job-search.png)

---

### Application Tracking

Track applications and monitor their current stage throughout the hiring process.

![Applications](./screenshots/applications.png)

---

### Interview Management

Manage upcoming interviews and interview-related information.

![Interviews](./screenshots/interviews.png)

---

### AI Resume Analysis

Compare a resume against a job description and identify skill alignment.

![AI Analysis](./screenshots/ai-analysis-1.png)

![AI Analysis - Job Requirements](./screenshots/ai-analysis-2.png)

![AI Analysis - Matching](./screenshots/ai-analysis-3.png)

![AI Analysis - Results](./screenshots/ai-analysis-4.png)

![AI Analysis - Match History](./screenshots/ai-analysis-5.png)

---

## 🏗️ Application Architecture

The project follows a frontend/backend architecture.

```text
                    ┌───────────────────────┐
                    │      JobTracker       │
                    │      Web Client       │
                    └───────────┬───────────┘
                                │
                                │ HTTP / REST API
                                ▼
                    ┌───────────────────────┐
                    │      FastAPI          │
                    │       Backend         │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        ┌───────────┐    ┌──────────────┐   ┌─────────────┐
        │ PostgreSQL│    │ Resume / AI  │   │ Integrations│
        │ Database  │    │ Processing   │   │ Gmail / Jobs│
        └───────────┘    └──────────────┘   └─────────────┘
```

---

## 🧰 Technology Stack

### Frontend

- React
- JavaScript
- HTML
- CSS
- Axios
- Chart.js
- React Chart.js 2
- Vite

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- JWT-based authentication

### Resume Processing

- PDF processing
- DOC/DOCX processing
- Resume text extraction
- Skill detection
- Keyword extraction
- Resume-to-job matching

### Integrations

- Gmail / Google OAuth
- External job APIs
- Adzuna job API
- Company / recruiter integrations

### Development Tools

- Git
- GitHub
- VS Code
- Docker / Docker Compose

---

## 📁 Project Structure

```text
ai-job-tracker/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── uploads/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── index.html
│
├── screenshots/
│   ├── ai-analysis-1.png
│   ├── ai-analysis-2.png
│   ├── ai-analysis-3.png
│   ├── ai-analysis-4.png
│   ├── ai-analysis-5.png
│   ├── applications.png
│   ├── dashboard.png
│   ├── interviews.png
│   └── job-search.png
│
├── docker-compose.yml
├── Gmail_SETUP.md
├── PHASE2.md
├── PHASE3.md
├── README.md
└── .gitignore
```

---

# 🚀 Getting Started

## Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- npm
- PostgreSQL
- Git

Docker can also be used if you prefer a containerized setup.

---

## 1. Clone the Repository

```bash
git clone https://github.com/sc2939459-max/ai-job-tracker.git
```

Move into the project:

```bash
cd ai-job-tracker
```

---

# ⚙️ Backend Setup

Open a terminal and move into the backend:

```bash
cd backend
```

### Create a Python virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Backend Environment Variables

Create:

```text
backend/.env
```

Use `.env.example` as the template.

Example:

```env
FRONTEND_URL=http://localhost:5173

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/recruiter-messages/google/callback

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

COMPANY_API_KEY=your_company_api_key
```

### Important

Never commit:

```text
backend/.env
```

to GitHub.

Never put API keys, OAuth secrets, database passwords, or other credentials directly into source code.

Use:

```text
.env
```

for local secrets and:

```text
.env.example
```

for safe placeholders.

---

# 🗄️ Database

The application uses PostgreSQL.

Create a database for the project, for example:

```text
jobtracker
```

Configure the database connection according to the backend configuration.

Make sure PostgreSQL is running before starting the API.

---

# ▶️ Run the Backend

From:

```text
backend/
```

run:

```bash
uvicorn app.main:app --reload --port 8000
```

The API should be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 💻 Frontend Setup

Open another terminal.

Move into:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔄 Running Frontend + Backend

You need two terminals.

### Terminal 1 — Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# 🔑 Authentication

The application uses authenticated API requests.

The frontend API client attaches the authentication token to requests using the HTTP Authorization header.

Example:

```text
Authorization: Bearer <token>
```

Protected application data is associated with the authenticated user.

---

# 📊 Core Application Workflow

The primary workflow is:

```text
                    ┌──────────────┐
                    │   Dashboard  │
                    └──────┬───────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
    ┌───────────┐   ┌─────────────┐   ┌───────────┐
    │ Search    │   │ Applications│   │ Resumes   │
    │ Jobs      │   │             │   │           │
    └─────┬─────┘   └──────┬──────┘   └─────┬─────┘
          │                │                 │
          │                ▼                 │
          │          ┌─────────────┐         │
          │          │ Interviews  │         │
          │          └─────────────┘         │
          │                                  │
          └──────────────┐    ┌──────────────┘
                         ▼    ▼
                    ┌──────────────┐
                    │ AI Analysis  │
                    └──────┬───────┘
                           │
                           ▼
                 Resume-to-Job Match
                           │
                           ▼
                  Skill Gap Analysis
```

---

# 🤖 Resume Matching Workflow

```text
1. Select Resume
        ↓
2. Paste Job Description
        ↓
3. Analyze Job Requirements
        ↓
4. Detect Technical Skills
        ↓
5. Detect Job Keywords
        ↓
6. Match Resume
        ↓
7. Calculate Score
        ↓
8. Display Matched Skills
        ↓
9. Display Missing Skills
        ↓
10. Store Match History
```

---

# 📧 Gmail Integration Workflow

The recruiter-message integration follows this general workflow:

```text
Google Account
      ↓
OAuth Authorization
      ↓
Gmail Access
      ↓
Message Synchronization
      ↓
Recruiter Email Classification
      ↓
Application Matching
      ↓
Application Status Update
```

The integration can identify relevant signals such as:

```text
Application Received
Application Under Review
Interview Invitation
Offer
Rejection
```

Google OAuth configuration is documented separately in:

```text
Gmail_SETUP.md
```

---

# 🧪 Development

Frontend development server:

```bash
cd frontend
npm run dev
```

Backend development server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

For frontend production builds:

```bash
cd frontend
npm run build
```

Preview the production build:

```bash
npm run preview
```

---

# 🐳 Docker

The repository also contains:

```text
docker-compose.yml
```

If Docker is configured for your environment, the application can be started using:

```bash
docker compose up --build
```

Stop the containers with:

```bash
docker compose down
```

---

# 🔒 Security Notes

This repository intentionally excludes sensitive local configuration.

Do not commit:

```text
.env
*.pem
*.key
credentials.json
client_secret.json
database passwords
OAuth client secrets
API keys
JWT secrets
```

If a secret is accidentally committed:

1. Remove it from the working tree.
2. Rotate/revoke the exposed credential.
3. Remove it from Git history when necessary.
4. Add the secret to `.gitignore`.
5. Use an environment variable instead.

---

# 🛣️ Roadmap

Potential future improvements include:

- [ ] Advanced AI resume rewriting
- [ ] Job-specific resume generation
- [ ] Additional resume templates
- [ ] More job-board integrations
- [ ] Improved job deduplication
- [ ] Automated application confirmation detection
- [ ] Advanced recruiter email classification
- [ ] More detailed career analytics
- [ ] Interview feedback tracking
- [ ] Application reminders
- [ ] Follow-up reminders
- [ ] Advanced dashboard analytics
- [ ] Production deployment
- [ ] Automated testing
- [ ] CI/CD pipeline

---

# 🎯 Project Goals

The main goals of this project are to demonstrate practical experience with:

- Full-stack web development
- REST API development
- React application architecture
- Python backend development
- Database design
- Authentication
- File processing
- Resume parsing
- Data extraction
- Skill matching
- API integrations
- OAuth
- Application workflow design
- Responsive UI development
- Git and GitHub workflows

---

# 💡 Why This Project?

Job searching often involves multiple disconnected tools:

```text
Job Boards
   +
Spreadsheets
   +
Email
   +
Resume Files
   +
Interview Notes
   +
Application Tracking
```

AI Job Tracker brings these activities into a single workspace.

The goal is not simply to store job applications, but to create a structured workflow that helps users understand:

```text
What jobs should I apply for?
        ↓
How well does my resume match?
        ↓
What skills am I missing?
        ↓
Which applications are active?
        ↓
What interviews are coming?
        ↓
How should I prepare?
```

---

# 📈 Current Project Status

### Current

- ✅ React frontend
- ✅ FastAPI backend
- ✅ PostgreSQL integration
- ✅ User authentication
- ✅ Job search
- ✅ Application tracking
- ✅ Resume management
- ✅ Resume-to-job matching
- ✅ Skill detection
- ✅ Missing-skill identification
- ✅ Match history
- ✅ Interview management
- ✅ Interview preparation
- ✅ Gmail integration workflow
- ✅ Project screenshots
- ✅ Docker configuration

### In Progress / Future

- 🚧 Advanced AI resume improvement
- 🚧 More automated application tracking
- 🚧 Additional integrations
- 🚧 Production deployment
- 🚧 Automated testing and CI/CD

---

# 👨‍💻 Author

## Sunil Maddipatla

Computer Science graduate interested in:

- Python Development
- Data Analytics
- Software Engineering
- Full-Stack Development
- AI-powered applications

### Technical Skills

```text
Python
SQL / MySQL
PostgreSQL
Pandas
JavaScript
React
HTML
CSS
FastAPI
SQLAlchemy
Git
GitHub
Chart.js
REST APIs
Data Analysis
Data Visualization
```

---

# ⭐ Support the Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

Your feedback and suggestions are welcome.

---

# 📄 License

This project is licensed under the MIT License.

See the [LICENSE](./LICENSE) file for the complete license terms.

---

<p align="center">
  <strong>AI Job Tracker</strong><br>
  A focused workspace for a smarter and more organized job search.
</p>
