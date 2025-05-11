// [ Kernel ] Module - JS : js_redirect_dynamic.py - js_redirect_dynamic.js

const { after } = require("node:test");
const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, message) {
    logList.push(message);
}

// ( Util ) Set Hook : Redirect with "HTTP ( HTTPS )"
function redirectHttp(response, redirectFlag, logList) {
    const status = response.status();

    if (status >= 300 && status < 400) {
        addLog(logList, `[ Execute ] Redirect with HTTP ( HTTPS ) : ${status}`);

        redirectFlag.value = true;
    }
}

// ( Main )
async function runRedirectDynamic() {
    const inputUrl = process.argv[2];

    let flag = false;
    let score = 0;
    const logList = [];

    const redirectFlag = { value : false };

    // Execute Chrome
    const browser = await puppeteer.launch({
        headless : true,
        args : [ "--no-sandbox", "--disable-setuid-sandbox" ]
    });

    const page = await browser.newPage();

    // Performance
    await page.setRequestInterception(true);
    page.on("request", (request) => {
        const blockTypeList = [ "image", "stylesheet", "font" ];

        if (blockTypeList.includes(request.resourceType())) {
            request.abort();
        }
        else {
            request.continue();
        }
    });

    try {
        // [ 0-1. ] Set Hook for Hook
        await page.exposeFunction("logExecute", (message) => {
            addLog(logList, message);

            redirectFlag.value = true;
        });

        // [ 0-2-1. ] Set Hook : Redirect with "HTTP ( HTTPS )"
        page.on("response", (response) => {
            redirectHttp(response, redirectFlag, logList);
        });

        // [ 0-2-2. ] Set Hook : Redirect with "window.locaion"
        await page.evaluateOnNewDocument(() => {
            const beforeAssign = window.location.assign;

            window.location.assign = function (newLocation) {
                window.logExecute(`[ Execute ] Redirect with "window.location" : ${newLocation}`);
                
                return beforeAssign.call(this, newLocation);
            };
        });

        const redirectStartTime = Date.now();

        await page.goto(inputUrl, {
            waitUntil : "domcontentloaded",
            timeout : 30000
        });

        const timeoutPromise = new Promise(resolve => setTimeout(resolve, 5000));

        await Promise.race([
            page.waitForNavigation({ waitUntil : "domcontentloaded", timeout : 30000 }).catch(() => {}),
            timeoutPromise
        ]);

        const afterUrl = page.url();
        const redirectEndTime = Date.now();

        const redirectTime = (redirectEndTime - redirectStartTime) / 1000;

        if (inputUrl !== afterUrl || redirectFlag.value === true) {
            flag = true;
            addLog(logList, `Execute Redirect. ( Redirect URL : ${afterUrl})`);

            if (redirectTime <= 3) {
                addLog(logList, `Fast Redirect. ( Redirect Time : ${redirectTime} ) ( + ${score} )`);
                score = 60;
            }
            else if (redirectTime <= 5) {
                addLog(logList, `Not Fast / Not Slow Redirect. ( Redirect Time : ${redirectTime} ) ( + ${score} )`);
                score = 40;
            }
            else {
                addLog(logList, `Slow Redirect. ( Redirect Time : ${redirectTime} ) ( + ${score} )`);
                score = 20;
            }
        }
        else {
            flag = false;
            addLog(logList, `Not Execute Redirect.`);
            score = 0;
        }
    }
    catch (error) {
        flag = false;
        addLog(logList, `[ ERROR ] Fail : ${error.message}`);
        score += 0;
    }
    finally {
        await browser.close();
    }

    console.log(JSON.stringify({
        flag,
        log_list : logList,
        score
    }));
}

runRedirectDynamic();
