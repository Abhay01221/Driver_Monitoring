"""
Prediction endpoint
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import sys

from app.services.image_processing import decode_image, validate_image
from app.services.inference import predict_drowsiness

router = APIRouter()


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
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Only JPEG and PNG are supported."
        )
    
    try:
        # Read file bytes
        file_bytes = await file.read()
        
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
        print(f"Error during prediction: {str(e)}", file=sys.stderr)
        
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
