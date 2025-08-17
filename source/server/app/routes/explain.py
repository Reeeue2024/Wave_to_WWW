# server/app/routes/explain.py
import os
import re
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

router = APIRouter(tags=["explain"])

# ---------- Schemas (변경 없음) ----------
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

# ---------- Helpers (일부 함수만 변경) ----------
MODULE_ORDER = [
    "Ai", "UrlShort", "UrlSubdomain", "UrlHomograph", "UrlHttp", "UrlIp", "UrlPort",
    "HtmlForm", "HtmlJsUrl", "HtmlResourceUrl", "HtmlIframe", "HtmlAnchor",
    "JsStaticExternal", "JsStaticHook", "JsStaticObfuscate", "JsStaticScript",
    "JsDynamicEval", "JsDynamicFetch",
]
ORDER_INDEX = {name: i for i, name in enumerate(MODULE_ORDER)}
MODULE_NAME_MAP = {
    "Ai": {"en": "AI", "ko": "AI"}, "UrlShort": {"en": "Shortened URL Usage", "ko": "단축 URL 사용 여부"},
    "UrlSubdomain": {"en": "Subdomain Usage", "ko": "서브도메인 사용"}, "UrlHomograph": {"en": "Homograph Usage", "ko": "동형이의어(Homograph) 사용"},
    "UrlHttp": {"en": "HTTP Protocol Usage", "ko": "HTTP 프로토콜 사용"}, "UrlIp": {"en": "IP Address Usage", "ko": "IP 주소 사용"},
    "UrlPort": {"en": "Port Number Usage", "ko": "포트 번호 사용"}, "UrlSsl": {"en": "SSL Certificate Usage", "ko": "SSL 인증서 사용 여부"},
    "UrlWhois": {"en": "WHOIS Data Usage", "ko": "WHOIS 정보 분석"}, "HtmlForm": {"en": "Form Tag Usage", "ko": "Form 태그 사용"},
    "HtmlIframe": {"en": "IFrame Tag Usage", "ko": "IFrame 태그 사용"}, "HtmlJsUrl": {"en": "JavaScript URL Usage", "ko": "자바스크립트 URL 사용"},
    "HtmlLink": {"en": "Link Tag Usage", "ko": "Link 태그 사용"}, "HtmlMetaRefresh": {"en": "Meta Refresh Tag Usage", "ko": "Meta Refresh 태그 사용"},
    "HtmlResourceUrl": {"en": "Resource URL Usage", "ko": "리소스 URL 사용"}, "HtmlStyle": {"en": "Style Tag Usage", "ko": "Style 태그 사용"},
    "HtmlAnchor": {"en": "Anchor Tag Usage", "ko": "Anchor 태그 사용"}, "JsStaticExternal": {"en": "External Script Usage", "ko": "외부 스크립트 사용"},
    "JsStaticHook": {"en": "Event Hook Usage", "ko": "이벤트 후킹 사용"}, "JsStaticObfuscate": {"en": "Code Obfuscation Usage", "ko": "코드 난독화 사용"},
    "JsStaticRedirect": {"en": "Static Redirect Usage", "ko": "정적 리디렉션 사용"}, "JsStaticScript": {"en": "Script Tag Usage", "ko": "Script 태그 사용"},
    "JsDynamicDom": {"en": "DOM Manipulation Usage", "ko": "DOM 조작 사용"}, "JsDynamicExternal": {"en": "Script Injection Usage", "ko": "스크립트 동적 삽입"},
    "JsDynamicHook": {"en": "Event Hook Usage", "ko": "동적 이벤트 후킹"}, "JsDynamicObfuscate": {"en": "Code Obfuscation Usage", "ko": "실행 중 코드 난독화"},
    "JsDynamicRedirect": {"en": "Redirect Usage", "ko": "실행 중 리디렉션"}, "JsDynamicEval": {"en": "Dynamic Eval Usage", "ko": "동적 Eval 사용"},
    "JsDynamicFetch": {"en": "Dynamic Fetch Usage", "ko": "동적 Fetch 사용"},
}

def _cut(v: Any, n: int = 1200) -> str:
    if v is None: return ""
    return str(v)[:n]

def _risk_policy(score: float) -> Dict[str, str]:
    if score < 50: return {"band": "low", "verdict_ko": "대체로 안전", "verdict_en": "Generally safe", "tone_ko": "차분하고 안심시키는 어조로, 소폭의 주의사항만 제시", "tone_en": "Reassuring and calm; provide light, practical cautions only", "ban_words_ko": "아래 표현 금지: 매우 위험, 치명적, 즉시, 심각, 고위험", "ban_words_en": "Avoid: highly dangerous, critical, urgent, severe, high risk", "actions_ko": "일상 점검 수준(도메인 확인, 과도한 개인정보 입력 자제 등)", "actions_en": "Routine checks (verify domain, avoid unnecessary sensitive input)",}
    if score < 70: return {"band": "medium", "verdict_ko": "주로 안전하지만 주의 필요", "verdict_en": "Mostly safe with caution", "tone_ko": "균형 잡힌 어조로 장점과 주의점 모두 제시. 과장된 경고 금지", "tone_en": "Balanced tone: note positives and caveats. No alarmist language", "ban_words_ko": "아래 표현 금지: 매우 위험, 치명적, 즉시, 심각, 고위험", "ban_words_en": "Avoid alarmist terms like highly dangerous, critical, urgent", "actions_ko": "점검 권고(주소창 철저 재확인, 민감정보 입력 전 재검토 등)", "actions_en": "Recommend simple checks (re-check address bar, review before input)",}
    return {"band": "high", "verdict_ko": "위험 높음", "verdict_en": "High risk", "tone_ko": "명확하고 단호한 경고. 이용 중단과 대안 제시", "tone_en": "Clear, firm warning. Advise avoidance and safer alternatives", "ban_words_ko": "", "ban_words_en": "", "actions_ko": "이용 중단, 공식 경로 재접속, 비밀번호 변경 등", "actions_en": "Avoid, use official channels, rotate passwords, etc.",}

def _interpretation_ko(band: str) -> str:
    if band == "low": return "일반적인 이용은 무리가 없으며, 기본적인 점검만 병행하시면 됩니다."
    if band == "medium": return "대체로 이용 가능하나, 아래 주의사항을 확인하고 민감 정보 입력은 신중히 하세요."
    return "이용을 피하고 공식 경로로만 접속하는 것을 권장합니다."

def _interpretation_en(band: str) -> str:
    if band == "low": return "Fine for typical use; just follow basic checks."
    if band == "medium": return "Generally OK to use, but review the brief red flags below and be cautious with sensitive data."
    return "Avoid using the site and switch to official channels."

def _extract_ai_score(modules: List[ModuleItem]) -> Optional[float]:
    for m in modules:
        if (m.moduleName or "").strip().lower() == "ai":
            r = m.reason
            if isinstance(r, list): txt = " ".join(str(x) for x in r[:20])
            elif isinstance(r, dict): txt = " ".join(f"{k}: {v}" for k, v in list(r.items())[:20])
            else: txt = str(r or "")
            mobj = re.search(r"[\d.]+", txt)
            if mobj:
                try:
                    val = float(mobj.group())
                    if 0 <= val <= 100: return val
                except ValueError: pass
    return None

def _friendly_reason(module: str, reason: Any, lang: str) -> str:
    if reason is None: return "탐지됨" if lang == "ko" else "Detected"
    if isinstance(reason, list): return " | ".join(str(item) for item in reason if str(item).strip())
    if isinstance(reason, dict): return " | ".join(f"{k}: {v}" for k, v in reason.items())
    return str(reason)

# --- CHANGED START ---
def _prompt_ko(payload: Dict, pol: Dict) -> str:
    score_overall = int(round(payload["overall"]["resultScore"]))
    total = payload["counts"]["total"]
    flagged = payload["counts"]["flagged"]
    ai_score = payload.get("aiScore", None)
    ai_str = f"{int(round(ai_score))}%" if isinstance(ai_score, (int, float)) else "N/A"
    reported_to_kisa = payload.get("reportedToKisa", False)
    
    interpretation_base = _interpretation_ko(pol['band'])
    kisa_notice_block = "wave to www에서 해당 사이트를 피싱 사이트로 의심하여 KISA(한국인터넷진흥원)에 자동 제보하였습니다." if reported_to_kisa else ""

    return f"""
당신은 보안 전문가로서 일반 사용자에게 웹사이트 보안 분석 결과를 설명하는 역할입니다.
마크다운 없이 일반 텍스트로만 작성하세요.
어조: {pol['tone_ko']} ({pol['ban_words_ko']})

아래 데이터는 실제로 웹사이트에서 탐지된 보안 위험 요소들입니다.
각 모듈의 "reason" 필드에는 구체적으로 무엇이 발견되었는지가 기술적 용어로 기록되어 있습니다.
이를 분석해서 일반 사용자가 이해할 수 있도록 설명해주세요.

**중요 지시사항:**
1. 기술적 용어를 일반인 용어로 번역하세요.
2. 각 탐지 항목이 왜 위험한지 사용자 관점에서 설명하세요.
3. 탐지된 구체적인 내용을 근거로 설명하세요 (추측하지 말고).
4. findings 배열의 각 항목에서 "name" 필드에 이미 사용자 친화적 이름이 제공되어 있으니 그것을 그대로 사용하세요.
5. KISA 제보 문구는 제공된 경우 반드시 그대로, 별도의 줄에 출력하세요.

다음 구조로 정확히 출력하세요:

전체 판단: {pol['verdict_ko']} ({score_overall}%)
탐지 현황: {flagged}/{total}개 항목에서 위험 신호 발견. AI 위험도: {ai_str}
해석: {interpretation_base}

{kisa_notice_block}

발견된 위험 요소:
(각 탐지된 모듈을 1., 2., 3... 형식으로 나열하되, reason 필드의 내용을 분석해서 구체적으로 무엇이 발견되었는지와 왜 위험한지 설명)

[실제 탐지 데이터]
{payload}
""".strip()

def _prompt_en(payload: Dict, pol: Dict) -> str:
    score_overall = int(round(payload["overall"]["resultScore"]))
    total = payload["counts"]["total"]
    flagged = payload["counts"]["flagged"]
    ai_score = payload.get("aiScore", None)
    ai_str = f"{int(round(ai_score))}%" if isinstance(ai_score, (int, float)) else "N/A"
    reported_to_kisa = payload.get("reportedToKisa", False)
    
    interpretation_base = _interpretation_en(pol['band'])
    kisa_notice_block = "wave to www has automatically reported this site to KISA (Korea Internet & Security Agency) as a suspected phishing site." if reported_to_kisa else ""

    return f"""
You are a security expert explaining website security analysis results to regular users.
Return PLAIN TEXT only (no Markdown).
Tone: {pol['tone_en']} ({pol['ban_words_en']})

The data below contains actual security risk factors detected on the website.
Analyze this data and explain it in terms regular users can understand.

**Important Instructions:**
1. Translate technical terms to plain language.
2. Explain why each detected item is risky from a user perspective.
3. Base explanations on the specific detected content (don't speculate).
4. Use the user-friendly names from the "name" field in findings array.
5. If the KISA notice is provided, you MUST output it verbatim on its own separate line.

Output in EXACTLY this structure:

Overall, the site is {pol['verdict_en'].lower()} ({score_overall}%).
Detection status: Found risk signals in {flagged} of {total} items. AI risk score: {ai_str}.
Interpretation: {interpretation_base}

{kisa_notice_block}

Risk factors found:
(List each detected module as 1., 2., 3... format, analyzing the reason field content to explain specifically what was found and why it's risky)

[Actual Detection Data]
{payload}
""".strip()
# --- CHANGED END ---

# ---------- Route ----------
@router.post("/explain")
def explain(req: ExplainRequest):
    # 1) AI 점수
    ai_score = _extract_ai_score(req.modules)

    # 2) 모듈 요약 + 원본 순서 인덱스
    mods = []
    for idx, m in enumerate(req.modules):
        r = m.reason
        if isinstance(r, list): r_str = "; ".join(str(x) for x in r)
        elif isinstance(r, dict): r_str = "; ".join(f"{k}: {v}" for k, v in list(r.items())[:20])
        else: r_str = str(r or "")
        mods.append({
            "name": _cut(m.moduleName, 128), "name_raw": m.moduleName,
            "detected": bool(m.moduleResultFlag), "reason_raw": r,
            "reason": _cut(r_str, 600), "orig_index": idx
        })

    total = len(mods)
    detected_list = [x for x in mods if x["detected"]]

    # 3) 출력 순서 정렬
    def sort_key(x: Dict) -> tuple:
        order = ORDER_INDEX.get(x["name_raw"], 10_000)
        return (order, x["orig_index"])
    detected_list.sort(key=sort_key)

    # 4) 사용자 친화 문구로 교체
    for x in detected_list:
        lang = req.lang
        x["friendly"] = _friendly_reason(x["name_raw"], x["reason_raw"], lang)
        x["display_name"] = MODULE_NAME_MAP.get(x["name_raw"], {}).get(lang, x["name_raw"])

    flagged = len(detected_list)

    # 5) 페이로드 생성
    payload = {
        "url": _cut(req.summary.inputUrl, 1024),
        "overall": {"resultFlag": bool(req.summary.resultFlag), "resultScore": req.summary.resultScore},
        "counts": {"total": total, "flagged": flagged},
        "findings": [{"name": x["display_name"], "reason": x["friendly"]} for x in detected_list],
        "aiScore": ai_score,
        "reportedToKisa": req.summary.reportedToKisa if req.summary.resultScore >= 70 else False,
    }

    pol = _risk_policy(req.summary.resultScore)

    # 6) OpenAI 미사용 시 폴백 출력
    if client is None:
        score_overall = int(round(req.summary.resultScore))
        ai_str = f"{int(round(ai_score))}%" if isinstance(ai_score, (int, float)) else "N/A"
        reported_to_kisa = req.summary.reportedToKisa if req.summary.resultScore >= 70 else False
        
        if req.lang == "ko":
            interpretation_base = _interpretation_ko(pol['band'])
            kisa_notice = "wave to www에서 해당 사이트를 피싱 사이트로 의심하여 KISA(한국인터넷진흥원)에 자동 제보하였습니다." if reported_to_kisa else ""
            header = (
                f"전체 판단: {pol['verdict_ko']} ({score_overall}%)\n"
                f"탐지 현황: {flagged}/{total} 모듈이 경고로 표시됨. AI score: {ai_str}\n"
                f"해석: {interpretation_base}\n"
                f"\n{kisa_notice}\n" if kisa_notice else "\n" # KISA 문구가 있을 때만 줄바꿈 추가
                "위험 신호:\n"
            )
        else:
            interpretation_base = _interpretation_en(pol['band'])
            kisa_notice = "wave to www has automatically reported this site to KISA (Korea Internet & Security Agency) as a suspected phishing site." if reported_to_kisa else ""
            header = (
                f"Overall, the site is {pol['verdict_en'].lower()} ({score_overall}%).\n"
                f"Modules flagged: {flagged} of {total}. AI score: {ai_str}.\n"
                f"Interpretation: {interpretation_base}\n"
                f"\n{kisa_notice}\n" if kisa_notice else "\n" # Add newlines only if KISA notice exists
                "Red flags:\n"
            )
            
        lines = [f"{i}. {x['display_name']}: {x['friendly']}" for i, x in enumerate(detected_list, 1)]
        body = "\n".join(lines) if lines else ("(해당 없음)" if req.lang == "ko" else "(none)")
        return {"ok": True, "data": {"explanation": header + body, "lang": req.lang}}

    # 7) OpenAI 사용 경로
    sys = (
        "You are a security explainer for end-users. "
        f"Output ONLY in {'Korean' if req.lang=='ko' else 'English'}. "
        "Respond in plain TEXT (no Markdown symbols or tables). "
        "List EVERY detected module in the red-flags section, one line each. "
        "Adhere strictly to the output format provided by the user."
    )
    user_prompt = (_prompt_ko if req.lang == "ko" else _prompt_en)(payload, pol)

    try:
        cmpl = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2, # 온도를 약간 낮춰서 형식을 더 잘 따르도록 유도
            max_tokens=1400,
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = (cmpl.choices[0].message.content or "").strip()
        return {"ok": True, "data": {"explanation": text, "lang": req.lang}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explain API error: {e}")