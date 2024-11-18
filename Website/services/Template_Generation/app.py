from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import List
import httpx
import asyncio
from CodeGenerator import template_generator
import logging
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

app = FastAPI()
generator = template_generator()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class ClassList(BaseModel):
    file_name: str
    all_types: List[str]

class ServiceResponse(BaseModel):
    file_name: str
    status: int
    response: Dict[str, Any]

class ErrorResponse(BaseModel):
    error: str
    timestamp: str
    request_id: str

# Custom exceptions
class ServiceConnectionError(Exception):
    pass

class ServiceTimeoutError(Exception):
    pass

class ServiceResponseError(Exception):
    pass

# Configuration
class ServiceConfig:
    ICON_SERVICE_URL = "http://0.0.0.0:8000/getawsicons"
    LLM_SERVICE_URL = "http://0.0.0.0:8001/getllmsuggestion"
    TIMEOUT = 30.0  # seconds
    MAX_RETRIES = 3
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Retry decorator for service calls
@retry(
    stop=stop_after_attempt(ServiceConfig.MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_cls=ServiceConnectionError
)
async def make_service_call(
    client: httpx.AsyncClient,
    url: str,
    method: str = "POST",
    **kwargs
) -> Dict:
    """Make HTTP calls to other services with retry logic"""
    try:
        response = await client.request(
            method,
            url,
            timeout=ServiceConfig.TIMEOUT,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException as e:
        raise ServiceTimeoutError(f"Service timeout: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise ServiceResponseError(f"Service error: {str(e)}")
    except httpx.RequestError as e:
        raise ServiceConnectionError(f"Connection error: {str(e)}")

async def generate_template(
    file: UploadFile,
    uuid: str,
    generator: Any
) -> Dict[str, Any]:
    """Process a single diagram through the service chain"""
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > ServiceConfig.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large"
        )

    try:
        async with httpx.AsyncClient() as client:
            # Call icon service
            icon_response = await make_service_call(
                client,
                ServiceConfig.ICON_SERVICE_URL,
                files={"architectureDiagram": (file.filename, file_content, file.content_type)}
            )
            
            if not icon_response.get("detections"):
                raise ServiceResponseError("Invalid response from icon service")
            
            icon_detection_types = [det["classType"] for det in icon_response["detections"]]
            print(icon_detection_types)

            # Call LLM service
            llm_response = await make_service_call(
                client,
                ServiceConfig.LLM_SERVICE_URL,
                json={"items": icon_detection_types}
            )
            
            if not llm_response.get("message"):
                raise ServiceResponseError("Invalid response from LLM service")

            # Generate template
            try:
                combined_messages = icon_detection_types + llm_response["message"]
                template_response = await asyncio.to_thread(
                    generator.create_template,
                    file.filename,
                    combined_messages
                )
            except Exception as e:
                logger.error(f"Template generation error: {str(e)}")
                raise ServiceResponseError("Template generation failed")

            return {
                "file_name": file.filename,
                "status": status.HTTP_200_OK,
                "response": template_response
            }

    except (ServiceConnectionError, ServiceTimeoutError, ServiceResponseError) as e:
        logger.error(f"Service chain error for {file.filename}: {str(e)}")
        return {
            "file_name": file.filename,
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "response": {"error": str(e)}
        }


@app.post("/generateawstemplate")
async def upload_architecture_diagrams(
    UUID: str = Form(...),
    ArchitectureDiagram: UploadFile = File(...),
):
    try:
        # Basic input validation
        if not ArchitectureDiagram.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File must be an image"
            )

        # Generate Template
        result = await generate_template(ArchitectureDiagram, UUID, generator)
        
        return JSONResponse(
            content={
                "request_id": UUID,
                "timestamp": str(datetime.now(timezone.utc)),
                "results": [result]
            },
            status_code=result["status"]
        )

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            content=ErrorResponse(
                error="Invalid request data",
                timestamp=str(datetime.now(timezone.utc)),
                request_id=UUID
            ).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            content=ErrorResponse(
                error="Internal server error",
                timestamp=str(datetime.now(timezone.utc)),
                request_id=UUID
            ).model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )