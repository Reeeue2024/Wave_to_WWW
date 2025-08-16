# server/app/routes/explain.py
import os
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
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

def _risk_policy(score: float) -> Dict[str, str]:
    """점수에 따라 톤/판정 문구/금지어 규칙을 반환"""
    if score < 50:
        return {
            "band": "low",
            "verdict_ko": "대체로 안전",
            "verdict_en": "Generally safe",
            "tone_ko": "차분하고 안심시키는 어조로, 소폭의 주의사항만 제시",
            "tone_en": "Reassuring and calm; provide light, practical cautions only",
            "ban_words_ko": "아래 표현 금지: 매우 위험, 치명적, 즉시, 심각, 고위험",
            "ban_words_en": "Avoid: highly dangerous, critical, urgent, severe, high risk",
            "actions_ko": "일상 점검 수준(도메인 확인, 과도한 개인정보 입력 자제 등)",
            "actions_en": "Routine checks (verify domain, avoid unnecessary sensitive input)",
        }
    if score < 70:
        return {
            "band": "medium",
            "verdict_ko": "주로 안전하지만 주의 필요",
            "verdict_en": "Mostly safe with caution",
            "tone_ko": "균형 잡힌 어조로 장점과 주의점 모두 제시. 과장된 경고 금지",
            "tone_en": "Balanced tone: note positives and caveats. No alarmist language",
            "ban_words_ko": "아래 표현 금지: 매우 위험, 치명적, 즉시, 심각, 고위험",
            "ban_words_en": "Avoid alarmist terms like highly dangerous, critical, urgent",
            "actions_ko": "점검 권고(주소창 철자 재확인, 민감정보 입력 전 재검토 등)",
            "actions_en": "Recommend simple checks (re-check address bar, review before input)",
        }
    return {
        "band": "high",
        "verdict_ko": "위험 높음",
        "verdict_en": "High risk",
        "tone_ko": "명확하고 단호한 경고. 이용 중단과 대안 제시",
        "tone_en": "Clear, firm warning. Advise avoidance and safer alternatives",
        "ban_words_ko": "",
        "ban_words_en": "",
        "actions_ko": "이용 중단, 공식 경로 재접속, 비밀번호 변경 등",
        "actions_en": "Avoid, use official channels, rotate passwords, etc.",
    }

def _interpretation_ko(band: str) -> str:
    if band == "low":
        return "일반적인 이용은 무리가 없으며, 기본적인 점검만 병행하시면 됩니다."
    if band == "medium":
        return "대체로 이용 가능하나, 아래 주의사항을 확인하고 민감 정보 입력은 신중히 하세요."
    return "이용을 피하고 공식 경로로만 접속하는 것을 권장합니다."

def _interpretation_en(band: str) -> str:
    if band == "low":
        return "Fine for typical use; just follow basic checks."
    if band == "medium":
        return "Generally OK to use, but review the brief red flags below and be cautious with sensitive data."
    return "Avoid using the site and switch to official channels."

def _prompt_ko(payload: Dict, pol: Dict) -> str:
    score = int(round(payload["overall"]["resultScore"]))
    total = payload["counts"]["total"]
    flagged = payload["counts"]["flagged"]
    return f"""
일반 사용자가 이해하기 쉽게, 마크다운 없이 '텍스트만'으로 작성하세요.
어조: {pol['tone_ko']} ({pol['ban_words_ko']})

다음 '정확한 구조'로 출력하세요:

전체 판단: {pol['verdict_ko']} ({score}%)
탐지 현황: {flagged}/{total} 모듈이 경고로 표시됨. AI 점수: {score}%
해석: {_interpretation_ko(pol['band'])}

위험 신호:
- 번호(1., 2., 3.)로 최대 5개를 나열
- 각 항목은 "모듈명: 왜 주의해야 하는지" 한 줄 요약
- 데이터에 없는 사실을 만들지 말 것

[데이터]
{payload}
""".strip()

def _prompt_en(payload: Dict, pol: Dict) -> str:
    score = int(round(payload["overall"]["resultScore"]))
    total = payload["counts"]["total"]
    flagged = payload["counts"]["flagged"]
    return f"""
Return PLAIN TEXT only (no Markdown). Tone must follow the policy (no alarmist terms for lower bands).

Output in EXACTLY this structure:

Overall, the site is {pol['verdict_en'].lower()} ({score}%).
Modules flagged: {flagged} of {total}. AI score: {score}%.
Interpretation: {_interpretation_en(pol['band'])}

Red flags:
- Use a numbered list (1., 2., 3.) with up to 5 items
- Each item: "<module>: why it matters" in simple words
- Do not invent findings; use only data provided

[DATA]
{payload}
""".strip()

# ---------- Route ----------
@router.post("/explain")
def explain(req: ExplainRequest):
    # 모듈 요약
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

    total = len(mods)
    top = [x for x in mods if x["detected"]]
    flagged = len(top)

    payload = {
        "url": _cut(req.summary.inputUrl, 1024),
        "overall": {
            "resultFlag": bool(req.summary.resultFlag),
            "resultScore": req.summary.resultScore
        },
        "counts": {"total": total, "flagged": flagged},
        "topFindings": top[:8],
    }

    pol = _risk_policy(req.summary.resultScore)

    # API 키 없을 때 폴백 (구조 동일)
    if client is None:
        score = int(round(req.summary.resultScore))
        if req.lang == "ko":
            header = (
                f"전체 판단: {pol['verdict_ko']} ({score}%)\n"
                f"탐지 현황: {flagged}/{total} 모듈이 경고로 표시됨. AI 점수: {score}%\n"
                f"해석: {_interpretation_ko(pol['band'])}\n\n"
                "위험 신호:\n"
            )
        else:
            header = (
                f"Overall, the site is {pol['verdict_en'].lower()} ({score}%).\n"
                f"Modules flagged: {flagged} of {total}. AI score: {score}%.\n"
                f"Interpretation: {_interpretation_en(pol['band'])}\n\n"
                "Red flags:\n"
            )
        redflags = []
        for i, x in enumerate(top[:5], 1):
            piece = x["reason"] if x["reason"] else "Potentially risky behavior"
            redflags.append(f"{i}. {x['name']}: {piece}")
        body = "\n".join(redflags) if redflags else ("(none)" if req.lang != "ko" else "(해당 없음)")
        return {"ok": True, "data": {"explanation": header + body, "lang": req.lang}}

    sys = (
        "You are a security explainer for end-users. "
        f"Output ONLY in {'Korean' if req.lang=='ko' else 'English'}. "
        "Respond in plain TEXT (no Markdown symbols or tables). "
        "Your tone MUST follow the risk policy and never exaggerate lower-risk cases."
    )
    user_prompt = (_prompt_ko if req.lang == "ko" else _prompt_en)(payload, pol)

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
