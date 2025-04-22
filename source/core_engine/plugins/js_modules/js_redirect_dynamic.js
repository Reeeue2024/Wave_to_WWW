// [ JS Modules ] JS Redirect Dynamic JS

const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];  // 입력받은 URL
  const logs = [];
  let score = 0;
  let redirected = false;

  const initialUrl = url;

  // 브라우저 실행
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox']
  });

  const page = await browser.newPage();

  // HTTP 리디렉션 감지
  page.on('response', response => {
    const status = response.status();
    if (status >= 300 && status < 400) {
      console.log(`[Info] Redirect Response Code: ${status}`);  // 영어로 출력
      logs.push(`[Info] Redirect Response Code: ${status}`);  // 로그에 기록만 함
      redirected = true;
    }
  });

  // JS 기반 리디렉션 감지
  await page.evaluateOnNewDocument(() => {
    const originalAssign = window.location.assign;
    window.location.assign = function (newLocation) {
      console.log('Redirect detected:', newLocation);  // 리디렉션이 감지되면 로그 출력
      return originalAssign.call(this, newLocation);
    };
  });

  // 시간 측정 시작
  const startTime = Date.now();

  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

  // 최대 5초 대기
  const timeoutPromise = new Promise(resolve => setTimeout(resolve, 5000));
  await Promise.race([
    page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {}),
    timeoutPromise
  ]);

  const finalUrl = page.url();
  const endTime = Date.now();
  const duration = (endTime - startTime) / 1000;

  // 리디렉션 여부 판단 및 점수 계산
  if (initialUrl !== finalUrl || redirected) {
    logs.push("Redirect detected");

    if (duration <= 3) {
      score = 0.6;
      logs.push(`fast (+${score})`);
    } else if (duration <= 5) {
      score = 0.4;
      logs.push(`moderate (+${score})`);
    } else {
      score = 0.2;
      logs.push(`slow (+${score})`);
    }

  } else {
    logs.push("No redirect detected (0.0)");
    score = 0.0;
  }

  await browser.close();

  // 최종 URL 출력
  console.log("Final URL:", finalUrl);

  // 결과 출력 (Python에서 JSON으로 파싱)
  console.log(JSON.stringify({ logs, score }));
})();
