// [ Kernel ] Module - JS : js_dynamic_redirect.py - js_dynamic_redirect.js

const puppeteer = require("puppeteer");
const { after } = require("node:test");

// ( Util ) Add Log
function addLog(logList, log) {
    logList.push(`${log}`);
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
async function runDynamicRedirect() {
    const inputUrl = process.argv[2];
    
    let flag = false; // Flag
    const reasonLogList = []; // Reason
    const reasonDataLogList = []; // Reason Data
    const errorLogList = []; // ERROR

    const executePatternList = new Set(); // Unique

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
        // [ 1. ] Set Hook : First Execute
        await page.exposeFunction("logExecute", (reason, reasonData) => {
            const key = `${reason} | ${reasonData}`;

            if (!executePatternList.has(key)) {
                flag = true;
                addLog(reasonLogList, reason);
                addLog(reasonDataLogList, reasonData);

                executePatternList.add(key);

                redirectFlag.value = true;
            }
        });

        // [ 2. ] Set Hook : HTTP Request
        page.on("response", (response) => {
            const status = response.status();

            if (status >= 300 && status < 400) {
                const location = response.headers()["location"] || "Unknown";

                page.evaluate((url) => {
                    window.logExecute("Execute \"HTTP Status Code\"", url);
                }, location);
            }
        });

        // [ 3. ] JavaScript Redirect Detection
        await page.evaluateOnNewDocument(() => {
            const originalAssign = window.location.assign;
            const originalReplace = window.location.replace;
            const originalHref = Object.getOwnPropertyDescriptor(Location.prototype, 'href').set;

            window.location.assign = function (url) {
                window.logExecute("Execute \"window.location.assign\" Redirect.", url);

                return originalAssign.call(this, url);
            };

            window.location.replace = function (url) {
                window.logExecute("Execute \"window.location.replace\" Redirect.", url);

                return originalReplace.call(this, url);
            };

            Object.defineProperty(window.location, "href", {
                set: function (url) {
                    window.logExecute("Execute \"location.href\" Redirect.", url);
                    
                    originalHref.call(window.location, url);
                }
            });
        });

        const beforeRedirectUrl = inputUrl;

        await page.goto(inputUrl, {
            waitUntil: "networkidle0",
            timeout: 10000
        });

        await Promise.race([
            page.waitForNavigation({ waitUntil : "domcontentloaded", timeout : 30000 }).catch(() => {}),
            new Promise(resolve => setTimeout(resolve, 5000))
        ]);

        const afterRedirectUrl = page.url();

        if (beforeRedirectUrl !== afterRedirectUrl || redirectFlag.value) {
            flag = true;
            addLog(reasonLogList, "Execute Redirect.");
            addLog(reasonDataLogList, `${afterRedirectUrl}`);
        } else {
            addLog(reasonLogList, "Not Execute Redirect.");
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

runDynamicRedirect();
