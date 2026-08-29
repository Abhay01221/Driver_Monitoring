"""
Prediction endpoint
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import sys

from app.services.image_processing import decode_image, validate_image
from app.services.inference import predict_drowsiness

router = APIRouter()
try:
    MAX_IMAGE_BYTES = max(1, int(os.getenv("MAX_IMAGE_BYTES", 10 * 1024 * 1024)))
except ValueError:
    MAX_IMAGE_BYTES = 10 * 1024 * 1024


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict drowsiness from uploaded image
    
    Args:
        file: Uploaded image file (JPEG, PNG)
        
    Returns:
        JSON with prediction results:
        {
            "label": "Drowsy" or "Non_Drowsy",
            "confidence": float (0-1),
            "status": "drowsy" or "alert",
            "all_probs": {class_name: probability}
        }
    """
    # Validate content type
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Only JPEG, PNG, and WebP are supported."
        )
    
    try:
        # Read file bytes
        file_bytes = await file.read()

        if len(file_bytes) > MAX_IMAGE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"Image is too large. Maximum size is {MAX_IMAGE_BYTES // (1024 * 1024)} MB."
            )
        
        # Validate image
        if not validate_image(file_bytes):
            raise HTTPException(
                status_code=400,
                detail="Invalid image file. Could not decode image."
            )
        
        # Decode image
        image = decode_image(file_bytes)
        
        # Run inference
        prediction = predict_drowsiness(image, conf_threshold=0.25)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "prediction": prediction
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error
        print(f"Error during prediction: {type(e).__name__}: {e}", file=sys.stderr)
        
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again."
        )
