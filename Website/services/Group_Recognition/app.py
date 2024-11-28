import io
import logging
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from states import Group, detection_object
from YOLOModel import yolomodel
from RectangleDetector import detectRectangles

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

def get_dist(a,b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

@app.post("/getgroups")
async def root(architectureDiagram: UploadFile = File(...)) -> JSONResponse:
    try:
        # Validate file type
        if not architectureDiagram.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File must be an image [groups-service]"
            )
        
        image_data = await architectureDiagram.read()
        
        # Try to open and validate image
        try:
            image = Image.open(io.BytesIO(image_data))
            image.verify()  # Verify it's actually an image
            img_pillow = Image.open(io.BytesIO(image_data))  # Reopen after verify
            img_cv2 = cv2.cvtColor(np.array(img_pillow), cv2.COLOR_RGBA2BGR)
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file [groups-service]"
            )

        # Run category icon detection
        try:
            detections:detection_object = [obj for obj in model.predict(img_pillow)]
        except Exception as e:
            logger.error(f"Unexpected error during category icon detection: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error [groups-service]"
            )
        
        # Run rectangle detection
        try:
            rectangle_outlines = detectRectangles(img_cv2)
        except Exception as e:
            logger.error(f"Unexpected error during rectangle detection: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error [groups-service]"
            )

        # assign icons to rectangles
        detected_groups = []
        for det in detections:
            x, y = det.box[2:]
            selected_i = 0
            min_dist = np.inf
            for i, rect in enumerate(rectangle_outlines):
                dist = get_dist((x,y),rect[:2])
                if dist < min_dist:
                    min_dist = dist
                    selected_i = i
            rect = rectangle_outlines.pop(i)
            detected_groups.append(Group(*rect, group_type=det.classType))

        # add remaining rectangles without icons
        for rect in rectangle_outlines:
            detected_groups.append(Group(*rect))

        # Return results
        return JSONResponse(
            content={"status": "success", "groups": detected_groups},
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
            detail="An unexpected error occurred [groups-service]"
        )
    finally:
        # Clean up
        await architectureDiagram.close()