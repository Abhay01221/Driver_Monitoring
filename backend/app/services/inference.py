"""
Inference service - handles model predictions
"""
import numpy as np
from typing import Dict, List, Optional
from app.models.model import model_manager
from app.services.image_processing import preprocess_for_yolo
from app.services.cv_features import extract_all_cv_features, validate_cv_features
from app.services.eye_detection import detect_eye_closure
from app.services.temporal_analysis import get_temporal_analyzer
from app.utils.helpers import format_prediction


def predict_drowsiness(image: np.ndarray, conf_threshold: float = 0.25, 
                      extract_cv_features: bool = True,
                      detect_eyes: bool = True,
                      use_temporal: bool = True,
                      previous_frame: Optional[np.ndarray] = None) -> Dict:
    """
    Run drowsiness detection inference on an image
    
    Args:
        image: Input image (numpy array, BGR from OpenCV)
        conf_threshold: Confidence threshold
        extract_cv_features: Whether to extract CV features (HOG, Sobel, Optical Flow)
        detect_eyes: Whether to detect eye closure
        use_temporal: Whether to use temporal analysis for smoothing
        previous_frame: Previous frame for optical flow analysis
        
    Returns:
        Prediction results dictionary with:
        - label: Predicted class label
        - confidence: Confidence score
        - status: "drowsy" or "alert"
        - severity: Risk level
        - color: Status color
        - cv_features: CV metadata (if extract_cv_features=True)
        - eye_analysis: Eye closure analysis (if detect_eyes=True)
        - temporal_analysis: Temporal smoothing results (if use_temporal=True)
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
        
        # Format result (initial prediction)
        prediction = format_prediction(class_name, confidence)
        is_drowsy_raw = prediction['status'] == 'drowsy'
        
        # Add all class probabilities for debugging
        prediction['all_probs'] = {
            result.names[i]: float(probs.data[i]) 
            for i in range(len(probs.data))
        }
        
        # Detect eye closure if requested (Task 6 enhancement)
        eyes_closed = False
        if detect_eyes:
            try:
                eye_analysis = detect_eye_closure(image)
                prediction['eye_analysis'] = eye_analysis
                eyes_closed = eye_analysis.get('eyes_likely_closed', False)
                
                # Enhance drowsiness prediction with eye closure
                # If eyes are closed, increase drowsiness severity
                if eyes_closed:
                    if prediction['status'] == 'drowsy':
                        prediction['severity'] = 2  # Upgrade to danger
                        prediction['color'] = 'red'
                        prediction['eye_closure_detected'] = True
                    else:
                        # Model says alert but eyes closed - possible early warning
                        prediction['eye_closure_warning'] = True
            except Exception as e:
                print(f"Eye closure detection failed: {e}")
                prediction['eye_analysis'] = None
        
        # Temporal analysis for robustness (Task 6 enhancement)
        if use_temporal:
            try:
                analyzer = get_temporal_analyzer(buffer_size=10)
                analyzer.add_prediction(
                    is_drowsy=is_drowsy_raw,
                    confidence=confidence,
                    eyes_closed=eyes_closed
                )
                temporal_result = analyzer.analyze()
                prediction['temporal_analysis'] = temporal_result
                
                # Override prediction with temporally smoothed result
                smoothed_drowsy = temporal_result['smoothed_prediction']
                alert_level = temporal_result['temporal_alert_level']
                
                # Update status based on temporal analysis
                if smoothed_drowsy:
                    prediction['status'] = 'drowsy'
                    prediction['label'] = 'Drowsy'
                    
                    # Set severity based on alert level
                    if alert_level >= 3:
                        prediction['severity'] = 2  # Danger
                        prediction['color'] = 'red'
                    elif alert_level >= 2:
                        prediction['severity'] = 1  # Warning
                        prediction['color'] = 'yellow'
                    else:
                        prediction['severity'] = 1  # Warning
                        prediction['color'] = 'yellow'
                else:
                    prediction['status'] = 'alert'
                    prediction['label'] = 'Alert'
                    prediction['severity'] = 0
                    prediction['color'] = 'green'
                
                # Add temporal metadata
                prediction['temporal_smoothed'] = True
                prediction['raw_prediction'] = 'drowsy' if is_drowsy_raw else 'alert'
                
            except Exception as e:
                print(f"Temporal analysis failed: {e}")
                prediction['temporal_analysis'] = None
        
        # Extract CV features if requested (Task 6 requirement)
        if extract_cv_features:
            try:
                cv_metadata = extract_all_cv_features(image, previous_frame)
                cv_validation = validate_cv_features(cv_metadata)
                
                prediction['cv_features'] = cv_metadata
                prediction['cv_validation'] = cv_validation
            except Exception as e:
                print(f"CV feature extraction failed: {e}")
                prediction['cv_features'] = None
                prediction['cv_validation'] = None
        
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
