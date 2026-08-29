"""
Data preparation and loading utilities
"""
import os
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import config
from typing import Tuple, Dict
import shutil
import cv2


def load_image_paths_and_labels(data_dir: Path = None, num_classes: int = 2) -> Tuple[list, list]:
    """
    Load image paths and labels from directory structure
    
    For UTA-RLDD (2-class from Kaggle):
        data/
        ├── active/         (label 0 - Alert)
        └── fatigue/        (label 1 - Drowsy)
    
    For legacy binary classification:
        data/
        ├── Non Drowsy/     (label 0)
        └── Drowsy/         (label 1)
    
    Args:
        data_dir: Path to data directory. If None, uses config.DATA_DIR
        num_classes: Number of classes (2 or 3)
    
    Returns:
        image_paths: List of image file paths
        labels: List of labels
    """
    if data_dir is None:
        data_dir = config.DATA_DIR
    
    data_dir = Path(data_dir)
    image_paths = []
    labels = []
    
    # Try UTA-RLDD structure (active/fatigue)
    active_dir = data_dir / "active"
    fatigue_dir = data_dir / "fatigue"
    
    if active_dir.exists() and fatigue_dir.exists():
        # Load Active (Alert) - label 0
        for img_file in active_dir.glob("*.*"):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                image_paths.append(str(img_file))
                labels.append(0)
        
        # Load Fatigue (Drowsy) - label 1
        for img_file in fatigue_dir.glob("*.*"):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                image_paths.append(str(img_file))
                labels.append(1)
        
        if len(image_paths) > 0:
            print(f"✓ Found {len(image_paths)} images (UTA-RLDD format)")
            print(f"  - Active (Alert): {labels.count(0)}")
            print(f"  - Fatigue (Drowsy): {labels.count(1)}")
            return image_paths, labels
    
    # Try legacy binary classification structure
    possible_structures = [
        (data_dir / "Non Drowsy", data_dir / "Drowsy"),
        (data_dir / "Non_Drowsy", data_dir / "Drowsy"),
        (data_dir / "non_drowsy", data_dir / "drowsy"),
        (data_dir / "Alert", data_dir / "Drowsy"),
    ]
    
    non_drowsy_dir = None
    drowsy_dir = None
    
    for non_d, d in possible_structures:
        if non_d.exists() and d.exists():
            non_drowsy_dir = non_d
            drowsy_dir = d
            break
    
    if non_drowsy_dir and drowsy_dir:
        # Load Non Drowsy (label 0)
        for img_file in non_drowsy_dir.glob("*.*"):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                image_paths.append(str(img_file))
                labels.append(0)
        
        # Load Drowsy (label 1)
        for img_file in drowsy_dir.glob("*.*"):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                image_paths.append(str(img_file))
                labels.append(1)
        
        if len(image_paths) > 0:
            print(f"✓ Found {len(image_paths)} images (binary mode)")
            print(f"  - Non Drowsy: {labels.count(0)}")
            print(f"  - Drowsy: {labels.count(1)}")
            return image_paths, labels
    
    if len(image_paths) == 0:
        print(f"\n❌ No images found in {data_dir}")
        print(f"\nPlease run: python download_dataset.py")
    
    return image_paths, labels


def split_data(image_paths: list, labels: list, 
               train_split: float = 0.7,
               val_split: float = 0.15,
               test_split: float = 0.15,
               random_state: int = 42) -> Dict:
    """
    Split data into train/val/test sets with stratification
    
    Args:
        image_paths: List of image paths
        labels: List of labels
        train_split: Training set ratio
        val_split: Validation set ratio
        test_split: Test set ratio
        random_state: Random seed
        
    Returns:
        Dictionary with train/val/test splits
    """
    assert abs(train_split + val_split + test_split - 1.0) < 1e-5
    
    # First split: train vs (val + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        image_paths, labels,
        test_size=(val_split + test_split),
        random_state=random_state,
        stratify=labels
    )
    
    # Second split: val vs test
    val_ratio = val_split / (val_split + test_split)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=(1 - val_ratio),
        random_state=random_state,
        stratify=y_temp
    )
    
    print(f"\n✓ Data split:")
    print(f"  - Train: {len(X_train)} images")
    print(f"  - Val: {len(X_val)} images")
    print(f"  - Test: {len(X_test)} images")
    
    return {
        "train": (X_train, y_train),
        "val": (X_val, y_val),
        "test": (X_test, y_test)
    }


def compute_class_weights(labels: list) -> Dict[int, float]:
    """
    Compute class weights to handle imbalance
    
    Args:
        labels: List of training labels
        
    Returns:
        Dictionary mapping class index to weight
    """
    weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    
    class_weights = {i: w for i, w in enumerate(weights)}
    print(f"\n✓ Class weights: {class_weights}")
    
    return class_weights





def prepare_yolo_dataset(data_splits: Dict, output_dir: Path = None, num_classes: int = 3):
    """
    Prepare dataset in YOLO classification format
    
    YOLO expects:
        dataset/
        ├── train/
        │   ├── Alert/
        │   ├── Low_Vigilant/
        │   └── Drowsy/
        ├── val/
        │   ├── Alert/
        │   ├── Low_Vigilant/
        │   └── Drowsy/
        └── test/
            ├── Alert/
            ├── Low_Vigilant/
            └── Drowsy/
    
    Args:
        data_splits: Dictionary from split_data()
        output_dir: Output directory (default: data/yolo_dataset)
        num_classes: Number of classes (2 or 3)
    """
    if output_dir is None:
        output_dir = config.DATA_DIR / "yolo_dataset"
    
    output_dir.mkdir(exist_ok=True)
    
    # Select appropriate class names
    class_names = config.CLASS_NAMES if num_classes == 3 else config.BINARY_CLASS_NAMES
    
    for split_name, (paths, labels) in data_splits.items():
        print(f"\n✓ Preparing YOLO {split_name} set...")
        
        split_dir = output_dir / split_name
        split_dir.mkdir(exist_ok=True)
        
        # Create class directories
        for class_name in class_names:
            class_dir = split_dir / class_name
            class_dir.mkdir(exist_ok=True)
        
        # Copy images to respective class folders
        for img_path, label in zip(paths, labels):
            class_name = class_names[label]
            dest_dir = split_dir / class_name
            
            img_file = Path(img_path)
            dest_path = dest_dir / img_file.name
            
            # Copy file
            shutil.copy2(img_path, dest_path)
    
    print(f"\n✓ YOLO dataset created at: {output_dir}")
    return output_dir


if __name__ == "__main__":
    # Test data loading
    print("Testing data preparation with UTA-RLDD dataset...")
    
    image_paths, labels = load_image_paths_and_labels(config.DATA_DIR, num_classes=2)
    
    if len(image_paths) == 0:
        print("\n⚠ No images found!")
        print(f"Please download the dataset to: {config.DATA_DIR}")
        print("\nRun: python download_dataset.py")
    else:
        num_classes = len(set(labels))
        print(f"\n✓ Loaded dataset with {num_classes} classes")
        
        data_splits = split_data(image_paths, labels)
        class_weights = compute_class_weights(data_splits["train"][1])
        
        # Prepare YOLO dataset
        yolo_dir = prepare_yolo_dataset(data_splits, num_classes=num_classes)
        print(f"\n✓ YOLO dataset prepared successfully")
        print(f"  - Location: {yolo_dir}")
