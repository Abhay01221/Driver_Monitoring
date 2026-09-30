
"""
Model training script for Driver Drowsiness Detection
Supports: YOLO (YOLOv8 classification)
"""
import argparse
from ultralytics import YOLO
import numpy as np
from pathlib import Path
import shutil

import config
from data_prep import (load_image_paths_and_labels, split_data, 
                       compute_class_weights, prepare_yolo_dataset)


def train_yolo_model(data_dir: Path, epochs: int, img_size: int):
    """
    Train YOLO classification model
    
    Args:
        data_dir: YOLO dataset directory
        epochs: Number of epochs
        img_size: Image size
    """
    print(f"\n{'='*50}")
    print(f"Training YOLO Classification Model...")
    print(f"{'='*50}\n")
    
    # Load pretrained YOLO classification model
    model = YOLO('yolov8n-cls.pt')
    
    # Train
    results = model.train(
        data=str(data_dir),
        epochs=epochs,
        imgsz=img_size,
        batch=config.BATCH_SIZE,
        name='drowsiness_detection',
        project=str(config.MODELS_DIR),
        patience=config.EARLY_STOPPING_PATIENCE,
        save=True,
        plots=True,
        verbose=True
    )
    
    # Copy best weights to standard location
    best_weights = config.MODELS_DIR / "drowsiness_detection" / "weights" / "best.pt"
    if best_weights.exists():
        shutil.copy2(best_weights, config.MODELS_DIR / "yolo_best.pt")
        print(f"✓ Best YOLO weights saved to: {config.MODELS_DIR / 'yolo_best.pt'}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Train drowsiness detection model')
    parser.add_argument('--model', type=str, default='yolo',
                       choices=['yolo'],
                       help='Model architecture to train (only YOLO supported)')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch size')
    parser.add_argument('--img-size', type=int, default=224,
                       help='Image size')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"Driver Drowsiness Detection - YOLO Training")
    print(f"{'='*60}\n")
    
    # Load data
    print("Loading dataset...")
    image_paths, labels = load_image_paths_and_labels(config.DATA_DIR)
    
    if len(image_paths) == 0:
        print("\n❌ No images found!")
        print(f"Dataset directory: {config.DATA_DIR}")
        print("\nTo download the dataset, run:")
        print("  python download_dataset.py")
        print("\nOr download manually from Kaggle:")
        print("  https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd")
        return
    
    # Split data
    data_splits = split_data(
        image_paths, labels,
        train_split=config.TRAIN_SPLIT,
        val_split=config.VAL_SPLIT,
        test_split=config.TEST_SPLIT,
        random_state=config.RANDOM_SEED
    )
    
    # Prepare YOLO dataset
    yolo_data_dir = prepare_yolo_dataset(data_splits)
    
    # Train YOLO
    results = train_yolo_model(
        data_dir=yolo_data_dir,
        epochs=args.epochs,
        img_size=args.img_size
    )
    
    print(f"\n{'='*60}")
    print("Training completed!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
