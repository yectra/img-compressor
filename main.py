from fastapi import FastAPI, File, UploadFile, Response
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

def compress_image(image_bytes):
    try:
        # Open the input image
        input_image = Image.open(io.BytesIO(image_bytes))

        # Convert image to JPEG format with compression
        output_image = io.BytesIO()
        input_image.convert("RGB").save(output_image, format="JPEG")
        output_image.seek(0)

        # Convert the output image to byte array
        byte_array = output_image.getvalue()

        return True, byte_array
    except Exception as e:
        return False, str(e)

@app.post("/compress")
async def compress(image: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_bytes = await image.read()

        # Compress the image
        success, compressed_image = compress_image(image_bytes)

        if success:
            return Response(content=compressed_image, media_type="image/jpeg")
        else:
            return {"error": "Failed to compress image"}
    except Exception as e:
        return {"error": str(e)}
