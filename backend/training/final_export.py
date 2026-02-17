import os
import tensorflow as tf
import tensorflowjs as tfjs
from tf_keras.models import load_model

# Paths
base_dir = os.path.dirname(os.path.dirname(__file__))
h5_path = os.path.join(base_dir, "model", "disease_detector.h5")
output_dir = os.path.join(base_dir, "..", "frontend", "models")

print(f"🔄 Loading {h5_path}...")
model = load_model(h5_path)

print(f"🔄 Converting to TF.js Layers Model...")
os.makedirs(output_dir, exist_ok=True)

# Export using programmatic API
tfjs.converters.save_keras_model(model, output_dir)

print(f"✅ Export complete! Files in {output_dir}")
print(os.listdir(output_dir))
