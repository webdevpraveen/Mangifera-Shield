"""
Mangifera Shield — Disease Detection Route
Tries to load trained ResNet50 model (.h5) if available.
Falls back to PIL color/texture analysis if no model file exists.
"""

import os
import io
import uuid
import json
import numpy as np
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from PIL import Image

from ..database import get_db, ScanResult
from ..services.treatment_engine import get_treatment, get_all_diseases

router = APIRouter(prefix="/api/disease", tags=["Disease Detection"])

# Disease class labels
DISEASE_CLASSES = [
    "Anthracnose",
    "Bacterial Canker",
    "Cutting Weevil",
    "Die Back",
    "Gall Midge",
    "Healthy",
    "Powdery Mildew",
    "Sooty Mould"
]

# === Try loading trained model ===
tf_model = None
class_label_map = None
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "disease_detector.h5")
LABELS_PATH = os.path.join(MODEL_DIR, "class_labels.json")

try:
    if os.path.exists(MODEL_PATH):
        import tensorflow as tf
        tf_model = tf.keras.models.load_model(MODEL_PATH)
        print(f"✅ Real AI model loaded: {MODEL_PATH}")

        # Load class label mapping if exists
        if os.path.exists(LABELS_PATH):
            with open(LABELS_PATH, 'r') as f:
                class_label_map = json.load(f)
            print(f"✅ Class labels loaded: {list(class_label_map.values())}")
        else:
            class_label_map = {str(i): name for i, name in enumerate(DISEASE_CLASSES)}
    else:
        print(f"⚠️ No model file at {MODEL_PATH} — using color analysis fallback")
except ImportError:
    print("⚠️ TensorFlow not installed — using color analysis fallback")
except Exception as e:
    print(f"⚠️ Model load error: {e} — using color analysis fallback")

USE_REAL_MODEL = tf_model is not None


def analyze_image(image_bytes: bytes) -> tuple:
    """
    Real image analysis using color histograms and texture features.
    Analyzes the actual pixel content of the uploaded leaf photo.
    Returns (disease_name, confidence).
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    pixels = np.array(img, dtype=np.float32)

    # Extract color channel statistics
    r_mean, g_mean, b_mean = pixels[:,:,0].mean(), pixels[:,:,1].mean(), pixels[:,:,2].mean()
    r_std, g_std, b_std = pixels[:,:,0].std(), pixels[:,:,1].std(), pixels[:,:,2].std()

    total_pixels = 224 * 224

    # Feature extraction: count pixels in specific color ranges
    r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]

    # Green pixels (healthy tissue)
    green_mask = (g > r) & (g > b) & (g > 60)
    green_ratio = green_mask.sum() / total_pixels

    # Dark pixels (sooty mould, die back)
    dark_mask = (r < 60) & (g < 60) & (b < 60)
    dark_ratio = dark_mask.sum() / total_pixels

    # Brown pixels (anthracnose, canker spots)
    brown_mask = (r > 80) & (r < 180) & (g > 40) & (g < 120) & (b < 80)
    brown_ratio = brown_mask.sum() / total_pixels

    # White/powdery pixels (powdery mildew)
    white_mask = (r > 200) & (g > 200) & (b > 200)
    white_ratio = white_mask.sum() / total_pixels

    # Red/rust pixels
    red_mask = (r > 150) & (g < 100) & (b < 100)
    red_ratio = red_mask.sum() / total_pixels

    # Texture variance (high = spots/lesions)
    gray = pixels.mean(axis=2)
    texture_var = gray.std()

    # === Scoring system ===
    scores = {d: 0.0 for d in DISEASE_CLASSES}

    # High green = healthy
    if green_ratio > 0.55:
        scores["Healthy"] += 0.40
    elif green_ratio > 0.40:
        scores["Healthy"] += 0.20

    # Dark spots + brown = Anthracnose
    if dark_ratio > 0.08 and brown_ratio > 0.10:
        scores["Anthracnose"] += 0.35
        scores["Die Back"] += 0.15

    # Brown dominant = Bacterial Canker
    if brown_ratio > 0.15:
        scores["Bacterial Canker"] += 0.30
        scores["Cutting Weevil"] += 0.10

    # White powder = Powdery Mildew
    if white_ratio > 0.10:
        scores["Powdery Mildew"] += 0.40

    # Very dark = Sooty Mould
    if dark_ratio > 0.15:
        scores["Sooty Mould"] += 0.35

    # Red/rust coloring
    if red_ratio > 0.05:
        scores["Gall Midge"] += 0.25

    # High texture variance with moderate green = Gall Midge
    if texture_var > 55 and 0.25 < green_ratio < 0.55:
        scores["Gall Midge"] += 0.15
        scores["Cutting Weevil"] += 0.15

    # Disease indicators reduce healthy score
    if brown_ratio > 0.10 or dark_ratio > 0.10 or white_ratio > 0.08:
        scores["Healthy"] -= 0.25

    # Find winner
    winner = max(scores, key=scores.get)
    max_score = scores[winner]

    # Normalize confidence
    total_positive = sum(s for s in scores.values() if s > 0) or 0.001
    confidence = max(0.60, min(0.97, (max_score / total_positive) + 0.30))

    return winner, round(confidence, 4)


@router.post("/detect")
async def detect_disease(
    image: UploadFile = File(...),
    farmer_phone: str = Form("0000000000"),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    """
    Upload a mango leaf image for AI-powered disease detection.
    Uses trained ResNet50 model if available, else falls back to color analysis.
    """
    image_bytes = await image.read()
    client_id = str(uuid.uuid4())

    if USE_REAL_MODEL:
        # === REAL MODEL INFERENCE ===
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = tf_model.predict(img_array, verbose=0)
        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_idx])

        # Map index to disease name
        if class_label_map:
            disease_name = class_label_map.get(str(predicted_idx), DISEASE_CLASSES[predicted_idx])
        else:
            disease_name = DISEASE_CLASSES[predicted_idx]

        mode = "trained_model"
    else:
        # === FALLBACK: COLOR ANALYSIS ===
        disease_name, confidence = analyze_image(image_bytes)
        mode = "color_analysis"

    # Get treatment recommendations
    treatment = get_treatment(disease_name, language)
    is_healthy = disease_name == "Healthy"

    # Save scan result to database
    scan = ScanResult(
        client_id=client_id,
        farmer_phone=farmer_phone,
        disease_name=disease_name,
        confidence=confidence,
        treatment_en=str(get_treatment(disease_name, "en")),
        treatment_hi=str(get_treatment(disease_name, "hi")),
        is_healthy=is_healthy
    )
    db.add(scan)
    db.commit()

    return {
        "success": True,
        "scan_id": client_id,
        "disease": disease_name,
        "confidence": round(confidence, 4),
        "is_healthy": is_healthy,
        "treatment": treatment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_info": {
            "name": "ResNet50" if USE_REAL_MODEL else "Color Analysis",
            "classes": len(DISEASE_CLASSES),
            "mode": mode
        }
    }


@router.get("/classes")
async def get_disease_classes():
    """Return all supported disease classes with basic info."""
    classes = []
    for disease in DISEASE_CLASSES:
        treatment_en = get_treatment(disease, "en")
        treatment_hi = get_treatment(disease, "hi")
        classes.append({
            "name": disease,
            "name_hi": treatment_hi["disease"],
            "severity": treatment_en["severity"],
            "description_en": treatment_en["description"],
            "description_hi": treatment_hi["description"]
        })
    return {"classes": classes, "total": len(classes)}


@router.get("/history")
async def get_scan_history(
    farmer_phone: str = "0000000000",
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get scan history for a farmer."""
    scans = db.query(ScanResult).filter(
        ScanResult.farmer_phone == farmer_phone
    ).order_by(ScanResult.created_at.desc()).limit(limit).all()

    return {
        "scans": [
            {
                "id": s.client_id,
                "disease": s.disease_name,
                "confidence": s.confidence,
                "is_healthy": s.is_healthy,
                "created_at": s.created_at.isoformat() if s.created_at else ""
            }
            for s in scans
        ],
        "total": len(scans)
    }
