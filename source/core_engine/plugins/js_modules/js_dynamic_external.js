// [ Kernel ] Module - JS : js_dynamic_external.py - js_dynamic_external.js

const puppeteer = require("puppeteer");
const { URL } = require("url");

// ( Util ) Add Log
function addLog(logList, log) {
    logList.push(`${log}`);
}

// ( Util ) Create Hook : Request
function setRequestHook(page, inputUrl, executeExternalList, reasonLogList, reasonDataLogList, errorLogList) {
    const inputOrigin = new URL(inputUrl).origin;

    page.on("request", (request) => {
        const requestUrl = request.url();

        try {
            const requestOrigin = new URL(requestUrl).origin;

            if (inputOrigin !== requestOrigin && !executeExternalList.has(requestUrl)) {
                executeExternalList.add(requestUrl);

                addLog(reasonLogList, "Execute Request to External.");
                addLog(reasonDataLogList, `${requestUrl}`);
            }
        }
        catch (error) {
            addLog(errorLogList, `[ ERROR ] Fail : ${error.message}`);
        }
    });
}

// ( Main )
async function runDynamicExternal() {
    const inputUrl = process.argv[2];

    let flag = false; // Flag
    const reasonLogList = []; // Reason
    const reasonDataLogList = []; // Reason Data
    const errorLogList = []; // ERROR

    const executeExternalList = new Set(); // Unique
    
    // Execute Chrome
    const browser = await puppeteer.launch({
        headless : true,
        args : [ "--no-sandbox", "--disable-setuid-sandbox" ]
    });

    const page = await browser.newPage();

    try {
        setRequestHook(page, inputUrl, executeExternalList, reasonLogList, reasonDataLogList, errorLogList);

        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 10000
        });

        await new Promise(resolve => setTimeout(resolve, 5000));

        if (executeExternalList.size > 0) {
            flag = true;
        }
        else {
            flag = false;

            addLog(reasonLogList, "Not Execute Request to External.");
            addLog(reasonDataLogList, "");
        }
    }
    catch (error) {
        flag = false;
        addLog(errorLogList, `[ ERROR ] Fail : ${error.message}`);
    }
    finally {
        await browser.close();
    }

    console.log(JSON.stringify({
        flag,
        reason_log_list : reasonLogList,
        reason_data_log_list : reasonDataLogList,
        error_log_list : errorLogList,
    }));
}

runDynamicExternal();
