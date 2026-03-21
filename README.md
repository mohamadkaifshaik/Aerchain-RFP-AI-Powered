RFP Mail Demo - Minimal working project

This project runs a small FastAPI backend storing data in SQLite and can send real emails via SMTP.

Requirements
- Python 3.10+
- pip

Setup
1. Unzip project and open terminal in backend folder:
   cd backend
2. Create virtualenv and install dependencies:
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
3. Copy .env.example to backend/.env and fill SMTP_ variables with real SMTP credentials.
   Example for Gmail (not recommended for production): SMTP_HOST=smtp.gmail.com, SMTP_PORT=587, SMTP_USER=you@gmail.com, SMTP_PASS=app_password
4. Start the backend:
   uvicorn app.main:app --reload --port 8000
5. Open frontend/index.html in your browser (or run a static server) and use the UI.

How email sending works
- Create vendors via UI (add their email).
- Create an RFP.
- Click "Send to all vendors" on an RFP; backend will call SMTP to send each vendor an email.
- The backend returns success/failure for each send attempt.

Testing without SMTP
- If SMTP env vars are not set, the API will return an error message explaining SMTP not configured.

API endpoints
- POST /api/rfps -> create RFP {title, description, budget_cents?, items?}
- GET /api/rfps -> list
- POST /api/vendors -> create vendor {name, primary_email}
- GET /api/vendors -> list
- POST /api/rfps/{rfp_id}/send -> send to list of vendor IDs (body is list of UUIDs)
- POST /api/proposals/ingest -> ingest raw proposal {rfp_id, vendor_email, raw_text}
- POST /api/rfps/{rfp_id}/send -> send to list of vendor IDs (body is list of UUIDs)
- POST /api/proposals/ingest -> ingest raw proposal {rfp_id, vendor_email, raw_text}
- - POST /api/rfps/{rfp_id}/send -> send to list of vendor IDs (body is list of UUIDs)

