// [ Kernel ] Module - JS : js_dynamic_obfuscate.py - js_dynamic_obfuscate.js

const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, log) {
    logList.push(`${log}`);
}

// ( Util ) Get Pattern List
function getPatternList() {
    return [
        {
            patternType : "obfuscateBase64",
            pattern : /(?:atob|btoa)\s*\(\s*[^)]+\s*\)/,
            patternReason : "Execute Base64 Obfuscate in JS."
        },
        {
            patternType : "obfuscateHex",
            pattern : /\\x[0-9a-fA-F]{2}/,
            patternReason : "Execute Hex Obfuscate in JS."
        },
        {
            patternType : "obfuscateSplitJoin",
            pattern : /(['"][a-zA-Z]{1,3}['"]\s*\+\s*['"][a-zA-Z]{1,3}['"])(\s*\+\s*['"][a-zA-Z]{1,3}['"])*?/,
            patternReason : "Execute String Split + Join Obfuscate in JS."
        },
        {
            patternType : "obfuscateReverseJoin",
            pattern : /["'][^"']+["']\s*\.split\s*\(\s*["'].*?["']\s*\)\s*\.reverse\s*\(\)\s*\.join\s*\(\s*["']?.*?["']?\s*\)/,
            patternReason : "Execute Reverse + Join Obfuscate in JS."
        },
        {
            patternType : "obfuscateRandomVriableName",
            pattern : /\bvar\s+_0x[a-f0-9]{4,}\b/,
            patternReason : "Execute Random Variable Name Obfuscate in JS."
        },
        {
            patternType : "obfuscateCharacterCode",
            pattern : /String\.fromCharCode\s*\(\s*[0-9,\s]+\)/,
            patternReason : "Execute Character Code Obfuscate in JS."
        },
        {
            patternType : "obfuscateNewFunction",
            pattern : /new\s+Function\s*\(\s*(['"].*?['"]\s*,\s*)*['"].*?['"]\s*\)/,
            patternReason : "Execute New Function Obfuscate in JS."
        },
        {
            patternType : "obfuscateReplaceFunction",
            pattern : /\.replace\s*\(\s*\/.*?\/\s*,\s*function\s*\([^)]*\)\s*{[^}]*}\s*\)/,
            patternReason : "Execute Replace Function Obfuscate in JS."
        }
    ];
}

// ( Main )
async function runDynamicObfuscate() {
    const inputUrl = process.argv[2];

    let flag = false; // Flag
    const reasonLogList = []; // Reason
    const reasonDataLogList = []; // Reason Data
    const errorLogList = []; // ERROR

    const executePatternList = new Set(); // Unique

    const originalPatternList = getPatternList();

    const serializePatternList = originalPatternList.map(p => ({
        patternType : p.patternType,
        patternReason : p.patternReason,
        pattern : p.pattern.source,
        flags : p.pattern.flags || ""
    }));

    // Execute Chrome
    const browser = await puppeteer.launch({
        headless : true,
        // headless : false,
        // devtools : true,
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
            if (!executePatternList.has(reasonData)) {
                flag = true;
                addLog(reasonLogList, `${reason}`); // Reason
                addLog(reasonDataLogList, `${reasonData}`); // Reason Data

                executePatternList.add(reasonData);
            }
        });

        // [ 2. ] Set Hook
        await page.evaluateOnNewDocument((serializePatterns) => {
            const patternList = JSON.parse(serializePatterns).map(p => ({
                patternType : p.patternType,
                patternReason : p.patternReason,
                pattern : new RegExp(p.pattern, p.flags)
            }));

            const executeLogList = new Set();

            function addExecuteLog(reason, reasonData) {
                const key = `${reason} | ${reasonData}`;

                if (!executeLogList.has(key)) {
                    window.logExecute(reason, reasonData);

                    executeLogList.add(key);
                }
            }

            function scanPattern(code, context) {
                if (typeof code !== "string") return;

                for (const pattern of patternList) {
                    if (pattern.pattern.test(code)) {
                        addExecuteLog(pattern.patternReason, `"${context}" : ${code}`);
                    }
                }
            }

            // ( IIFE ) Set Proxy
            (function () {
                const hookList = {
                    eval : () => {
                        window.eval = new Proxy(window.eval, {
                            apply(target, thisArg, args) {
                                scanPattern(args[0], "eval");

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    Function : () => {
                        window.Function = new Proxy(window.Function, {
                            apply(target, thisArg, args) {
                                scanPattern(args[0], "Function");

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    setTimeout : () => {
                        window.setTimeout = new Proxy(window.setTimeout, {
                            apply(target, thisArg, args) {
                                scanPattern(args[0], "setTimeout");

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    setInterval : () => {
                        window.setInterval = new Proxy(window.setInterval, {
                            apply(target, thisArg, args) {
                                scanPattern(args[0], "setInterval");
                                
                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    }
                };

                for (const hookKey in hookList) {
                    hookList[hookKey]();
                }
            })();
        }, JSON.stringify(serializePatternList));

        // [ 3. ] Start
        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 10000
        });

        await new Promise(resolve => setTimeout(resolve, 5000));
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

runDynamicObfuscate();
