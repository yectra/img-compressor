from fastapi import FastAPI, File, UploadFile, Response
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

# Configure CORS settings
origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

def compress_image(image_bytes, quality=None, width=None, height=None):
    try:
        # Open the input image
        input_image = Image.open(io.BytesIO(image_bytes))

        # Resize the image if width and/or height are provided
        if width is not None and height is not None:
            input_image = input_image.resize((width, height))

        # Convert image to JPEG format with compression
        output_image = io.BytesIO()
        input_image.convert("RGB").save(output_image, format="JPEG", quality=quality)
        output_image.seek(0)

        # Convert the output image to byte array
        byte_array = output_image.getvalue()

        return True, byte_array
    except Exception as e:
        return False, str(e)
    
@app.post("/api/compress")
async def compress(image: UploadFile = File(...), quality: Optional[int] = None, width: Optional[int] = None, height: Optional[int] = None):
    try:
        # Read the uploaded image
        image_bytes = await image.read()

        # Compress the image
        success, compressed_image = compress_image(image_bytes, quality, width, height)

        if success:
            # Get the size of the original image in megabytes (MB)
            original_size_mb = len(image_bytes) / (1024 * 1024)  # Convert bytes to MB

            # Get the size of the compressed image in megabytes (MB)
            compressed_size_mb = len(compressed_image) / (1024 * 1024)  # Convert bytes to MB

            # Calculate the percentage reduction in size
            reduction_percentage = ((original_size_mb - compressed_size_mb) / original_size_mb) * 100

            # Return the compressed image data along with size reduction information
            return Response(content=compressed_image, media_type="image/jpeg", headers={
                "original_size": f"{original_size_mb:.2f} MB",
                "compressed_size": f"{compressed_size_mb:.2f} MB",
                "compression_percentage": f"{reduction_percentage:.2f}%"
            })
        else:
            return {"error": "Failed to compress image"}
    except Exception as e:
        print(e)
        return {"error": str(e)}