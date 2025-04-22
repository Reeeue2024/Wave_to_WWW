// [ JS Modules ] js_dom_dynamic.js

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

  const currentDomain = new URL(url).hostname;

  // 정규표현식 정의
  const DomRules = [
    {
      name: "password_input",
      pattern: /<input[^>]*type=["']password["']/i,
      score: 5,
      message: "비밀번호 입력창 존재 감지"
    },
    {
      name: "hidden_iframe",
      pattern: /<iframe[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
      score: 5,
      message: "숨겨진 iframe 감지"
    },
    {
      name: "external_script",
      pattern: new RegExp(`<script[^>]+src=["']https?:\/\/(?!.*${currentDomain})`, "i"),
      score: 5,
      message: "외부 스크립트 삽입 감지"
    },
    {
      name: "external_form_action",
      pattern: new RegExp(`<form[^>]+action=["']https?:\/\/(?!.*${currentDomain})`, "i"),
      score: 5,
      message: "form 액션이 외부 도메인으로 지정됨"
    },
    {
      name: "insecure_login_form",
      pattern: /<form[^>]+action=["']http:\/\/[^>]*>.*?<input[^>]*type=["']password["']/is,
      score: 5,
      message: "비밀번호 전송에 HTTPS 미사용"
    },
    {
      name: "suspicious_onclick",
      pattern: /onclick\s*=\s*["'].*(location\.href|window\.location|document\.location).*["']/i,
      score: 5,
      message: "onclick 속성 내 의심스러운 리디렉션 감지"
    },
    {
      name: "javascript_uri",
      pattern: /href\s*=\s*["']javascript:/i,
      score: 5,
      message: "href 속성에 javascript URI 사용 감지"
    },
    {
      name: "invisible_link",
      pattern: /<a[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
      score: 5,
      message: "숨겨진 링크 요소 감지"
    },
    {
      name: "iframe_redirect",
      pattern: new RegExp(`<iframe[^>]+src=["']https?:\/\/(?!.*${currentDomain})`, "i"),
      score: 5,
      message: "외부 도메인으로 연결된 iframe 감지"
    },
    {
      name: "meta_refresh_redirect",
      pattern: /<meta[^>]+http-equiv=["']refresh["'][^>]+content=["']\d+;\s*url=/i,
      score: 5,
      message: "meta refresh 태그를 통한 리디렉션 감지"
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
        addLog(`[실행 탐지] ${message}`, execScore);  // 실제 실행되면 가산
        triggeredRules.add(ruleName); // 중복 가산 방지
      }
    });
    
    // 자동 실행 탐지를 위한 후킹 삽입
    await page.evaluateOnNewDocument(() => {
      // DOM 변경 자동 실행 탐지
      const observer = new MutationObserver(mutations => {
        for (const mutation of mutations) {
          if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
            window.trackExecution("dom_mutation", "DOM 변경 감지 (자동 실행)", 25);
          }
        }
      });
      
      // DOM 감시 시작
      window.addEventListener("DOMContentLoaded", () => {
        observer.observe(document.body, { childList: true, subtree: true });
      });

      const smartHook = (original, name) => {
        return function (...args) {
          window.trackExecution("timer_exec", name + " 통해 자동 실행 감지", 25);
          return original.apply(this, args);
        };
      };

      window.setTimeout = smartHook(window.setTimeout, "setTimeout");
      window.setInterval = smartHook(window.setInterval, "setInterval");
    });
    
    // 페이지 접속 후 코드 수집
    await page.goto(url, { waitUntil: "networkidle0", timeout: 3000 });

    const scripts = await page.$$eval("script", elements =>
      elements.map(el => el.innerText).filter(Boolean)
    );

    const uniqueScripts = [...new Set(scripts)];

    for (const code of uniqueScripts) {
      // 정규표현식 탐지 수행
      for (const rule of DomRules) {
        if (rule.pattern.test(code)) {
          addLog(rule.message, rule.score); // 정적 탐지 점수 가산
          detectedRules.add(rule.name); // 저장
        }
      }
    }
    
    // 사용자 클릭 시뮬레이션
    const anchors = await page.$$("a");
    for (const anchor of anchors) {
      try {
        await anchor.click({ delay: 100 });
      } catch (_) {}
    }

    await page.waitForTimeout(2000);

  } catch (err) {
    logs.push(`[오류] 페이지 분석 실패: ${err.message} (+20점)`);
    score += 20;
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({ logs, score }));
})();