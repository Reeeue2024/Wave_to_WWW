// [ JS Modules ] js_script_dynamic.js

const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const url = process.argv[2];
  const logs = [];
  let score = 0;

  // 탐지 규칙 정의
  const rules = [
    {
      pattern: /https?:\/\/[^\s'"]*(malicious|track|spy|steal|adserver)[^\s'"]*/i,
      score: 25,
      message: "의심스러운 외부 CDN URL 감지 (+25점)"
    },
    {
      pattern: /data:text\/javascript/i,
      score: 20,
      message: "data URI 형식의 스크립트 감지 (+20점)"
    },
    {
      pattern: /<script[^>]*(onerror|onload|onclick)=/i,
      score: 15,
      message: "inline 이벤트 핸들러 포함 스크립트 감지 (+15점)"
    },
    {
        pattern: /document\.write(ln)?\s*\(/i,
        score: 15,
        message: "document.write(ln) 사용 감지 (+15점)"
      },
      {
        pattern: /(steal|track|keylog|cookie|grab)[a-z]*\b/i,
        score: 15,
        message: "의심 키워드 포함 감지 (+15점)"
      },
      {
        pattern: /atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}/,
        score: 10,
        message: "Base64 디코딩 또는 긴 인코딩 문자열 감지 (+10점)"
      }
  ];

  // 중복 탐지 방지 위한 메세지 추적용 Set
  const detected = new Set();

  try {
    const browser = await puppeteer.launch({
      executablePath: process.env.PUPPETEER_EXEC_PATH || path.resolve(
        process.env.HOME,
        ".cache/puppeteer/chrome/mac-135.0.7049.42/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
      ),
      headless: true,
      args: ["--no-sandbox"]
    });

    // 렌더링 <script> 태그의 전체 outerHTML 및 src 속성 수집
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: "networkidle2", timeout: 5000 });

    const scripts = await page.$$eval("script", elements =>
      elements.map(el => (el.outerHTML || "") + "\n" + (el.src || ""))
    );
    
    // 탐지 규칙 매칭, 점수 및 로그 누적
    for (const content of scripts) {
      for (const rule of rules) {
        if (!detected.has(rule.message) && rule.pattern.test(content)) {
          logs.push(rule.message);
          score += rule.score;
          detected.add(rule.message);
        }
      }
    }

    await browser.close();
  } catch (err) {
    logs.push(`[오류] 페이지 열기 실패: ${err.message} (+20점)`);
    score += 20;
  }

  // 최종 결과 JSON 출력
  console.log(JSON.stringify({ logs, score }));
})();
