# 🛡️ Mangifera Shield — AI Model Training Guide

## Quick Start

### Step 1: Get the Dataset
Download from Kaggle: [Mango Leaf Disease Dataset](https://www.kaggle.com/datasets/aman2000jaiswal/mango-leaf-disease-dataset)

```bash
# Option A: Kaggle CLI
pip install kaggle
kaggle datasets download -d aman2000jaiswal/mango-leaf-disease-dataset
unzip mango-leaf-disease-dataset.zip -d backend/training/dataset/

# Option B: Manual download from Kaggle website
#   → Extract to backend/training/dataset/
```

Expected folder structure:
```
backend/training/dataset/
├── Anthracnose/
├── Bacterial Canker/
├── Cutting Weevil/
├── Die Back/
├── Gall Midge/
├── Healthy/
├── Powdery Mildew/
└── Sooty Mould/
```

### Step 2: Install Training Dependencies
```bash
pip install -r backend/training/requirements_training.txt
```

### Step 3: Train the Model
```bash
cd backend/training
python train_model.py
```

This will:
- **Phase 1**: Train classification head (base frozen) — 25 epochs
- **Phase 2**: Fine-tune top 30 MobileNetV2 layers — 10 epochs
- Auto-save 3 model formats:
  - `backend/model/disease_detector.h5` (backend)
  - `backend/model/disease_detector.tflite` (mobile)
  - `frontend/models/model.json` + `.bin` (browser)

### Step 4: Restart & Test
```bash
# Restart backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The app **automatically detects** the model:
- **Backend** → loads `.h5` model for `/api/disease/detect`
- **Frontend** → loads TF.js model from `/models/model.json` for offline scanning

## GPU Setup (Optional)

For faster training with CUDA-compatible GPU:
```bash
pip install tensorflow[and-cuda]==2.15.0
```

Expected training time:
| Hardware | Time |
|----------|------|
| CPU only | ~2 hours |
| NVIDIA GPU (e.g. T4) | ~15 minutes |
| Google Colab free GPU | ~20 minutes |

## Manual TF.js Conversion

If auto-conversion failed during training:
```bash
cd backend/training
python convert_to_tfjs.py
```
