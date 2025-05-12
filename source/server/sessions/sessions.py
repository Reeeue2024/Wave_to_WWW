# server/sessions/sessions.py

from typing import Dict, Any
import json

# 세션 저장소 (메모리 기반)
_session_store: Dict[str, Dict[str, Any]] = {}

def store_result(session_id: str, result: Dict[str, Any]) -> None:
    _session_store[session_id] = result

def get_result(session_id: str) -> Dict[str, Any] | None:
    return _session_store.get(session_id)
