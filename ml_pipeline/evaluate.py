"""
Model evaluation script - YOLO only
"""
import argparse
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from ultralytics import YOLO
from pathlib import Path

import config
from data_prep import load_image_paths_and_labels, split_data


def evaluate_yolo_model(model_path: str, test_data_dir: Path) -> dict:
    """
    Evaluate YOLO model on test set
    
    Args:
        model_path: Path to YOLO weights
        test_data_dir: Path to test data
        
    Returns:
        Dictionary with metrics
    """
    print(f"Loading YOLO model from: {model_path}")
    model = YOLO(model_path)
    
    # Validate on test set
    results = model.val(data=str(test_data_dir.parent), split='test')
    
    return {
        'accuracy': results.results_dict.get('metrics/accuracy_top1', 0),
        'results': results
    }


def print_evaluation_results(results: dict):
    """
    Print evaluation results
    
    Args:
        results: Results dictionary
    """
    print(f"\n{'='*60}")
    print("Evaluation Results")
    print(f"{'='*60}\n")
    
    print(f"Overall Accuracy: {results['accuracy']:.4f}")
    
    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained model')
    parser.add_argument('--model-path', type=str, required=True,
                       help='Path to trained YOLO model (.pt)')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"YOLO Model Evaluation")
    print(f"{'='*60}\n")
    
    # YOLO evaluation
    yolo_data_dir = config.DATA_DIR / "yolo_dataset" / "test"
    results = evaluate_yolo_model(
        model_path=args.model_path,
        test_data_dir=yolo_data_dir
    )
    
    print_evaluation_results(results)
    print("Evaluation completed!")


if __name__ == "__main__":
    main()
