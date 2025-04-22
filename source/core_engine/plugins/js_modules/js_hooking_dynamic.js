// [ JS Modules ] Hooking Dynamic JS

const puppeteer = require('puppeteer');  // puppeteer 사용
const path = require('path');

(async () => {
  const url = process.argv[2];  // URL을 파라미터로 받음
  const logs = [];
  let score = 0;

    // 후킹 탐지 규칙 정의
    const rules = [
        { pattern: /addEventListener\s*\(/i, score: 0.05, message: "addEventListener (+0.05)" },
        { pattern: /XMLHttpRequest\s*\(/i, score: 0.06, message: "XMLHttpRequest (+0.06)" },
        { pattern: /fetch\s*\(/i, score: 0.06, message: "fetch (+0.06)" },
        { pattern: /eval\s*\(/i, score: 0.08, message: "eval (+0.08)" },
        { pattern: /document\.write\s*\(/i, score: 0.04, message: "document.write (+0.04)" },
        { pattern: /(steal|track|keylog|cookie|grab)[a-z]*\b/i, score: 0.04, message: "suspicious (+0.04)" },
        { pattern: /setTimeout\s*\(/i, score: 0.06, message: "setTimeout (+0.06)" },
        { pattern: /setInterval\s*\(/i, score: 0.06, message: "setInterval (+0.06)" },
        { pattern: /localStorage\s*\./i, score: 0.06, message: "localStorage (+0.06)" },
        { pattern: /sessionStorage\s*\./i, score: 0.06, message: "sessionStorage (+0.06)" },
        { pattern: /WebSocket\s*\(/i, score: 0.08, message: "WebSocket (+0.08)" },
        { pattern: /document\.cookie\s*/i, score: 0.08, message: "document.cookie (+0.08)" },
        { pattern: /window\s*\./i, score: 0.06, message: "window (+0.06)" },
        { pattern: /atob\s*\(/i, score: 0.08, message: "atob (+0.08)" },
        { pattern: /btoa\s*\(/i, score: 0.08, message: "btoa (+0.08)" }
    ];
    

  // 중복 탐지 방지 위한 메시지 추적용 Set
  const detected = new Set();

  try {
    // Puppeteer로 브라우저 실행 (Chrome/Chromium 자동 다운로드)
    const browser = await puppeteer.launch({
      headless: true, // headless 모드로 브라우저 실행
      args: ['--no-sandbox']
    });

    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 5000 });

    // 페이지 내 모든 script 태그를 확인하여 후킹 코드 패턴을 찾음
    const scripts = await page.$$eval('script', elements =>
      elements.map(el => (el.outerHTML || '') + '\n' + (el.src || ''))
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
