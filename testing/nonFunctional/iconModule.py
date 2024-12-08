import os
import uuid
import aiohttp
import asyncio
from pathlib import Path
import mimetypes

async def process_single_image(session, image_path, base_url):
    """Process a single architecture diagram image."""
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    
    # Read the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Create form data
    form_data = aiohttp.FormData()
    form_data.add_field('UUID', request_id)
    form_data.add_field(
        'ArchitectureDiagram',
        image_data,
        filename=os.path.basename(image_path),
        content_type=mimetypes.guess_type(image_path)[0] or 'application/octet-stream'
    )
    
    try:
        async with session.post(f"{base_url}/generateawstemplate", data=form_data) as response:
            if response.status == 200:
                result = await response.json()
                return {
                    'image_path': image_path,
                    'uuid': request_id,
                    'success': True,
                    'result': result
                }
            else:
                return {
                    'image_path': image_path,
                    'uuid': request_id,
                    'success': False,
                    'error': f"HTTP {response.status}: {await response.text()}"
                }
    except Exception as e:
        return {
            'image_path': image_path,
            'uuid': request_id,
            'success': False,
            'error': str(e)
        }

async def process_folder(folder_path, base_url="http://localhost:8000"):
    """Process all images in the specified folder."""
    # Supported image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    
    # Get all image files from the folder
    image_files = [
        f for f in Path(folder_path).iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        print(f"No image files found in {folder_path}")
        return []
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            process_single_image(session, str(image_path), base_url)
            for image_path in image_files
        ]
        results = await asyncio.gather(*tasks)
    
    # Process and display results
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\nProcessed {len(results)} files:")
    print(f"✓ Successful: {len(successful)}")
    print(f"✗ Failed: {len(failed)}")
    
    if failed:
        print("\nFailed conversions:")
        for f in failed:
            print(f"- {os.path.basename(f['image_path'])}: {f['error']}")
    
    return results

# Example usage
if __name__ == "__main__":
    # Replace with your folder path and API base URL
    FOLDER_PATH = "../aws_diagrams"
    BASE_URL = "http://localhost:8002"
    
    asyncio.run(process_folder(FOLDER_PATH, BASE_URL))