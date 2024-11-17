from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import io
import logging
from fastapi.middleware.cors import CORSMiddleware
from YOLOModel import yolomodel

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = yolomodel()

@app.post("/getawsicons")
async def root(architectureDiagram: UploadFile = File(...)) -> JSONResponse:
    try:
        # Validate file type
        if not architectureDiagram.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File must be an image"
            )
        
        image_data = await architectureDiagram.read()
        
        # Try to open and validate image
        try:
            image = Image.open(io.BytesIO(image_data))
            image.verify()  # Verify it's actually an image
            image = Image.open(io.BytesIO(image_data))  # Reopen after verify
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file"
            )

        # Run detection
        try:
            detections = [obj.to_dict() for obj in model.predict(image)]
        except Exception as e:
            logger.error(f"Unexpected error during detection: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

        # Return results
        return JSONResponse(
            content={"status": "success", "detections": detections},
            status_code=status.HTTP_200_OK
        )
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
    finally:
        # Clean up
        await architectureDiagram.close()