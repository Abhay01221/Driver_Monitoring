"""
Configuration for model training
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Check if UTA-RLDD dataset is available in kagglehub cache
KAGGLE_RLDD_PATH = Path.home() / ".cache" / "kagglehub" / "datasets" / "minhngt02" / "uta-rldd" / "versions" / "2"
if KAGGLE_RLDD_PATH.exists():
    # Use the Kaggle dataset directly
    print(f"✓ Using UTA-RLDD dataset from: {KAGGLE_RLDD_PATH}")
    DATA_DIR = KAGGLE_RLDD_PATH / "train"  # Use the training split
    
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# Dataset configuration
# UTA-RLDD Binary classification: active (alert) vs fatigue (drowsy)
ALERT_DIR = DATA_DIR / "active"
DROWSY_DIR = DATA_DIR / "fatigue"

# Legacy support
LOW_VIGILANT_DIR = DATA_DIR / "Low_Vigilant"
NON_DROWSY_DIR = DATA_DIR / "Non Drowsy"

IMG_SIZE = (224, 224)  # For transfer learning models
YOLO_IMG_SIZE = 640    # For YOLO

# Training configuration
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

# Model configuration
MODELS = {
    "mobilenet": {
        "base": "MobileNetV2",
        "img_size": (224, 224),
        "preprocess": "tf.keras.applications.mobilenet_v2.preprocess_input"
    },
    "efficientnet": {
        "base": "EfficientNetB0", 
        "img_size": (224, 224),
        "preprocess": "tf.keras.applications.efficientnet.preprocess_input"
    },
    "custom_cnn": {
        "base": None,
        "img_size": (145, 145),
        "preprocess": "normalize"
    },
    "yolo": {
        "base": "yolov8n-cls.pt",
        "img_size": 640,
        "preprocess": "yolo"
    }
}

# Data augmentation
AUGMENTATION_CONFIG = {
    "rotation_range": 15,
    "width_shift_range": 0.1,
    "height_shift_range": 0.1,
    "brightness_range": (0.8, 1.2),
    "horizontal_flip": True,
    "zoom_range": 0.1,
    "fill_mode": "nearest"
}

# Early stopping
EARLY_STOPPING_PATIENCE = 10
REDUCE_LR_PATIENCE = 5

# Class names
# UTA-RLDD (Binary): active (alert) vs fatigue (drowsy)  
CLASS_NAMES = ["Alert", "Drowsy"]

# For legacy compatibility
BINARY_CLASS_NAMES = ["Non_Drowsy", "Drowsy"]
