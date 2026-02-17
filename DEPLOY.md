# 🚀 Deployment Guide: How to Clone & Run

Follow these steps to set up **Mangifera Shield** on a new laptop/server in 5 minutes.

## 1. Clone the Repository
Open your terminal (Command Prompt/PowerShell) and run:
```bash
git clone <your-github-repo-url>
cd Dasheri-Sentinal
```

## 2. Install Dependencies
Run this command to install all required libraries:
```bash
pip install -r backend/requirements.txt
```

## 3. 🧠 Restore AI Model (Automatic via Git LFS)
The AI model (`disease_detector.h5`) is large (220MB) and is stored using **Git LFS**.

### If you have Git LFS installed:
It will download automatically when you clone. Verification:
```bash
ls -lh backend/model/disease_detector.h5
# Should be ~220MB
```

### If you don't have Git LFS:
1.  Install it: `git lfs install`
2.  Pull the model: `git lfs pull`

*If you skip this, the backend will still run but will use "Color Analysis" fallback instead of Deep Learning.*

## 4. Run the App
Simply run the one-click start script:
```bash
python run_app.py
```
*   **Frontend:** Open [http://localhost:8000](http://localhost:8000)
*   **API Docs:** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## 5. (Optional) Enable Live Data
The app runs in "Demo Mode" by default. To enable live weather/mandi rates:
1.  Rename `.env.example` to `.env`.
2.  Add your API keys inside `.env`.
