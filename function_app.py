import azure.functions as func
from wrapper_functions.imageCompressor import app as imagecompressor

# Create the main FunctionApp instance
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Middleware for file conversion
async def image_compressor(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await func.AsgiMiddleware(imagecompressor).handle_async(req, context)

# Register the routes with the main FunctionApp
app.route(route="api/fileconversion", methods=["POST"])(image_compressor)