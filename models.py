from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    events = relationship("Event", back_populates="worker")


class Workstation(Base):
    __tablename__ = "workstations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    events = relationship("Event", back_populates="workstation")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    workstation_id = Column(Integer, ForeignKey("workstations.id"))
    event_type = Column(String)
    confidence = Column(Float)
    count = Column(Integer, default=0)

    worker = relationship("Worker", back_populates="events")
    workstation = relationship("Workstation", back_populates="events")