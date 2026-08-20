# ML Pipeline - Driver Drowsiness Detection

Training pipeline for drowsiness detection models.

## 📊 Dataset

**Source:** [Driver Drowsiness Dataset (DDD)](https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd)

**Classes:**
- Drowsy
- Non Drowsy

**Download using kagglehub (RECOMMENDED):**

```bash
cd ml_pipeline

# Install kagglehub
pip install kagglehub

# Download dataset (easiest method)
python download_dataset.py
```

**OR download using Kaggle CLI:**

```bash
# Install Kaggle CLI
pip install kaggle

# Setup Kaggle API credentials
# 1. Go to https://www.kaggle.com/settings/account
# 2. Click "Create New API Token"
# 3. Save kaggle.json to ~/.kaggle/kaggle.json (Linux/Mac) or %USERPROFILE%\.kaggle\kaggle.json (Windows)

# Download dataset
kaggle datasets download -d ismailnasri20/driver-drowsiness-dataset-ddd

# Extract
unzip driver-drowsiness-dataset-ddd.zip -d data/
```

**Expected structure:**
```
ml_pipeline/
└── data/
    ├── Drowsy/
    │   ├── img1.jpg
    │   ├── img2.jpg
    │   └── ...
    └── Non Drowsy/
        ├── img1.jpg
        ├── img2.jpg
        └── ...
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ml_pipeline
pip install -r requirements.txt
```

### 2. Download Dataset (Easiest Method)

```bash
# Using kagglehub (recommended)
python download_dataset.py
```

This will:
- Download the dataset from Kaggle (first-time authentication required)
- Automatically organize it in the correct structure
- Show you the dataset statistics

**Alternative methods:**
- Use Kaggle CLI: `kaggle datasets download -d ismailnasri20/driver-drowsiness-dataset-ddd`
- Manual download from Kaggle website

### 3. Quick Start Training (Interactive)

```bash
# Easiest way - interactive script
python quickstart_training.py
```

This script will:
1. Check/download dataset
2. Let you choose model type
3. Configure training parameters
4. Start training
5. Copy weights to backend automatically

### 4. Manual Training

Or train manually with specific parameters:

#### Option A: Transfer Learning (Recommended)

```bash
# MobileNetV2 (fast, 95%+ accuracy)
python train.py --model mobilenet --epochs 50 --batch-size 32

# EfficientNetB0 (slower, higher accuracy)
python train.py --model efficientnet --epochs 50 --batch-size 32
```

#### Option B: Custom CNN

```bash
python train.py --model custom_cnn --epochs 100 --batch-size 32
```

#### Option C: YOLO Classification (Current Implementation)

```bash
python train.py --model yolo --epochs 100 --img-size 640 --batch-size 32
```

### 4. Evaluate Model

```bash
# Keras models
python evaluate.py --model-path models/mobilenet_best.h5 --model-type keras

# YOLO models
python evaluate.py --model-path models/yolo_best.pt --model-type yolo
```

### 5. Deploy Model

```bash
# Copy trained weights to backend
cp models/yolo_best.pt ../backend/weights/best.pt

# Or for Keras models, convert to ONNX/TFLite first
```

## 📁 Project Structure

```
ml_pipeline/
├── data/                  # Dataset (downloaded)
│   ├── Drowsy/
│   ├── Non Drowsy/
│   └── yolo_dataset/     # Auto-generated for YOLO
├── models/                # Saved trained models
│   ├── mobilenet_best.h5
│   ├── yolo_best.pt
│   └── ...
├── outputs/               # Training plots and metrics
│   ├── mobilenet_training_history.png
│   ├── confusion_matrix.png
│   └── roc_curve.png
├── config.py             # Training configuration
├── data_prep.py          # Data loading and preprocessing
├── train.py              # Training script
├── evaluate.py           # Evaluation script
└── requirements.txt
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Image sizes
IMG_SIZE = (224, 224)      # For transfer learning
YOLO_IMG_SIZE = 640        # For YOLO

# Training
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Data splits
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

# Early stopping
EARLY_STOPPING_PATIENCE = 10
REDUCE_LR_PATIENCE = 5
```

## 🎯 Model Comparison

| Model | Size | Params | Accuracy | Inference Speed (CPU) | Best For |
|-------|------|--------|----------|----------------------|----------|
| MobileNetV2 | ~14MB | ~3.5M | 95-97% | ~50ms | Production (balanced) |
| EfficientNetB0 | ~29MB | ~5.3M | 96-98% | ~80ms | High accuracy |
| Custom CNN | ~4MB | ~1M | 92-94% | ~30ms | Edge devices |
| YOLOv8n-cls | ~6MB | ~2.7M | 93-96% | ~40ms | Detection pipelines |

## 📊 Training Process

### Data Pipeline

1. **Load Images:** Read from directory structure
2. **Split Data:** 70% train, 15% val, 15% test (stratified)
3. **Preprocessing:**
   - Resize to target size
   - Normalize to [0, 1]
   - Convert to RGB
4. **Augmentation (training only):**
   - Horizontal flip
   - Random brightness (±20%)
   - Random contrast (±20%)
   - Slight rotation (±15°)

### Training Strategy

#### Transfer Learning:
1. **Phase 1:** Freeze base, train head (5-10 epochs)
2. **Phase 2:** Fine-tune top layers (40-50 epochs)
3. **Optimizer:** Adam (lr=0.001)
4. **Loss:** Binary crossentropy
5. **Callbacks:**
   - Early stopping (patience=10)
   - Model checkpoint (save best)
   - Reduce LR on plateau (factor=0.5)

#### YOLO Training:
1. Start from YOLOv8n-cls pretrained weights
2. Fine-tune on DDD dataset
3. Automatic augmentation and hyperparameter tuning
4. Exports best weights to `.pt` format

## 📈 Evaluation Metrics

After training, evaluation generates:

### Classification Report
- Precision, Recall, F1-Score per class
- Macro/micro averages

### Confusion Matrix
- True positives/negatives
- False positives/negatives

### ROC Curve
- AUC score
- Optimal threshold analysis

### Output Files
- `outputs/confusion_matrix.png`
- `outputs/roc_curve.png`
- `outputs/{model}_training_history.png`

## 🔄 Model Export Formats

### Keras Models → ONNX (for production)

```python
import tf2onnx
import onnx

model = keras.models.load_model('models/mobilenet_best.h5')

# Convert to ONNX
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)
output_path = "models/mobilenet.onnx"

model_proto, _ = tf2onnx.convert.from_keras(model, 
    input_signature=spec, output_path=output_path)
```

### YOLO → Export

```python
from ultralytics import YOLO

model = YOLO('models/yolo_best.pt')

# Export to ONNX
model.export(format='onnx')

# Export to TensorFlow
model.export(format='saved_model')

# Export to TFLite (for mobile)
model.export(format='tflite')
```

## 🧪 Testing Inference

```python
# Test Keras model
import numpy as np
from tensorflow import keras
import cv2

model = keras.models.load_model('models/mobilenet_best.h5')

img = cv2.imread('test_image.jpg')
img = cv2.resize(img, (224, 224))
img = img / 255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img)
print(f"Drowsy probability: {pred[0][0]:.4f}")
```

```python
# Test YOLO model
from ultralytics import YOLO

model = YOLO('models/yolo_best.pt')
results = model('test_image.jpg')

for r in results:
    print(f"Class: {r.names[r.probs.top1]}")
    print(f"Confidence: {r.probs.top1conf:.4f}")
```

## 🐛 Troubleshooting

### Out of Memory (OOM)

```bash
# Reduce batch size
python train.py --model mobilenet --batch-size 16

# Or use smaller image size
# Edit config.py: IMG_SIZE = (128, 128)
```

### Poor Accuracy

1. **Check class balance:** Are classes imbalanced?
2. **Increase epochs:** Try 100+ epochs
3. **Better augmentation:** Add more data augmentation
4. **Try different model:** EfficientNet often gives better results
5. **Check data quality:** Remove corrupted/mislabeled images

### Training Too Slow

1. **Use GPU:** Install CUDA + cuDNN
2. **Reduce image size:** Use 128x128 or 145x145
3. **Use smaller model:** Custom CNN or MobileNetV2
4. **Reduce batch size:** But may affect convergence

### CUDA Out of Memory

```bash
# Mixed precision training (TensorFlow)
# Add to train.py:
from tensorflow.keras import mixed_precision
mixed_precision.set_global_policy('mixed_float16')

# Or reduce batch size
python train.py --batch-size 8
```

## 📚 Technologies

- **TensorFlow / Keras** - Deep learning framework
- **PyTorch** - For YOLO training
- **Ultralytics YOLO** - YOLO implementation
- **OpenCV** - Image processing
- **scikit-learn** - Metrics and evaluation
- **matplotlib / seaborn** - Visualization

## 🔮 Future Improvements

- [ ] Data augmentation with Albumentations
- [ ] Hyperparameter tuning with Optuna
- [ ] Model quantization for edge deployment
- [ ] Ensemble methods (combine multiple models)
- [ ] Active learning pipeline
- [ ] ONNX Runtime optimization
- [ ] TensorRT acceleration

## 📄 License

MIT

## 🙏 Acknowledgments

Dataset: [Ismail Nasri - Driver Drowsiness Dataset (DDD)](https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd)
