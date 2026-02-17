"""
🛡️ Mangifera Shield — H5 to TF.js Converter
=============================================
Converts the trained Keras .h5 model to TensorFlow.js format for browser inference.

Usage:
    python convert_to_tfjs.py

Requires:
    pip install tensorflowjs
"""

import os
import sys
import subprocess

def convert():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    h5_path = os.path.join(base_dir, "model", "disease_detector.h5")
    output_dir = os.path.join(base_dir, "..", "frontend", "models")

    if not os.path.exists(h5_path):
        print(f"❌ Model file not found: {h5_path}")
        print("   Run train_model.py first!")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"🔄 Converting {h5_path} → TF.js format...")
    print(f"   Output: {output_dir}")

    # Method 1: Direct Keras conversion with quantization
    result = subprocess.run([
        sys.executable, '-m', 'tensorflowjs_converter',
        '--input_format=keras',
        '--quantize_uint8', '*',
        h5_path,
        output_dir
    ], capture_output=True, text=True)

    if result.returncode == 0:
        # List output files
        files = os.listdir(output_dir)
        total_size = sum(os.path.getsize(os.path.join(output_dir, f)) for f in files)
        print(f"\n✅ Conversion successful!")
        print(f"   Files: {files}")
        print(f"   Total size: {total_size / (1024*1024):.1f} MB")
        print(f"\n   Model is ready for browser inference!")
    else:
        print(f"❌ Conversion failed:\n{result.stderr}")
        print("\n   Trying SavedModel method...")

        # Method 2: Save as SavedModel first, then convert
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(h5_path)
            saved_dir = os.path.join(base_dir, "model", "saved_model_temp")
            model.save(saved_dir)

            result2 = subprocess.run([
                sys.executable, '-m', 'tensorflowjs_converter',
                '--input_format=tf_saved_model',
                '--output_format=tfjs_graph_model',
                '--quantize_uint8', '*',
                saved_dir,
                output_dir
            ], capture_output=True, text=True)

            if result2.returncode == 0:
                print("✅ Conversion successful (SavedModel method)!")
            else:
                print(f"❌ Both methods failed: {result2.stderr}")

            # Cleanup
            import shutil
            shutil.rmtree(saved_dir, ignore_errors=True)
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    convert()
