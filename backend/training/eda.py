"""
🛡️ Mangifera Shield — Exploratory Data Analysis (EDA)
======================================================
Generates visual insights from the Mango Leaf Disease Dataset.
Outputs:
- class_distribution.png: Bar chart of image counts
- pixel_intensity.png: Histogram of pixel values
- sample_images.png: Grid of sample images from each class

Usage:
    python eda.py
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from PIL import Image

# Configuration
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
print(f"DEBUG: DATASET_DIR = {DATASET_DIR}")
print(f"DEBUG: Exists? {os.path.exists(DATASET_DIR)}")
if os.path.exists(DATASET_DIR):
    print(f"DEBUG: Contents: {os.listdir(DATASET_DIR)}")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "plots")
CLASS_NAMES = [
    "Anthracnose", "Bacterial Canker", "Cutting Weevil", "Die Back",
    "Gall Midge", "Healthy", "Powdery Mildew", "Sooty Mould"
]

def check_dataset():
    if not os.path.exists(DATASET_DIR):
        print(f"❌ Dataset not found at {DATASET_DIR}")
        print("   Please download dataset first (see train_model.py)")
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📂 Dataset found. Saving plots to {OUTPUT_DIR}/")

def plot_class_distribution():
    print("📊 Generating class distribution plot...")
    counts = {}
    for cls in CLASS_NAMES:
        path = os.path.join(DATASET_DIR, cls)
        if os.path.exists(path):
            counts[cls] = len([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png'))])
        else:
            counts[cls] = 0
            
    df = pd.DataFrame(list(counts.items()), columns=['Class', 'Count'])
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Count', y='Class', data=df, palette='viridis', hue='Class', legend=False)
    plt.title('Mango Leaf Disease Dataset Distribution')
    plt.xlabel('Number of Images')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "class_distribution.png"))
    print(f"   ✅ Saved class_distribution.png (Total: {sum(counts.values())} images)")
    return counts

def plot_sample_images():
    print("🖼️ Generatig sample images grid...")
    plt.figure(figsize=(15, 8))
    
    for i, cls in enumerate(CLASS_NAMES):
        path = os.path.join(DATASET_DIR, cls)
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png'))]
            if files:
                img_path = os.path.join(path, files[0])
                img = Image.open(img_path)
                plt.subplot(2, 4, i+1)
                plt.imshow(img)
                plt.title(f"{cls}\n({len(files)} images)")
                plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "sample_images.png"))
    print("   ✅ Saved sample_images.png")

def plot_pixel_intensity():
    print("📈 Generating pixel intensity histogram (from random sample)...")
    pixel_values = []
    
    # Sample 5 images from each class
    for cls in CLASS_NAMES:
        path = os.path.join(DATASET_DIR, cls)
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png'))]
            import random
            sample = random.sample(files, min(len(files), 5))
            for f in sample:
                img = Image.open(os.path.join(path, f)).resize((224, 224))
                pixel_values.extend(np.array(img).flatten())
    
    plt.figure(figsize=(10, 6))
    sns.histplot(pixel_values, bins=50, color='green', kde=True)
    plt.title('Pixel Intensity Distribution (Global)')
    plt.xlabel('Pixel Value (0-255)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(OUTPUT_DIR, "pixel_intensity.png"))
    print("   ✅ Saved pixel_intensity.png")

if __name__ == "__main__":
    check_dataset()
    plot_class_distribution()
    plot_sample_images()
    plot_pixel_intensity()
    print("\n🎉 EDA Complete! Visualizations saved in backend/training/plots/")
