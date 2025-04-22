// [ JS Modules ] js_script_dynamic.js

const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const url = process.argv[2];
  const logs = [];
  let score = 0;
  const triggeredRules = new Set();
  const detectedRules = new Set();

  function addLog(message, points) {
    logs.push(`${message} (+${points}점)`);
    score += points;
  }

  // 정규표현식 정의
  const ScriptRules = [
    {
      name: "suspiciousCdn",
      pattern: /https?:\/\/[^\s'""]*(malicious|track|spy|steal|adserver)[^\s'""]*/,
      score: 25,
      message: "의심스럽고 복잡한 CDN URL 검지"
    },
    {
      name: "inlineEventScript",
      pattern: /<script[^>]*>.*(onerror|onload|onclick)=.*<\/script>/,
      score: 15,
      message: "inline event 기능의 스크립트 검지"
    },
    {
      name: "dataJsUrl",
      pattern: /data:text\/javascript/,
      score: 20,
      message: "data URI 구조의 스크립트 삽입 검지"
    },
    {
      name: "documentWrite",
      pattern: /document\.write(ln)?\s*\(/,
      score: 15,
      message: "document.write 사용 감지"
    },
    {
      name: "suspiciousKeyword",
      pattern: /(steal|track|keylog|cookie|grab)[a-z]*\b/,
      score: 15,
      message: "의심 키워드 포함 스크립트 감지"
    },
    {
      name: "base64EncodedString",
      pattern: /atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}/,
      score: 10,
      message: "Base64 디코딩 또는 인코딩 스크립트 감지"
    },
    {
      name: "script_in_img_tag",
      pattern: /<img[^>]+src=['"]javascript:/,
      score: 20,
      message: "<img> 태그에서 javascript: 사용 감지"
    },
    {
      name: "script_src_inline_mix",
      pattern: /<script[^>]+src=.*?>.*?<\/script>/,
      score: 15,
      message: "<script> 태그에서 src와 inline 코드 병용 감지"
    },
    {
      name: "iframe_javascript_src",
      pattern: /<iframe[^>]+src=['"]javascript:/,
      score: 20,
      message: "<iframe>의 src 속성에 javascript URI 사용 감지"
    },
    {
      name: "cookie_access",
      pattern: /document\.cookie/,
      score: 10,
      message: "document.cookie 접근 코드 감지"
    }
  ];

  // 헤드리스 크롬 실행
  const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox']
    });

  const page = await browser.newPage();

  // 리소스 요청 차단, 성능 최적화
  await page.setRequestInterception(true);
  page.on("request", (request) => {
    if (["image", "stylesheet", "font"].includes(request.resourceType())) {
      request.abort();
    } else {
      request.continue();
    }
  });

  try {
    // 실행 감지 위한 후킹 함수 등록
    await page.exposeFunction("trackExecution", (ruleName, message, execScore) => {
      if (detectedRules.has(ruleName) && !triggeredRules.has(ruleName)) {
        addLog(`[실행 탐지] ${message}`, execScore);
        triggeredRules.add(ruleName);
      }
    });

    // 자동 실행 탐지를 위한 후킹 삽입
    await page.evaluateOnNewDocument(() => {
      const ruleChecks = {
        cookie_access: code => code.includes("document.cookie"),
        documentWrite: code => code.includes("document.write"),
        base64EncodedString: code => code.includes("atob(") || code.includes("btoa("),
        suspiciousKeyword: code => /(steal|track|keylog|cookie|grab)/.test(code)
      };

      // 루프 돌며 룰 검사
      const smartHook = (original, gatewayName, execScore) => {
        return function (...args) {
          try {
            const code = args[0];
            if (typeof code === "string") {
              for (const rule in ruleChecks) {
                if (ruleChecks[rule](code)) {
                  window.trackExecution(rule, `${gatewayName}을 통한 ${rule} 실행 감지`, execScore);
                }
              }
            }
          } catch (_) {}
          return original.apply(this, args);
        };
      };

      window.eval = smartHook(window.eval, "eval", 15);
      window.Function = smartHook(window.Function, "Function", 15);
      window.setTimeout = smartHook(window.setTimeout, "setTimeout", 10);
      window.setInterval = smartHook(window.setInterval, "setInterval", 10);
    });

    // 페이지 접속 후 코드 수집
    await page.goto(url, { waitUntil: "networkidle0", timeout: 10000 });

    const scripts = await page.$$eval("script", elements =>
      elements.map(el => el.innerText).filter(Boolean)
    );

    const uniqueScripts = [...new Set(scripts)];

    for (const code of uniqueScripts) {
      // 정규표현식 탐지 수행
      for (const rule of ScriptRules) {
        if (rule.pattern.test(code)) {
          addLog(rule.message, rule.score); // 정적 탐지 점수 가산
          detectedRules.add(rule.name); // 저장
        }
      }
    }

  } catch (err) {
    logs.push(`[오류] 페이지 분석 실패: ${err.message} (+20점)`);
    score += 20;
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({ logs, score }));
})();