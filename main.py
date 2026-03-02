# main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import models
import datetime
from schema import EventCreate
import os

# ----------------------
# Create DB tables
# ----------------------
Base.metadata.create_all(bind=engine)

# ----------------------
# FastAPI app
# ----------------------
app = FastAPI(title="Worker Productivity Dashboard API")

# ----------------------
# Enable CORS
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Serve frontend
# ----------------------
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ----------------------
# DB Dependency
# ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# Seed data endpoint
# ----------------------
@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    # clear old data
    db.query(models.Event).delete()
    db.query(models.Worker).delete()
    db.query(models.Workstation).delete()
    db.commit()

    # create workers
    workers = []
    for i in range(1, 7):
        worker = models.Worker(name=f"W{i}")
        db.add(worker)
        workers.append(worker)

    # create stations
    stations = []
    for i in range(1, 7):
        station = models.Workstation(name=f"S{i}")
        db.add(station)
        stations.append(station)

    db.commit()

    for w in workers:
        db.refresh(w)
    for s in stations:
        db.refresh(s)

    now = datetime.datetime.utcnow()
    for w in workers:
        for s in stations:
            event = models.Event(
                timestamp=now,
                worker_id=w.id,
                workstation_id=s.id,
                event_type="working",
                confidence=0.95,
                count=5
            )
            db.add(event)
    db.commit()

    return {"message": "Seed data created"}

# ----------------------
# Event ingestion
# ----------------------
@app.post("/events")
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(
        timestamp=event.timestamp,
        worker_id=event.worker_id,
        workstation_id=event.workstation_id,
        event_type=event.event_type,
        confidence=event.confidence,
        count=event.count
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {"message": "Event stored successfully", "event_id": new_event.id}

# ----------------------
# Worker Metrics
# ----------------------
@app.get("/metrics/workers")
def worker_metrics(db: Session = Depends(get_db)):
    result = []
    workers = db.query(models.Worker).all()
    for w in workers:
        events = db.query(models.Event).filter(models.Event.worker_id == w.id).all()
        working = sum(1 for e in events if e.event_type == "working")
        idle = sum(1 for e in events if e.event_type == "idle")
        total_units = sum(e.count for e in events)
        utilization = working / (working + idle) if (working + idle) > 0 else 0
        result.append({
            "worker_id": w.id,
            "worker_name": w.name,
            "working_events": working,
            "idle_events": idle,
            "utilization": round(utilization, 2),
            "total_units": total_units
        })
    return result

# ----------------------
# Station Metrics
# ----------------------
@app.get("/metrics/stations")
def station_metrics(db: Session = Depends(get_db)):
    result = []
    stations = db.query(models.Workstation).all()
    for s in stations:
        events = db.query(models.Event).filter(models.Event.workstation_id == s.id).all()
        working = sum(1 for e in events if e.event_type == "working")
        idle = sum(1 for e in events if e.event_type == "idle")
        total_units = sum(e.count for e in events)
        utilization = working / (working + idle) if (working + idle) > 0 else 0
        result.append({
            "station_id": s.id,
            "station_name": s.name,
            "working_events": working,
            "idle_events": idle,
            "utilization": round(utilization, 2),
            "total_units": total_units
        })
    return result

# ----------------------
# Factory Metrics
# ----------------------
@app.get("/metrics/factory")
def factory_metrics(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    working = sum(1 for e in events if e.event_type == "working")
    idle = sum(1 for e in events if e.event_type == "idle")
    total_units = sum(e.count for e in events)
    utilization = working / (working + idle) if (working + idle) > 0 else 0
    return {
        "total_working_events": working,
        "total_idle_events": idle,
        "utilization": round(utilization, 2),
        "total_units": total_units
    }

# ----------------------
# Automatically seed dummy data on startup if DB is empty
# ----------------------
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if db.query(models.Worker).count() == 0:
            seed_data(db)
    finally:
        db.close()