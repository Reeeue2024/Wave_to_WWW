// [ Kernel ] Module - JS : js_script_dynamic.py - js_script_dynamic.js

const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, message) {
    logList.push(message);
}

// ( Util ) Get Pattern List
function getPatternList() {
    return [
        {
            patternType : "inline_event_script",
            pattern : /<script[^>]*>.*(onerror|onload|onclick)=.*<\/script>/,
            patternReason : "Inline Event Script Exist.",
            patternWeight : 15,
        },
        {
            patternType : "data_uri_script",
            pattern : /data:text\/javascript/,
            patternReason : "Data URI Script Exist.",
            patternWeight : 20,
        },
        {
            patternType : "document_write_script",
            pattern : /document\.write(ln)?\s*\(/,
            patternReason : "Document Write Script Exist.",
            patternWeight : 15,
        },
        {
            patternType : "base64_script",
            pattern : /atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}/,
            patternReason : "Base64 Script Exist.",
            patternWeight : 10,
        },
        {
            patternType : "inline_image_tag_script",
            pattern : /<img[^>]+src=['"]javascript:/,
            patternReason : "Inline Image Tag Script Exist.",
            patternWeight : 20,
        },
        {
            patternType : "iframe_script",
            pattern : /<iframe[^>]+src=['"]javascript:/,
            patternReason : "Iframe Script Exist.",
            patternWeight : 20,
        },
        {
            patternType : "document_cookie_script",
            pattern : /document\.cookie/,
            patternReason : "Document Cookie Script Exist.",
            patternWeight : 10,
        },
    ];
}

// ( Main )
async function runScriptDynamic() {
    const inputUrl = process.argv[2];

    let flag = false;
    let score = 0;
    const logList = [];

    const existPatternList = new Set();
    const executePatternList = new Set();

    const patternList = getPatternList();

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
        await page.exposeFunction("logExecute", (patternType, patternReason, patternWeight) => {
            if (existPatternList.has(patternType) && !executePatternList.has(patternType)) {
                flag = true;
                addLog(logList, `[ Execute ( Pattern ) ] ${patternReason} ( + ${patternWeight} )`);
                score += patternWeight;

                executePatternList.add(patternType);
            }
        });

        // [ 0-2. ] Set Hook
        await page.evaluateOnNewDocument(() => {
            const functionPatternList = {
                inline_event_script : code => /<script[^>]*>.*(onerror|onload|onclick)=.*<\/script>/.test(code),
                data_uri_script : code => /data:text\/javascript/.test(code),
                document_write_script : code => /document\.write(ln)?\s*\(/.test(code),
                base64_script : code => /atob\s*\(|btoa\s*\(|[A-Za-z0-9+/]{50,}={0,2}/.test(code),
                inline_image_tag_script : code => /<img[^>]+src=['"]javascript:/.test(code),
                iframe_script : code => /<iframe[^>]+src=['"]javascript:/.test(code),
                document_cookie_script : code => /document\.cookie/.test(code)
            };

            const createHook = (inputFunction, executeFunction, weight) => {
                return function (...args) {
                    try {
                        const code = args[0];

                        if (typeof code === "string") {
                            for (const functionPattern in functionPatternList) {
                                if (functionPatternList[functionPattern](code)) {
                                    window.logExecute(functionPattern, `Execute from "${executeFunction}"`, weight);
                                }
                            }
                        }
                    }
                    catch (_) {}

                    return inputFunction.apply(this, args);
                };
            };

            window.eval = createHook(window.eval, "eval", 15);
            window.Function = createHook(window.Function, "Function", 15);
            window.setTimeout = createHook(window.setTimeout, "setTimeout", 10);
            window.setInterval = createHook(window.setInterval, "setInterval", 10);
        });

        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 5000
        });

        const scriptList = await page.$$eval("script", elements =>
            elements.map(el => el.innerText).filter(Boolean)
        );

        const uniqueScriptList = [ ...new Set(scriptList) ];

        for (const scriptElement of uniqueScriptList) {
            for (const patternElement of patternList) {
                const patternResult = scriptElement.match(patternElement.pattern);

                if (patternResult) {
                    if (!existPatternList.has(patternElement.patternType)) {
                        const reasonData = patternResult[0];

                        flag = true;
                        addLog(logList, `[ Exist ] ${patternElement.patternReason} ( + ${patternElement.patternWeight} )`);
                        addLog(logList, `Reason Data : ${reasonData}`);
                        score += patternElement.patternWeight;

                        existPatternList.add(patternElement.patternType);
                    }
                }
            }
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
        score,
    }));
}

runScriptDynamic();
