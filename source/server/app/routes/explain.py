# server/app/routes/explain.py
import os
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

# 환경변수는 main.py에서 이미 load_dotenv로 로드됨
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

router = APIRouter(tags=["explain"])

# ---------- Schemas ----------
class ModuleItem(BaseModel):
    moduleName: str
    moduleResultFlag: bool = False
    moduleScore: Optional[float] = None
    moduleWeight: Optional[float] = None
    reason: Optional[Any] = None
    moduleRun: Optional[bool] = None

class Summary(BaseModel):
    inputUrl: Optional[str] = None
    resultFlag: bool = False
    resultScore: float = 0.0
    reportedToKisa: Optional[bool] = None

class ExplainRequest(BaseModel):
    lang: str = Field(default="ko", description="ko 또는 en")
    summary: Summary
    modules: List[ModuleItem] = []

# ---------- Helpers ----------
def _cut(v: Any, n: int = 1200) -> str:
    if v is None:
        return ""
    return str(v)[:n]

def _prompt_ko(payload: Dict) -> str:
    return f"""
보안 비전문가에게도 이해되도록 아주 쉽게 설명하세요.

[형식]
- 한 문장 요약
- 위험 신호(3~5개): 쉬운 표현 + 왜 위험한지
- 지금 당장 할 일(2~3개 체크리스트)
- 추가 팁(선택)

[데이터]
{payload}
"""

def _prompt_en(payload: Dict) -> str:
    return f"""
Explain in plain language for non-technical users.

[Format]
- One-sentence summary
- Red flags (3–5): simple phrasing + why it matters
- Do-now checklist (2–3)
- Extra tips (optional)

[Data]
{payload}
"""

# ---------- Route ----------
@router.post("/explain")
def explain(req: ExplainRequest):
    # 키 없으면 개발용 fallback (동작 확인용)
    if client is None:
        total = len(req.modules)
        detected = sum(1 for m in req.modules if m.moduleResultFlag)
        score = req.summary.resultScore
        if req.lang == "ko":
            text = (
                f"한 줄 요약: 총 {total}개 중 {detected}개에서 위험 신호가 발견되었습니다. "
                f"AI 점수는 {score}%입니다.\n\n"
                "지금 할 일: (1) 비밀번호/결제정보 입력 금지 (2) 주소창 도메인 철자 재확인 "
                "(3) 공식 사이트를 검색/북마크로 직접 접속하세요."
            )
        else:
            text = (
                f"Summary: {detected} of {total} checks flagged risk indicators. "
                f"AI score: {score}%.\n\n"
                "Do now: (1) Do not enter credentials/payment (2) Re-check the domain "
                "(3) Visit the official site via search/bookmark."
            )
        return {"ok": True, "data": {"explanation": text, "lang": req.lang}}

    # LLM에 넣을 축약 payload 만들기
    mods = []
    for m in req.modules:
        reason = m.reason
        if isinstance(reason, list):
            reason = "; ".join(str(x) for x in reason)
        elif isinstance(reason, dict):
            reason = "; ".join(f"{k}: {v}" for k, v in list(reason.items())[:10])
        mods.append({
            "name": _cut(m.moduleName, 128),
            "detected": bool(m.moduleResultFlag),
            "reason": _cut(reason, 600)
        })

    payload = {
        "url": _cut(req.summary.inputUrl, 1024),
        "overall": {
            "resultFlag": bool(req.summary.resultFlag),
            "resultScore": req.summary.resultScore
        },
        "topFindings": [x for x in mods if x["detected"]][:8],
        "checkedNoIssues": [x["name"] for x in mods if not x["detected"]][:8],
    }

    sys = (
        "You are a security explainer for end-users. "
        f"Output ONLY in {'Korean' if req.lang=='ko' else 'English'}. "
        "Be concise, clear, and practical."
    )
    user_prompt = (_prompt_ko if req.lang == "ko" else _prompt_en)(payload)

    try:
        cmpl = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=700,
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = (cmpl.choices[0].message.content or "").strip()
        return {"ok": True, "data": {"explanation": text, "lang": req.lang}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explain API error: {e}")
