"""
🛡️ Mangifera Shield — AI Disease Detection Model Trainer
=========================================================
MobileNetV2 Transfer Learning for Mango Leaf Disease Classification.

Dataset: "Mango Leaf Disease Dataset" from Kaggle
Classes: Anthracnose, Bacterial Canker, Cutting Weevil, Die Back,
         Gall Midge, Healthy, Powdery Mildew, Sooty Mould

Usage:
    1. Download dataset from Kaggle:
       kaggle datasets download -d aman2000jaiswal/mango-leaf-disease-dataset
    
    2. Extract into backend/training/dataset/ with this structure:
       dataset/
         ├── Anthracnose/
         ├── Bacterial Canker/
         ├── Cutting Weevil/
         ├── Die Back/
         ├── Gall Midge/
         ├── Healthy/
         ├── Powdery Mildew/
         └── Sooty Mould/

    3. Run this script:
       python train_model.py

    4. Output:
       - backend/model/disease_detector.h5  (Keras model for backend)
       - backend/model/disease_detector.tflite  (TFLite for mobile)
       - frontend/models/model.json + *.bin  (TF.js for browser)
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG = {
    "dataset_dir": os.path.join(os.path.dirname(__file__), "dataset"),
    "backend_model_dir": os.path.join(os.path.dirname(__file__), "..", "model"),
    "frontend_model_dir": os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "models"),
    "img_size": (224, 224),
    "batch_size": 32,
    "epochs": 5,
    "learning_rate": 0.001,
    "fine_tune_epochs": 8,
    "fine_tune_lr": 0.0001,
    "validation_split": 0.2,
    "class_names": [
        "Anthracnose",
        "Bacterial Canker",
        "Cutting Weevil",
        "Die Back",
        "Gall Midge",
        "Healthy",
        "Powdery Mildew",
        "Sooty Mould"
    ]
}


def check_gpu():
    """Check and display available GPU."""
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPU available: {len(gpus)} device(s)")
        for gpu in gpus:
            print(f"   → {gpu.name}")
        # Prevent GPU memory fragmentation
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    else:
        print("⚠️ No GPU found. Training on CPU (will be slower).")
    return len(gpus) > 0


def verify_dataset():
    """Verify dataset directory structure."""
    dataset_dir = CONFIG["dataset_dir"]
    
    if not os.path.exists(dataset_dir):
        print(f"\n❌ Dataset directory not found: {dataset_dir}")
        print("\n📥 Download instructions:")
        print("   Option 1 — Kaggle CLI:")
        print("     pip install kaggle")
        print("     kaggle datasets download -d aman2000jaiswal/mango-leaf-disease-dataset")
        print(f"     Extract to: {dataset_dir}")
        print("\n   Option 2 — Manual download:")
        print("     Go to: https://www.kaggle.com/datasets/aman2000jaiswal/mango-leaf-disease-dataset")
        print("     Download ZIP → Extract all folders into dataset/")
        print(f"\n   Expected structure in {dataset_dir}:")
        for cls in CONFIG["class_names"]:
            print(f"     └── {cls}/  (folder with .jpg/.png images)")
        sys.exit(1)
    
    # Check each class folder
    found_classes = []
    total_images = 0
    
    for cls in CONFIG["class_names"]:
        cls_dir = os.path.join(dataset_dir, cls)
        if os.path.exists(cls_dir):
            imgs = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            found_classes.append(cls)
            total_images += len(imgs)
            print(f"   ✅ {cls}: {len(imgs)} images")
        else:
            print(f"   ❌ {cls}: folder MISSING!")
    
    if len(found_classes) < len(CONFIG["class_names"]):
        missing = set(CONFIG["class_names"]) - set(found_classes)
        print(f"\n⚠️  Missing classes: {missing}")
        print("    Training will proceed with available classes only.")
    
    print(f"\n📊 Total: {len(found_classes)} classes, {total_images} images")
    return found_classes, total_images


def create_datasets():
    """Create training and validation datasets with augmentation."""
    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    print("\n📦 Creating datasets...")

    # Training with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest',
        validation_split=CONFIG["validation_split"]
    )
    
    # Validation generator (no augmentation, just rescaling)
    val_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=CONFIG["validation_split"]
    )

    train_ds = train_datagen.flow_from_directory(
        CONFIG["dataset_dir"],
        target_size=CONFIG["img_size"],
        batch_size=CONFIG["batch_size"],
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=42
    )

    val_ds = val_datagen.flow_from_directory(
        CONFIG["dataset_dir"],
        target_size=CONFIG["img_size"],
        batch_size=CONFIG["batch_size"],
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )

    # Save class indices mapping
    class_indices = train_ds.class_indices
    print(f"\n📋 Class mapping: {class_indices}")
    
    return train_ds, val_ds, class_indices


def build_model(num_classes):
    """Build ResNet50 transfer learning model."""
    import tensorflow as tf
    from tensorflow.keras import layers, Model
    from tensorflow.keras.applications import ResNet50

    print(f"\n🧠 Building ResNet50 model ({num_classes} classes)...")

    # Load ResNet50 with ImageNet weights (without top)
    base_model = ResNet50(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers initially
    base_model.trainable = False

    # Add custom classification head
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs, name="MangiferaShield_ResNet50")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=CONFIG["learning_rate"]),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()
    return model, base_model


def train_model(model, base_model, train_ds, val_ds):
    """Train model with two phases: frozen base, then fine-tuning."""
    import tensorflow as tf

    # === Phase 1: Train classification head (base frozen) ===
    print("\n" + "=" * 60)
    print("📈 Phase 1: Training classification head...")
    print("=" * 60)

    callbacks_p1 = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            verbose=1
        )
    ]

    # Calculate class weights for imbalance handling
    print("\n⚖️ Calculating class weights...")
    train_labels = train_ds.classes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_labels),
        y=train_labels
    )
    class_indices = train_ds.class_indices
    # Convert to dictionary {0: 1.5, 1: 0.8, ...}
    class_weight_dict = dict(enumerate(class_weights))
    
    # Print weights for user to see
    labels_map = {v: k for k, v in class_indices.items()}
    for i, w in class_weight_dict.items():
        print(f"   Class {labels_map[i]}: {w:.2f}")

    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=CONFIG["epochs"],
        callbacks=callbacks_p1,
        class_weight=class_weight_dict,
        verbose=1
    )

    # === Phase 2: Fine-tune top layers of MobileNetV2 ===
    print("\n" + "=" * 60)
    print("🔧 Phase 2: Fine-tuning MobileNetV2 top layers...")
    print("=" * 60)

    # Unfreeze the top 30 layers of base model
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Re-compile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=CONFIG["fine_tune_lr"]),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks_p2 = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=8, # Increased patience for deep training
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            os.path.join(CONFIG["backend_model_dir"], "best_model.h5"),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2, # Aggressive reduction
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]

    history2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=CONFIG["fine_tune_epochs"],
        callbacks=callbacks_p2,
        class_weight=class_weight_dict,
        verbose=1
    )

    return history1, history2


def evaluate_model(model, val_ds, class_indices):
    """Evaluate model and print classification report."""
    print("\n" + "=" * 60)
    print("📊 Evaluating model...")
    print("=" * 60)

    loss, accuracy = model.evaluate(val_ds, verbose=1)
    print(f"\n🎯 Validation Accuracy: {accuracy * 100:.2f}%")
    print(f"📉 Validation Loss: {loss:.4f}")

    # Per-class accuracy
    try:
        from sklearn.metrics import classification_report
        import numpy as np

        val_ds.reset()
        predictions = model.predict(val_ds, verbose=1)
        y_pred = np.argmax(predictions, axis=1)
        y_true = val_ds.classes

        # Invert class_indices
        class_labels = {v: k for k, v in class_indices.items()}
        target_names = [class_labels[i] for i in range(len(class_labels))]

        report = classification_report(y_true, y_pred, target_names=target_names)
        print(f"\n📋 Classification Report:\n{report}")
    except ImportError:
        print("⚠️ Install scikit-learn for detailed report: pip install scikit-learn")

    return accuracy

def plot_confusion_matrix(model, val_ds, class_indices):
    """Generate and save confusion matrix."""
    print("\n📊 Generating Confusion Matrix...")
    val_ds.reset()
    predictions = model.predict(val_ds, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = val_ds.classes
    
    cm = confusion_matrix(y_true, y_pred)
    
    # Ensure plots directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=list(class_indices.keys()),
                yticklabels=list(class_indices.keys()))
    plt.title('Confusion Matrix (ResNet50)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    print(f"   ✅ Saved plots/confusion_matrix.png")


def save_models(model, class_indices):
    """Save model in all formats: H5, TFLite, and TF.js."""
    import tensorflow as tf

    os.makedirs(CONFIG["backend_model_dir"], exist_ok=True)
    os.makedirs(CONFIG["frontend_model_dir"], exist_ok=True)

    # === 1. Save Keras H5 model (for backend) ===
    h5_path = os.path.join(CONFIG["backend_model_dir"], "disease_detector.h5")
    model.save(h5_path)
    h5_size = os.path.getsize(h5_path) / (1024 * 1024)
    print(f"\n✅ Keras H5 saved: {h5_path} ({h5_size:.1f} MB)")

    # === 2. Save class labels ===
    labels_path = os.path.join(CONFIG["backend_model_dir"], "class_labels.json")
    labels = {str(v): k for k, v in class_indices.items()}
    with open(labels_path, 'w') as f:
        json.dump(labels, f, indent=2)
    print(f"✅ Class labels saved: {labels_path}")

    # Also save in frontend
    frontend_labels = os.path.join(CONFIG["frontend_model_dir"], "class_labels.json")
    with open(frontend_labels, 'w') as f:
        json.dump(labels, f, indent=2)

    # === 3. Convert to TFLite (for mobile) ===
    try:
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()

        tflite_path = os.path.join(CONFIG["backend_model_dir"], "disease_detector.tflite")
        with open(tflite_path, 'wb') as f:
            f.write(tflite_model)
        tflite_size = len(tflite_model) / (1024 * 1024)
        print(f"✅ TFLite saved: {tflite_path} ({tflite_size:.1f} MB)")
    except Exception as e:
        print(f"⚠️ TFLite conversion failed: {e}")

    # === 4. Convert to TensorFlow.js (for browser) ===
    try:
        import subprocess
        saved_model_dir = os.path.join(CONFIG["backend_model_dir"], "saved_model_temp")
        model.save(saved_model_dir)

        result = subprocess.run([
            sys.executable, '-m', 'tensorflowjs_converter',
            '--input_format=tf_saved_model',
            '--output_format=tfjs_graph_model',
            '--quantize_uint8', '*',
            saved_model_dir,
            CONFIG["frontend_model_dir"]
        ], capture_output=True, text=True)

        if result.returncode == 0:
            # Calculate total size of TF.js model files
            tfjs_files = os.listdir(CONFIG["frontend_model_dir"])
            tfjs_size = sum(os.path.getsize(os.path.join(CONFIG["frontend_model_dir"], f))
                          for f in tfjs_files) / (1024 * 1024)
            print(f"✅ TF.js model saved: {CONFIG['frontend_model_dir']} ({tfjs_size:.1f} MB)")
            print(f"   Files: {tfjs_files}")
        else:
            print(f"⚠️ TF.js conversion error: {result.stderr}")
            print("   Trying alternative conversion method...")
            convert_h5_to_tfjs(h5_path)

        # Cleanup temp saved model
        import shutil
        if os.path.exists(saved_model_dir):
            shutil.rmtree(saved_model_dir)
    except Exception as e:
        print(f"⚠️ TF.js conversion failed: {e}")
        print("   Run manually: python convert_to_tfjs.py")


def convert_h5_to_tfjs(h5_path):
    """Fallback: Convert H5 to TF.js using keras format."""
    import subprocess
    result = subprocess.run([
        sys.executable, '-m', 'tensorflowjs_converter',
        '--input_format=keras',
        '--quantize_uint8', '*',
        h5_path,
        CONFIG["frontend_model_dir"]
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ TF.js model saved (keras fallback): {CONFIG['frontend_model_dir']}")
    else:
        print(f"❌ TF.js conversion failed completely: {result.stderr}")


def main():
    print("=" * 60)
    print("🛡️  Mangifera Shield — AI Disease Model Trainer")
    print("   ResNet50 Transfer Learning (with Class Balancing)")
    print("=" * 60)

    # Step 1: Check GPU
    has_gpu = check_gpu()

    # Step 2: Verify dataset
    found_classes, total_images = verify_dataset()

    if total_images < 10:
        print("\n❌ Too few images. Need at least 10 images per class.")
        sys.exit(1)

    # Step 3: Create datasets
    train_ds, val_ds, class_indices = create_datasets()
    num_classes = len(class_indices)

    # Step 4: Build model
    model, base_model = build_model(num_classes)

    # Step 5: Train
    h1, h2 = train_model(model, base_model, train_ds, val_ds)

    # Step 6: Evaluate
    accuracy = evaluate_model(model, val_ds, class_indices)
    plot_confusion_matrix(model, val_ds, class_indices)

    # Step 7: Save all model formats
    save_models(model, class_indices)

    # Summary
    print("\n" + "=" * 60)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 60)
    print(f"   🎯 Final Accuracy: {accuracy * 100:.2f}%")
    print(f"   📁 Backend model: backend/model/disease_detector.h5")
    print(f"   📁 Frontend model: frontend/models/model.json")
    print(f"   📁 Class labels: backend/model/class_labels.json")
    print("\n   ✅ Restart the server → disease detection is now REAL!")
    print("=" * 60)


if __name__ == "__main__":
    main()
