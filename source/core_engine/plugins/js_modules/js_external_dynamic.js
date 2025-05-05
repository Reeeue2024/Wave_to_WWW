// [ Core ] Module - JS : js_external_dynamic.py - js_external_dynamic.js

const puppeteer = require("puppeteer");
const { URL } = require("url");

// ( Util ) Add Log
function addLog(logList, message) {
    logList.push(message);
}

// ( Util ) Set Request Intercept
function setRequestIntercept(page, inputHostname, externalList, logList) {
    page.on("request", (request) => {
        const requestUrl = request.url();

        try {
            const prefixList = [ "http://", "https://", "ftp://", "file://" ];

            if (!prefixList.some(prefix => requestUrl.startsWith(prefix))) {
                return;
            }

            const requestHostname = new URL(requestUrl).hostname;

            if (requestHostname !== inputHostname && !externalList.has(requestUrl)) {
                externalList.add(requestUrl);

                addLog(logList, `[ Execute ] External : ${requestHostname}`);
            }
        }
        catch (error) {
            addLog(logList, `[ ERROR ] Fail to Intercept Request ( URL ) : ${requestUrl}`);
        }
    });
}

// ( Main )
async function runExternalDynamic() {
    const inputUrl = process.argv[2];

    let flag = false;
    let score = 0;
    const logList = [];

    const externalList = new Set();

    const inputHostname = new URL(inputUrl).hostname;

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
        // [ 0. ] Set Request Intercept
        setRequestIntercept(page, inputHostname, externalList, logList);

        addLog(logList, `[ Before ] URL : ${inputUrl}`);

        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 10000
        });

        await new Promise(resolve => setTimeout(resolve, 5000));

        addLog(logList, `[ After ] URL : ${page.url()}`);

        if (externalList.size > 0) {
            flag = true;
            addLog(logList, `[ Exist ] Number of External Request : ${externalList.size}`);
            score += 100;
        }
        else {
            flag = false;
            addLog(logList, `[ Not Exist ] Number of External Request : ${externalList.size}`);
            score = 0;
        }
    }
    catch (error) {
        flag = false;
        addLog(logList, `[ ERROR ] Fail : ${error.message}`, 0);
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

runExternalDynamic();
