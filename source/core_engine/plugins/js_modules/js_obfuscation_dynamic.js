// [ JS Modules ] js_obfuscation_dynamic.js

const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const url = process.argv[2];
  const logs = [];
  let score = 0;

  // 탐지 규칙 정의
  const rules = [
    {
      pattern: /eval\s*\(/,
      score: 25,
      message: "eval() 사용 감지 (+25점)"
    },
    {
      pattern: /Function\s*\(/,
      score: 15,
      message: "Function() 사용 감지 (+15점)"
    },
    {
      pattern: /setTimeout\s*\(\s*['"]/,
      score: 10,
      message: "setTimeout 문자열 실행 감지 (+10점)"
    },
    {
      pattern: /String\.fromCharCode\s*\(/,
      score: 10,
      message: "String.fromCharCode() 사용 감지 (+10점)"

    },
    {
      pattern: /\\x[0-9a-fA-F]{2}/,
      score: 20,
      message: "16진수 이스케이프 문자열 감지 (+20점)"
    },
    {
      pattern: /var\s+_0x[a-fA-F0-9]+/,
      score: 20,
      message: "난독화된 변수명 패턴 감지 (+20점)"
    }
  ];
  
  // 중복 탐지 방지 위한 메세지 추적용 Set
  const detected = new Set();

  try {
    const browser = await puppeteer.launch({
      executablePath: path.resolve(
        process.env.HOME,
        ".cache/puppeteer/chrome/mac-135.0.7049.42/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
      ),
      headless: true,
      args: ["--no-sandbox"]
    });
    
    // 렌더링 <script> 요소의 JavaScript 코드만 수집
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: "networkidle2", timeout: 5000 });

    const scripts = await page.$$eval("script", elements =>
      elements.map(el => el.innerText).filter(Boolean)
    );
    
    // 탐지 규칙 매칭, 점수 및 로그 누적
    for (const code of scripts) {
      for (const rule of rules) {
        if (!detected.has(rule.message) && rule.pattern.test(code)) {
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
