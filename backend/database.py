"""
Mangifera Shield — Database Models
SQLAlchemy models for farmers, ledger entries, scan results, and sync queue.
"""

import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'mangifera_shield.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Farmer(Base):
    """Farmer profile — local user of the app."""
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, index=True)
    village = Column(String(100), default="Malihabad")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class LedgerEntry(Base):
    """Khet-Khata — offline-first harvest inventory ledger."""
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), unique=True, index=True)  # UUID from frontend
    farmer_phone = Column(String(15), index=True)
    variety = Column(String(50), default="Dasheri")
    quantity_kg = Column(Float, nullable=False)
    quality_grade = Column(String(20), default="A")  # A, B, C
    harvest_date = Column(String(20), nullable=False)
    estimated_price = Column(Float, default=0.0)
    notes = Column(Text, default="")
    synced = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ScanResult(Base):
    """AI disease scan results with diagnosis and treatment."""
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), unique=True, index=True)
    farmer_phone = Column(String(15), index=True)
    disease_name = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    treatment_en = Column(Text, default="")
    treatment_hi = Column(Text, default="")
    image_path = Column(String(255), default="")
    is_healthy = Column(Boolean, default=False)
    certificate_id = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class MandiPrice(Base):
    """Cached mandi prices for offline access."""
    __tablename__ = "mandi_prices"

    id = Column(Integer, primary_key=True, index=True)
    commodity = Column(String(50), default="Mango (Dasheri)")
    market = Column(String(100), nullable=False)
    min_price = Column(Float, default=0.0)
    max_price = Column(Float, default=0.0)
    modal_price = Column(Float, default=0.0)
    unit = Column(String(20), default="Quintal")
    arrival_date = Column(String(20), nullable=False)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency: get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
