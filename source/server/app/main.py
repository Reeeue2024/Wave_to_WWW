# [ Server ] main.py (no db ver.)

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from server.sessions.sessions import store_result, get_result
from server.app.utils.response import success_response, error_response
from server.app.utils.logger import logger
from server.app.schemas.request_schema import UrlDetectRequest
from configs.config import ALLOWED_ORIGINS
from core_engine.kernel_service import KernelService
from server.app.db_connector import check_url_in_db, insert_url_result
import uuid
import time
import json

app = FastAPI()

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
async def detect_url(request: UrlDetectRequest):
    url = request.url
    engine_type = "full"  # 기본값 고정
    session_id = str(uuid.uuid4())
    start_time = time.time()

    existing_result = check_url_in_db(url)

    if existing_result:
        logger.info(f"이미 검사된 URL: {url}")
        response_payload = {
            "session_id": session_id,
            "url": str(url),
            "is_phishing": existing_result["is_phishing"],
            "total score": existing_result["total_score"],
            "scores": existing_result["scores"],
            "results": existing_result["results"]
        }
        return success_response(response_payload)
    
    else:
        logger.info(f"새로 검사되는 URL: {url}")
        try:
            kernel_service = KernelService()
            result = kernel_service.run_kernel(input_url=url, engine_type=engine_type)
        except Exception as e:
            logger.exception("[ ERROR ] Kernel execution failed.")
            return error_response(message="Kernel execution failed", status_code=500)

        insert_url_result(
            url, 
            result.get("engine_result_flag"), 
            result.get("engine_result_score"),
            {
                r["module_class_name"]: r["module_score"]
                for r in result.get("module_result_dictionary_list", [])
            },
            result.get("module_result_dictionary_list", [])
        )
        
        duration = round((time.time() - start_time) * 1000)
        logger.info(f"[ Time ] Detection completed in {duration}ms")

        response_payload = {
            "session_id": session_id,
            "url": str(url),
            "is_phishing": result.get("engine_result_flag"),
            "total score": result.get("engine_result_score"),
            "scores": {
                r["module_class_name"]: r["module_score"]
                for r in result.get("module_result_dictionary_list", [])
            },
            "results": [
                {
                    "module_class_name": r["module_class_name"],
                    "module_result_flag": r["module_result_flag"],  # 모듈 실행 결과
                    "module_result_data": r["module_result_data"],  # 모듈 결과 데이터
                }
                for r in result.get("module_result_dictionary_list", [])
            ]
        }

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
