"""
Mangifera Shield — Khet-Khata Ledger Route
CRUD operations for offline-first harvest inventory management.
"""

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database import get_db, LedgerEntry

router = APIRouter(prefix="/api/ledger", tags=["Khet-Khata Ledger"])


class LedgerEntryCreate(BaseModel):
    client_id: Optional[str] = None
    farmer_phone: str = "0000000000"
    variety: str = "Dasheri"
    quantity_kg: float
    quality_grade: str = "A"
    harvest_date: str
    estimated_price: float = 0.0
    notes: str = ""


class LedgerEntryUpdate(BaseModel):
    variety: Optional[str] = None
    quantity_kg: Optional[float] = None
    quality_grade: Optional[str] = None
    harvest_date: Optional[str] = None
    estimated_price: Optional[float] = None
    notes: Optional[str] = None


class SyncBatch(BaseModel):
    entries: List[LedgerEntryCreate]


@router.get("/entries")
async def get_entries(
    farmer_phone: str = "0000000000",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all ledger entries for a farmer."""
    entries = db.query(LedgerEntry).filter(
        LedgerEntry.farmer_phone == farmer_phone
    ).order_by(LedgerEntry.created_at.desc()).limit(limit).all()

    total_kg = sum(e.quantity_kg for e in entries)
    total_value = sum(e.estimated_price * e.quantity_kg for e in entries if e.estimated_price)

    return {
        "entries": [
            {
                "id": e.client_id,
                "variety": e.variety,
                "quantity_kg": e.quantity_kg,
                "quality_grade": e.quality_grade,
                "harvest_date": e.harvest_date,
                "estimated_price": e.estimated_price,
                "notes": e.notes,
                "synced": e.synced,
                "created_at": e.created_at.isoformat() if e.created_at else ""
            }
            for e in entries
        ],
        "summary": {
            "total_entries": len(entries),
            "total_quantity_kg": round(total_kg, 1),
            "estimated_total_value": round(total_value),
            "varieties": list(set(e.variety for e in entries))
        }
    }


@router.post("/entries")
async def create_entry(entry: LedgerEntryCreate, db: Session = Depends(get_db)):
    """Create a new ledger entry."""
    client_id = entry.client_id or str(uuid.uuid4())

    db_entry = LedgerEntry(
        client_id=client_id,
        farmer_phone=entry.farmer_phone,
        variety=entry.variety,
        quantity_kg=entry.quantity_kg,
        quality_grade=entry.quality_grade,
        harvest_date=entry.harvest_date,
        estimated_price=entry.estimated_price,
        notes=entry.notes,
        synced=True
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return {
        "success": True,
        "entry_id": client_id,
        "message": "Entry created successfully"
    }


@router.put("/entries/{client_id}")
async def update_entry(
    client_id: str,
    update: LedgerEntryUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing ledger entry."""
    entry = db.query(LedgerEntry).filter(LedgerEntry.client_id == client_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(entry, key, value)

    entry.updated_at = datetime.now(timezone.utc)
    db.commit()

    return {"success": True, "message": "Entry updated"}


@router.delete("/entries/{client_id}")
async def delete_entry(client_id: str, db: Session = Depends(get_db)):
    """Delete a ledger entry."""
    entry = db.query(LedgerEntry).filter(LedgerEntry.client_id == client_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db.delete(entry)
    db.commit()

    return {"success": True, "message": "Entry deleted"}


@router.post("/sync")
async def sync_entries(batch: SyncBatch, db: Session = Depends(get_db)):
    """
    Bulk sync entries from offline IndexedDB.
    Creates or updates entries based on client_id.
    """
    synced = 0
    errors = []

    for entry_data in batch.entries:
        try:
            client_id = entry_data.client_id or str(uuid.uuid4())

            # Check if entry already exists
            existing = db.query(LedgerEntry).filter(
                LedgerEntry.client_id == client_id
            ).first()

            if existing:
                # Update existing
                existing.variety = entry_data.variety
                existing.quantity_kg = entry_data.quantity_kg
                existing.quality_grade = entry_data.quality_grade
                existing.harvest_date = entry_data.harvest_date
                existing.estimated_price = entry_data.estimated_price
                existing.notes = entry_data.notes
                existing.synced = True
                existing.updated_at = datetime.utcnow()
            else:
                # Create new
                new_entry = LedgerEntry(
                    client_id=client_id,
                    farmer_phone=entry_data.farmer_phone,
                    variety=entry_data.variety,
                    quantity_kg=entry_data.quantity_kg,
                    quality_grade=entry_data.quality_grade,
                    harvest_date=entry_data.harvest_date,
                    estimated_price=entry_data.estimated_price,
                    notes=entry_data.notes,
                    synced=True
                )
                db.add(new_entry)

            synced += 1
        except Exception as e:
            errors.append({"client_id": entry_data.client_id, "error": str(e)})

    db.commit()

    return {
        "success": True,
        "synced": synced,
        "errors": errors,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
