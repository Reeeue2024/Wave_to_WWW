// [ Kernel ] Module - JS : js_hook_dynamic.py - js_hook_dynamic.js

const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, message) {
    logList.push(message);
}

// ( Util ) Get Pattern List
function getPatternList() {
    return [
        {
            patternType : "addEventListener",
            pattern : /addEventListener\s*\(/i,
            patternReason : "Execute \"addEventListener\" Function.",
            patternWeight : 5,
        },
        {
            patternType : "xmlHttpRequest",
            pattern : /XMLHttpRequest\s*\(/i,
            patternReason : "Execute \"XMLHttpRequest\" Function.",
            patternWeight : 6,
        },
        {
            patternType : "fetch",
            pattern : /fetch\s*\(/i,
            patternReason : "Execute \"fetch\" Function.",
            patternWeight : 6,
        },
        {
            patternType : "eval",
            pattern : /eval\s*\(/i,
            patternReason : "Execute \"eval\" Function.",
            patternWeight : 8,
        },
        {
            patternType : "documentWrite",
            pattern : /document\.write\s*\(/i,
            patternReason : "Execute \"document.write\" Function.",
            patternWeight : 4,
        },
        {
            patternType : "setTimeout",
            pattern : /setTimeout\s*\(/i,
            patternReason : "Execute \"setTimeout\" Function.",
            patternWeight : 6,
        },
        {
            patternType : "setInterval",
            pattern : /setInterval\s*\(/i,
            patternReason : "Execute \"setInterval\" Function.",
            patternWeight : 6,
        },
        {
            patternType : "localStorage",
            pattern : /localStorage\s*\./i,
            patternReason : "Access to \"localStorage\" Object.",
            patternWeight : 6,
        },
        {
            patternType : "sessionStorage",
            pattern : /sessionStorage\s*\./i,
            patternReason : "Access to \"sessionStorage\" Object.",
            patternWeight : 6,
        },
        {
            patternType : "webSocket",
            pattern : /WebSocket\s*\(/i,
            patternReason : "Execute \"WebSocket\" Function.",
            patternWeight : 8,
        },
        {
            patternType : "documentCookie",
            pattern : /document\.cookie\s*/i,
            patternReason : "Access to \"document.cookie.\"",
            patternWeight : 8,
        },
        {
            patternType : "window",
            pattern : /window\s*\./i,
            patternReason : "Access to \"window\" Object.",
            patternWeight : 6,
        },
        {
            patternType : "atob",
            pattern : /atob\s*\(/i,
            patternReason : "Execute \"atob\" Function.",
            patternWeight : 8,
        },
        {
            patternType : "btoa",
            pattern : /btoa\s*\(/i,
            patternReason : "Execute \"btoa\" Function.",
            patternWeight : 8,
        },
    ];
}

// ( Main )
async function runHookingDynamic() {
    const inputUrl = process.argv[2];

    let flag = false;
    let score = 0;
    const logList = [];

    const patternList = getPatternList();

    const existPatternList = new Set();
    const executePatternList = new Set(); // To Do

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
        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 5000
        });

        const scriptList = await page.$$eval("script", elements =>
            elements.map(el => (el.outerHTML || "") + "\n" + (el.src || ""))
        );

        for (const scriptElement of scriptList) {
            for (const patternElement of patternList) {
                if (patternElement.pattern.test(scriptElement)) {
                    if (!existPatternList.has(patternElement.patternType)) {
                        flag = true;
                        addLog(logList, `[ Execute ] ${patternElement.patternReason} ( + ${patternElement.patternWeight} )`);
                        score += patternElement.patternWeight;

                        existPatternList.add(patternElement.patternType);
                    }
                }
            }
        }

        await browser.close();
    }
    catch (error) {
        flag = false;
        addLog(logList, `[ ERROR ] Fail : ${error.message}`);
        score += 0;
    }

    console.log(JSON.stringify({
        flag,
        log_list : logList,
        score
    }));
}

runHookingDynamic();
