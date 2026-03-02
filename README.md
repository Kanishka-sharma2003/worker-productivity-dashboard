Factory Worker Productivity Dashboard
Overview

This is a full-stack web application that ingests AI-generated worker activity events from CCTV systems, stores them in a database, computes productivity metrics, and displays them in a dashboard.

It is built using FastAPI for the backend, SQLite for data storage, and a HTML + JavaScript frontend for the dashboard.

Architecture
AI CCTV Events → Backend (FastAPI) → SQLite Database → Backend → Frontend Dashboard

Frontend: HTML + JS, displays tables for workers, workstations, and factory metrics. Fetches data every 5 seconds.

Backend: FastAPI, exposes APIs to ingest events and fetch computed metrics. Computes worker, workstation, and factory-level metrics.

Database: SQLite stores Worker, Workstation, and Event data. Pre-populated with dummy data.

CORS Handling: Backend allows requests from http://127.0.0.1:5500
 so frontend can fetch data seamlessly.

Database Schema
Table	Columns	Description
Worker	id, name	Metadata for workers
Workstation	id, name	Metadata for workstations
Event	id, timestamp, worker_id, workstation_id, event_type, confidence, count	AI-generated events

Event types include: working, idle, absent, product_count

Each event is assumed to represent 1 unit of time

Metrics Definitions
Worker Metrics

Total active time → count of working events

Total idle time → count of idle events

Utilization (%) → working / (working + idle)

Total units produced → sum of count from all events

Units per hour / per shift → optionally computed assuming 1 event = 1 unit of time

Workstation Metrics

Occupancy time → total events recorded at the station

Utilization (%) → working / (working + idle)

Total units produced → sum of count for that station

Throughput rate → total units / total event time

Factory Metrics

Total productive time → sum of all working events

Total production count → sum of count from all events

Average production rate → average units across all workers/workstations

Average utilization → average utilization across all workers

Assumptions / Edge Cases

Each event represents 1 unit of time

Last event duration is ignored

Out-of-order events: metrics computed on all events regardless of timestamp

Duplicate events: counted as-is (optional unique constraint can be added)

Intermittent connectivity: frontend automatically retries fetch every 5 seconds

Backend Endpoints
Endpoint	Method	Description
/	GET	Check server is running
/seed	POST	Seed dummy data
/events	POST	Ingest AI-generated event
/metrics/workers	GET	Get worker-level metrics
/metrics/stations	GET	Get workstation-level metrics
/metrics/factory	GET	Get factory summary metrics
How to Run Locally
Option 1 – Python + Uvicorn

Backend:

cd backend
python -m venv venv
venv\Scripts\activate.bat  # Windows
# source venv/bin/activate  # Linux / Mac
pip install -r requirements.txt
uvicorn main:app --reload

Seed dummy data:

curl -X POST http://127.0.0.1:8000/seed

Frontend:

cd frontend
python -m http.server 5500

Open browser at http://127.0.0.1:5500

Option 2 – Docker Compose (Recommended)

Folder structure:

worker-productivity-dashboard/
├─ backend/Dockerfile
├─ frontend/Dockerfile
├─ docker-compose.yml
├─ README.md
└─ (other files/folders)

Run everything via Docker:

cd "C:\Users\Kanishka Sharma\OneDrive\Desktop\worker-productivity-dashboard"
docker compose up --build

Seed data (in a new terminal):

curl -X POST http://127.0.0.1:8000/seed

Backend → http://127.0.0.1:8000

Frontend → http://127.0.0.1:5500

Metrics auto-refresh every 5 seconds

Stop containers:

docker compose down
Theoretical Considerations
1. Model Versioning

Each event can include a model_version field to track which CV model generated it

Enables traceability and comparisons across versions

2. Detecting Model Drift

Monitor confidence scores for events

Sudden drops in confidence indicate potential drift

3. Triggering Retraining

Retraining scheduled if drift is detected

Use recent events as training dataset for the new model version

4. Scaling

5 → 100+ cameras: asynchronous ingestion + batch DB writes

Multi-site deployment: separate databases per site, aggregate metrics centrally

Notes

Backend: FastAPI + SQLite

Frontend: HTML + JS fetching APIs every 5 seconds

Dummy data: 6 workers, 6 workstations, pre-populated for first-run usability