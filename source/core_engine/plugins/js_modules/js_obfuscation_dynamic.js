// [ JS Modules ] js_obfuscation_dynamic.js

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
  const ObfuscationRules = [
    {
      name: "base64_encoding",
      pattern: /atob\(|btoa\(/,
      score: 5,
      message: "Base64 인코딩 감지"
    },
    {
      name: "hex_encoding",
      pattern: /\\x[0-9a-fA-F]{2}/,
      score: 5,
      message: "16진수 인코딩 감지"
    },
    {
      name: "split_join_obfuscation",
      pattern: /(["'][a-zA-Z])(["']\s*\+\s*["'][a-zA-Z])/,
      score: 5,
      message: "문자열 분할 후 합성 감지"
    },
    {
      name: "reverse_join_obfuscation",
      pattern: /split\(\s*["']["']\s*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)/,
      score: 5,
      message: "reverse + join 조합 감지"
    },
    {
      name: "random_var_names",
      pattern: /var\s+_0x[a-f0-9]{4,}/,
      score: 5,
      message: "무작위 변수명 패턴 감지"
    },
    {
      name: "charcode_execution",
      pattern: /String\.fromCharCode\(/,
      score: 5,
      message: "문자코드 기반 실행 가능성 감지"
    },
    {
      name: "function_constructor",
      pattern: /new\s+Function\s*\(/,
      score: 5,
      message: "Function 생성자 사용 감지"
    },
    {
      name: "iife_detected",
      pattern: /\(function\s*\(.*\)\s*{.*}\)\s*\(\)/s,
      score: 5,
      message: "즉시 실행 함수 감지"
    },
    {
      name: "self_invoking_wrapper",
      pattern: /var\s+\w+\s*=\s*function\s*\(.*\)\s*{.*};\s*\w+\(\)/s,
      score: 5,
      message: "자체 호출 래퍼 함수 감지"
    },
    {
      name: "replace_function_obfuscation",
      pattern: /\.replace\(\s*\/.*\/\s*,\s*function\s*\(/,
      score: 5,
      message: "정규표현식 + replace 함수 난독화 감지"
    }
  ];

  // 헤드리스 크롬 실행
  const browser = await puppeteer.launch({
    executablePath: process.env.PUPPETEER_EXEC_PATH || path.resolve(
      process.env.HOME,
      ".cache/puppeteer/chrome/mac-135.0.7049.42/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    ),
    headless: true,
    args: ["--no-sandbox"]
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
      // 동적 탐지할 룰 정의
      const ruleChecks = {
        base64_encoding: code => code.includes("atob("),
        hex_encoding: code => /\\x[0-9a-f]{2}/.test(code),
        charcode_execution: code => code.includes("String.fromCharCode"),
        split_join_obfuscation: code => /["']\s*\+\s*["']/.test(code),
        reverse_join_obfuscation: code => /split\(.*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)/.test(code),
        function_constructor: code => code.includes("alert") || code.includes("eval")
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
      for (const rule of ObfuscationRules) {
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
