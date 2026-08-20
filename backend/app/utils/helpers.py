"""
Utility helper functions
"""
import os
from typing import Optional


def get_env_var(key: str, default: Optional[str] = None) -> str:
    """
    Get environment variable with optional default
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set")
    return value


def format_prediction(label: str, confidence: float) -> dict:
    """
    Format prediction result consistently
    
    Args:
        label: Prediction label
        confidence: Confidence score (0-1)
        
    Returns:
        Formatted prediction dictionary
    """
    return {
        "label": label,
        "confidence": round(float(confidence), 4),
        "status": "drowsy" if "drowsy" in label.lower() else "alert"
    }
