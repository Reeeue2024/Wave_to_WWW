# [ Server ] main.py (db-linked + extension ver.)
# source/server/app/main.py

from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from server.sessions.sessions import store_result, get_result
from server.app.utils.response import success_response, error_response
from server.app.utils.logger import logger
from server.app.schemas.request_schema import UrlDetectRequest
from configs.config import ALLOWED_ORIGINS
from core_engine.kernel_service import KernelService
from core_engine.kernel_resource import kernel_resource_instance
from server.app.db_connector import check_url_in_db, insert_url_result
import uuid
import time
import json

app = FastAPI()

@app.on_event("startup")
def load_kernel_resources():
    kernel_resource_instance.load_resource()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프론트엔드 정적 파일 서빙
app.mount("/static", StaticFiles(directory="web/gui"), name="static")

# 루트 엔드포인트
@app.get("/")
def root():
    return success_response({}, message="Backend is running")

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    return success_response({
        "status": "ok",
        "message": "Backend is running"
    })

# 탐지 실행 엔드포인트
@app.post("/detect/url")
async def detect_url(
    request: Request,
    data: UrlDetectRequest = Body(...)
):
    url = str(data.url)

    # 클라이언트 타입 판별 (기본: web)
    client_type = request.headers.get("client-type", "web").lower()
    if client_type not in ("web", "extension"):
        logger.warning(f"[ Warning ] Invalid client-type header: {client_type}")
        return error_response(message = "Invalid client-type", status_code=400)
    engine_type = "light" if client_type == "extension" else "full"

    logger.info(f"[ Client Type ] {client_type.upper()} → Engine Type: {engine_type}")
    session_id = str(uuid.uuid4())
    start_time = time.time()

    # DB 조회
    existing_result = check_url_in_db(url)
    if existing_result:
        logger.info(f"[ Exist in DB! ] {url}")
        if engine_type == "light":
            return success_response({
                "input_url": str(data.url),
                "engine_result_flag": existing_result["engine_result_flag"]
            })
        else:
            return success_response({
                **existing_result
            })

    logger.info(f"[ New URL ] {url}")
    try:
        kernel_service = KernelService()
        result = kernel_service.run_kernel(input_url=url, engine_type=engine_type)
    except Exception as e:
        logger.exception("[ ERROR ] Kernel execution failed.")
        return error_response(message="Kernel execution failed", status_code=500)

    duration = round((time.time() - start_time) * 1000)
    logger.info(f"[ Time ] Detection completed in {duration}ms")

    if engine_type == "light":
        response_payload = {
            "input_url": str(data.url),
            "engine_result_flag": result.get("engine_result_flag")
        }
    else:
        clean_result = {
            "input_url": result.get("input_url"),
            "engine_result_flag": result.get("engine_result_flag"),
            "engine_result_score": result.get("engine_result_score"),
            "module_result_dictionary_list": result.get("module_result_dictionary_list")
        }
        response_payload = clean_result
        insert_url_result(
            input_url = clean_result.get("input_url"),
            engine_result_flag = clean_result.get("engine_result_flag"),
            engine_result_score = clean_result.get("engine_result_score"),
            module_result_dictionary_list = clean_result.get("module_result_dictionary_list")
        )
    
    store_result(session_id, response_payload)
    return success_response(response_payload)


# 결과 조회 엔드포인트
@app.get("/detect/result/{session_id}")
def get_detect_result(session_id: str):
    result = get_result(session_id)
    if result:
        return success_response(result)
    return error_response(message="Session not found", status_code=404)

# 예외 핸들러
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"[ Unhandled Exception ] {exc}")
    return error_response(message="Internal server error", status_code=500)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"[ Validation Error ] {exc}")
    return error_response(message="Invalid request format", status_code=422)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000, reload=True)
