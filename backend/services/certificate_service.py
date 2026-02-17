"""
Mangifera Shield — Certificate Service
Generates AI-verified quality certificates as PDF with QR codes.
"""

import io
import os
import uuid
import qrcode
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph


def generate_certificate(scan_data: dict, farmer_name: str = "किसान") -> tuple:
    """
    Generate a quality certificate PDF with QR code.
    Returns (pdf_bytes, certificate_id).
    """
    certificate_id = f"MS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Background
    c.setFillColor(HexColor("#f0fdf4"))
    c.rect(0, 0, width, height, fill=1)

    # Header banner
    c.setFillColor(HexColor("#166534"))
    c.rect(0, height - 120, width, 120, fill=1)

    # Title
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "MANGIFERA SHIELD")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 75, "AI-Verified Quality Certificate")

    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 95, "Malihabad Mango Belt | Powered by Edge AI")

    # Certificate ID
    c.setFillColor(HexColor("#166534"))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 150, f"Certificate ID: {certificate_id}")

    # Divider
    c.setStrokeColor(HexColor("#22c55e"))
    c.setLineWidth(2)
    c.line(50, height - 170, width - 50, height - 170)

    # Farmer details
    y_pos = height - 210
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#166534"))
    c.drawString(60, y_pos, "Farmer Details / Kisan Vivaran")

    y_pos -= 30
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#1f2937"))
    c.drawString(60, y_pos, f"Name / Naam: {farmer_name}")

    y_pos -= 25
    c.drawString(60, y_pos, f"Location / Sthaan: Malihabad, Lucknow, UP")

    y_pos -= 25
    c.drawString(60, y_pos, f"Date / Taarikh: {datetime.now().strftime('%d %B %Y')}")

    # Divider
    y_pos -= 20
    c.setStrokeColor(HexColor("#d1d5db"))
    c.setLineWidth(1)
    c.line(50, y_pos, width - 50, y_pos)

    # AI Scan Results
    y_pos -= 35
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#166534"))
    c.drawString(60, y_pos, "AI Scan Results / AI Jaanch Parinam")

    disease = scan_data.get("disease", "Healthy")
    confidence = scan_data.get("confidence", 0.95)
    is_healthy = disease.lower() == "healthy"

    y_pos -= 30
    c.setFont("Helvetica-Bold", 16)
    if is_healthy:
        c.setFillColor(HexColor("#16a34a"))
        c.drawString(60, y_pos, f"✅ Status: HEALTHY / SWASTH")
    else:
        c.setFillColor(HexColor("#dc2626"))
        c.drawString(60, y_pos, f"⚠ Disease Detected: {disease}")

    y_pos -= 25
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#1f2937"))
    c.drawString(60, y_pos, f"AI Confidence: {confidence * 100:.1f}%")

    y_pos -= 25
    c.drawString(60, y_pos, f"Model: ResNet50 (Mango Disease Detection)")

    y_pos -= 25
    c.drawString(60, y_pos, f"Variety / Kism: Dasheri")

    # Quality Grade
    y_pos -= 40
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#166534"))
    c.drawString(60, y_pos, "Quality Assessment / Gunvatta Mulyankan")

    y_pos -= 30
    c.setFont("Helvetica-Bold", 18)
    if is_healthy:
        c.setFillColor(HexColor("#16a34a"))
        c.drawString(60, y_pos, "Grade A — Premium Export Quality")
        y_pos -= 25
        c.setFont("Helvetica", 11)
        c.setFillColor(HexColor("#1f2937"))
        c.drawString(60, y_pos, "This batch is certified disease-free by AI analysis.")
        y_pos -= 20
        c.drawString(60, y_pos, "Yeh khaap AI jaanch se rog-mukt praman-it hai.")
    else:
        c.setFillColor(HexColor("#ea580c"))
        c.drawString(60, y_pos, "Requires Treatment — See Recommendations")

    # Generate QR Code
    qr_data = f"MangiferaShield|{certificate_id}|{disease}|{confidence:.2f}|{datetime.now().isoformat()}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#166534", back_color="white")

    # Save QR to buffer
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    from reportlab.lib.utils import ImageReader
    qr_image = ImageReader(qr_buffer)
    c.drawImage(qr_image, width - 180, 80, width=120, height=120)

    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#6b7280"))
    c.drawCentredString(width - 120, 65, "Scan for verification")

    # Footer
    c.setStrokeColor(HexColor("#22c55e"))
    c.setLineWidth(2)
    c.line(50, 50, width - 50, 50)

    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#6b7280"))
    c.drawCentredString(width / 2, 35, "Mangifera Shield — Protecting Malihabad's Mango Heritage with AI")
    c.drawCentredString(width / 2, 22, f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')} | This is an AI-generated certificate")

    c.save()
    buffer.seek(0)

    return buffer.getvalue(), certificate_id
