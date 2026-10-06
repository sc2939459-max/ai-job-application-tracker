# Gmail recruiter-message integration

The Recruiter Messages page uses Gmail read-only access. It does not send, delete, or modify email.

## 1. Enable Gmail API

In Google Cloud Console:

1. Create/select a project.
2. Enable **Gmail API**.
3. Configure the OAuth consent screen.
4. Create an **OAuth 2.0 Web application** client.
5. Add this authorized redirect URI for local development:

```text
http://localhost:8000/api/recruiter-messages/google/callback
```

## 2. Backend environment

Copy the values into `backend/.env` (never commit this file):

```text
FRONTEND_URL=http://localhost:5173
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/api/recruiter-messages/google/callback
```

The current implementation stores the Gmail refresh token so the backend can sync without asking the user to authorize every time. For production, encrypt that token at rest and keep the encryption key in a secret manager.

## 3. Start the app

Start the FastAPI backend and Vite frontend as usual. Open **Recruiter Messages → Connect Gmail**, complete Google consent, and return to the Recruiter Messages page.

The backend searches recent Gmail messages for job-related signals such as interview, recruiter, hiring, application, assessment, candidate, offer, and job opportunity. It then reads the message headers/body and displays matching messages in the tracker.

## 4. Important limitation

The tracker does not claim that every email is a recruiter message. Filtering is keyword-based and can produce false positives or miss unusual recruiter emails. The Gmail permission is read-only.
