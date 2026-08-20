"""
Inference service - handles model predictions
"""
import numpy as np
from typing import Dict, List
from app.models.model import model_manager
from app.services.image_processing import preprocess_for_yolo
from app.utils.helpers import format_prediction


def predict_drowsiness(image: np.ndarray, conf_threshold: float = 0.25) -> Dict:
    """
    Run drowsiness detection inference on an image
    
    Args:
        image: Input image (numpy array, BGR from OpenCV)
        conf_threshold: Confidence threshold
        
    Returns:
        Prediction results dictionary with:
        - label: Predicted class label
        - confidence: Confidence score
        - status: "drowsy" or "alert"
        - raw_results: Raw model output (optional)
    """
    # Get loaded model
    model = model_manager.get_model()
    
    # Preprocess image for YOLO (converts BGR -> RGB)
    img_rgb = preprocess_for_yolo(image)
    
    # Run inference
    results = model.predict(img_rgb, conf_threshold=conf_threshold)
    
    # Parse YOLO classification results
    # results[0] contains the first (and only) image result
    result = results[0]
    
    # For YOLO classification:
    # - result.probs contains the class probabilities
    # - result.probs.top1 is the predicted class index
    # - result.probs.top1conf is the confidence score
    # - result.names maps indices to class names
    
    if hasattr(result, 'probs') and result.probs is not None:
        probs = result.probs
        predicted_class_idx = int(probs.top1)
        confidence = float(probs.top1conf)
        
        # Get class name from model
        class_name = result.names[predicted_class_idx]
        
        # Format result
        prediction = format_prediction(class_name, confidence)
        
        # Add all class probabilities for debugging
        prediction['all_probs'] = {
            result.names[i]: float(probs.data[i]) 
            for i in range(len(probs.data))
        }
        
    else:
        # Fallback if probs not available
        prediction = {
            "label": "Unknown",
            "confidence": 0.0,
            "status": "unknown",
            "error": "No classification probabilities found"
        }
    
    return prediction


def batch_predict(images: List[np.ndarray], 
                  conf_threshold: float = 0.25) -> List[Dict]:
    """
    Run inference on multiple images
    
    Args:
        images: List of input images
        conf_threshold: Confidence threshold
        
    Returns:
        List of prediction dictionaries
    """
    results = []
    
    for image in images:
        try:
            result = predict_drowsiness(image, conf_threshold)
            results.append(result)
        except Exception as e:
            results.append({
                "label": "Error",
                "confidence": 0.0,
                "status": "error",
                "error": str(e)
            })
    
    return results
