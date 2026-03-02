# schema.py
from pydantic import BaseModel
from datetime import datetime

# -------- Event create schema --------
class EventCreate(BaseModel):
    worker_id: int
    station_id: int
    event_type: str   # WORKING or IDLE
    units_produced: int = 0
    timestamp: datetime


# -------- Worker metrics response --------
class WorkerMetrics(BaseModel):
    worker_id: int
    worker_name: str
    working_events: int
    idle_events: int
    utilization: float
    total_units: int


# -------- Station metrics response --------
class StationMetrics(BaseModel):
    station_id: int
    station_name: str
    working_events: int
    idle_events: int
    utilization: float
    total_units: int


# -------- Factory summary response --------
class FactoryMetrics(BaseModel):
    total_working_events: int
    total_idle_events: int
    utilization: float
    total_units: int