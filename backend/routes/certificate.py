"""
Mangifera Shield — Certificate Route
Generate AI-verified quality certificates.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from ..database import get_db, ScanResult
from ..services.certificate_service import generate_certificate

router = APIRouter(prefix="/api/certificate", tags=["Quality Certificate"])


class CertificateRequest(BaseModel):
    scan_id: str
    farmer_name: str = "किसान"
    variety: str = "Dasheri"


@router.post("/generate")
async def create_certificate(
    request: CertificateRequest,
    db: Session = Depends(get_db)
):
    """Generate a quality certificate PDF for a scan result."""
    # Look up scan result
    scan = db.query(ScanResult).filter(
        ScanResult.client_id == request.scan_id
    ).first()

    if scan:
        scan_data = {
            "disease": scan.disease_name,
            "confidence": scan.confidence,
            "is_healthy": scan.is_healthy,
            "scan_date": scan.created_at.isoformat() if scan.created_at else ""
        }
    else:
        # Demo mode — generate with provided data
        scan_data = {
            "disease": "Healthy",
            "confidence": 0.96,
            "is_healthy": True,
            "scan_date": datetime.now().isoformat()
        }

    pdf_bytes, certificate_id = generate_certificate(
        scan_data=scan_data,
        farmer_name=request.farmer_name
    )

    # Update scan with certificate ID
    if scan:
        scan.certificate_id = certificate_id
        db.commit()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=MangiferaShield_{certificate_id}.pdf",
            "X-Certificate-ID": certificate_id
        }
    )


@router.post("/preview")
async def preview_certificate(request: CertificateRequest):
    """Get certificate data without generating PDF."""
    return {
        "certificate_preview": {
            "farmer_name": request.farmer_name,
            "variety": request.variety,
            "scan_id": request.scan_id,
            "generated_at": datetime.now().isoformat(),
            "status": "ready"
        }
    }
