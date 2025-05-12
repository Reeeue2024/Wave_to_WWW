# [ Server ] response.py

from fastapi.responses import JSONResponse

def success_response(data: dict, message: str = "The request was successfully processed."):
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(message: str = "An error occured while processing the request.", status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )
