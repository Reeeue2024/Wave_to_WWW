// [ JS Modules ] External Server Dynamic JS

const puppeteer = require('puppeteer');
const { URL } = require('url'); // URL 파서 사용

(async () => {
  const initialUrl = process.argv[2]; // 입력된 URL
  const logs = [];
  let score = 0.0;
  const externalRequests = new Set(); // 고유한 외부 요청 저장
  let initialDomain = null;

  // URL 유효성 검사 및 도메인 추출
  try {
    const parsedUrl = new URL(initialUrl);
    initialDomain = parsedUrl.hostname;
    if (!initialDomain) throw new Error("URL에서 도메인 추출 실패.");
    logs.push(`[Info] Initial domain: ${initialDomain}`); // 도메인 로그
  } catch (e) {
    logs.push(`[Error] Invalid URL: ${initialUrl}`);
    return console.log(JSON.stringify({ logs, score: 0.0, detected_requests: [] })); // 오류 시 종료
  }

  let browser;
  try {
    // Puppeteer 실행
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // 네트워크 요청 가로채기
    page.on('request', request => {
      const requestUrl = request.url();
      try {
        if (!requestUrl.startsWith('http://') && !requestUrl.startsWith('https://') && !requestUrl.startsWith('ftp://') && !requestUrl.startsWith('file://')) {
          return;
        }

        const requestedDomain = new URL(requestUrl).hostname;

        // 외부 도메인 요청 탐지
        if (requestedDomain !== initialDomain && !externalRequests.has(requestUrl)) {
          externalRequests.add(requestUrl); // 요청된 URL을 Set에 추가
          logs.push(`External request to: ${requestedDomain}`); // 로그 기록
        }
      } catch (e) {
        logs.push(`[Warn] Failed to parse request URL: ${requestUrl.substring(0, 80)}...`); // URL 파싱 오류
      }
    });

    // 페이지 이동 및 대기
    logs.push(`Navigating to ${initialUrl}`);
    await page.goto(initialUrl, {
      waitUntil: 'networkidle0', // 네트워크 활동이 완료될 때까지 대기
      timeout: 30000 // 타임아웃 30초
    });

    await new Promise(resolve => setTimeout(resolve, 5000));

    logs.push(`Navigation complete. Final URL: ${page.url()}`);

    // 외부 요청에 따른 점수 계산
    if (externalRequests.size > 0) {
      score = 1.0; // 외부 서버 요청 탐지
      logs.push(`Detected ${externalRequests.size} unique external requests. (+${score})`);
    } else {
      logs.push("No external requests detected (0.0)");
    }

  } catch (error) {
    logs.push(`[Error] Dynamic analysis failed: ${error.message}`);
    score = 0.0; // 실패 시 점수 0
  } finally {
    if (browser) await browser.close(); // 브라우저 종료
  }

  // 결과를 JSON으로 반환 (Python에서 출력)
  console.log(JSON.stringify({
    logs,
    score,
    detected_requests: Array.from(externalRequests) // Set을 Array로 변환
  }));

})();
