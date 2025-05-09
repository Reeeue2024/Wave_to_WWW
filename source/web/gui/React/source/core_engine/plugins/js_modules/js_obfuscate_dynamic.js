// [ Core ] Module - JS : js_obfuscate_dynamic.py - js_obfuscate_dynamic.js

const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, message) {
    logList.push(message);
}

// ( Util ) Get Pattern List
function getPatternList() {
    return [
        {
            patternType : "base64_obfuscate",
            pattern : /atob\(|btoa\(/,
            patternReason : "Base64 Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "hex_obfuscate",
            pattern : /\\x[0-9a-fA-F]{2}/,
            patternReason : "Hex Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "split_join_obfuscate",
            pattern : /"[a-zA-Z]"\s*\+\s*"[a-zA-Z]"/,
            patternReason : "String Split + Join Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "reverse_join_obfuscate",
            pattern : /split\(.*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)/,
            patternReason : "Reverse + Join Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "random_variable_name_obfuscate",
            pattern : /var\s+_0x[a-f0-9]{4,}/,
            patternReason : "Random Variable Name Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "character_code_obfuscate",
            pattern : /String\.fromCharCode\(/,
            patternReason : "Character Code Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "new_function_obfuscate",
            pattern : /new\s+Function\s*\(/,
            patternReason : "New Function Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "iife_obfuscate",
            pattern : /\(function\s*\(.*\)\s*{.*}\)\s*\(\)/s,
            patternReason : "IIFE Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "self_invoke_function_obfuscate",
            pattern : /var\s+\w+\s*=\s*function\s*\(.*\)\s*{.*};\s*\w+\(\)/s,
            patternReason : "Self Invoke Function Obfuscate Exist.",
            patternWeight : 5,
        },
        {
            patternType : "replace_function_obfuscate",
            pattern : /\.replace\(\s*\/.*\/\s*,\s*function\s*\(/,
            patternReason : "Replace Function Obfuscate Exist.",
            patternWeight : 5,
        },
    ];
}

// ( Main )
async function runObfuscateDynamic() {
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
                addLog(logList, `[ Execute ] ${patternReason} ( + ${patternWeight} )`);
                score += patternWeight;

                executePatternList.add(patternType);
            }
        });

        // [ 0-2. ] Set Hook
        await page.evaluateOnNewDocument(() => {
            const functionPatternList = {
                base64_obfuscate : code => /atob\(|btoa\(/.test(code),
                hex_obfuscate : code => /\\x[0-9a-fA-F]{2}/.test(code),
                character_code_obfuscate : code => code.includes("String.fromCharCode"),
                split_join_obfuscate : code => /"[a-zA-Z]"\s*\+\s*"[a-zA-Z]"/.test(code),
                reverse_join_obfuscate : code => /split\(.*\)\s*\.\s*reverse\(\)\s*\.\s*join\(\)/.test(code),
                random_variable_name_obfuscate : code => /var\s+_0x[a-f0-9]{4,}/.test(code),
                new_function_obfuscate : code => /new\s+Function\s*\(/.test(code),
                iife_obfuscate : code => /\(function\s*\(.*\)\s*{.*}\)\s*\(\)/s.test(code),
                self_invoke_function_obfuscate : code => /var\s+\w+\s*=\s*function\s*\(.*\)\s*{.*};\s*\w+\(\)/s.test(code),
                replace_function_obfuscate : code => /\.replace\(\s*\/.*\/\s*,\s*function\s*\(/.test(code),
            };

            const createHook = (inputFunction, executeFunction, score) => {
                return function (...args) {
                    try {
                        const code = args[0];

                        if (typeof code === "string") {
                            for (const functionPattern in functionPatternList) {
                                if (functionPatternList[functionPattern](code)) {
                                    window.logExecute(functionPattern, `Execute from "${executeFunction}"`, score);
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
            timeout : 10000
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
        score
    }));
}

runObfuscateDynamic();
