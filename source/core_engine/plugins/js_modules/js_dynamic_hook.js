// [ Kernel ] Module - JS : js_dynamic_hook.py - js_dynamic_hook.js

const puppeteer = require("puppeteer");

// ( Util ) Add Log
function addLog(logList, log) {
    logList.push(`${log}`);
}

// ( Util ) Get Pattern List
function getPatternList() {
    return [
        {
            patternType : "fetch",
            patternReason : "Execute \"fetch\" Function."
        },
        {
            patternType : "eval",
            patternReason : "Execute \"eval\" Function."
        },
        {
            patternType : "documentWrite",
            patternReason : "Execute \"document.write\" Function."
        },
        {
            patternType : "setTimeout",
            patternReason : "Execute \"setTimeout\" Function."
        },
        {
            patternType : "setInterval",
            patternReason : "Execute \"setInterval\" Function."
        },
        {
            patternType : "addEventListener",
            patternReason : "Execute \"addEventListener\" Function."
        },
        {
            patternType : "localStorage",
            patternReason : "Access to \"localStorage\" Object."
        },
        {
            patternType : "sessionStorage",
            patternReason : "Access to \"sessionStorage\" Object."
        },
        {
            patternType : "XMLHttpRequest",
            patternReason : "Execute \"XMLHttpRequest\" Function."
        },
        {
            patternType : "WebSocket",
            patternReason : "Execute \"WebSocket\" Function."
        },
        {
            patternType : "documentCookie",
            patternReason : "Access to \"document.cookie\" Property."
        }
    ];
}

// ( Main )
async function runDynamicHook() {
    const inputUrl = process.argv[2];

    let flag = false; // Flag
    const reasonLogList = []; // Reason
    const reasonDataLogList = []; // Reason Data
    const errorLogList = []; // ERROR

    const executePatternList = new Set(); // Unique

    const patternList = getPatternList();

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
        await page.evaluateOnNewDocument((patternList) => {
            const executeLogList = new Set();

            function addExecuteLog(reason, reasonData) {
                const key = `${reason} | ${reasonData}`;

                if (!executeLogList.has(key)) {
                    window.logExecute(reason, reasonData);

                    executeLogList.add(key);
                }
            }

            // ( IIFE ) Set Proxy
            (function () {
                const hookList = {
                    fetch : () => {
                        window.fetch = new Proxy(window.fetch, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"fetch\" Function.", args[0]);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    eval : () => {
                        window.eval = new Proxy(window.eval, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"eval\" Function.", args[0]);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    documentWrite : () => {
                        document.write = new Proxy(document.write, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"document.write\" Function.", args.join(" "));

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    setTimeout : () => {
                        window.setTimeout = new Proxy(window.setTimeout, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"setTimeout\" Function.", args[0]);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    setInterval : () => {
                        window.setInterval = new Proxy(window.setInterval, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"setInterval\" Function.", args[0]);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    addEventListener : () => {
                        EventTarget.prototype.addEventListener = new Proxy(EventTarget.prototype.addEventListener, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Execute \"addEventListener\" Function.", args[0]);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    localStorage : () => {
                        localStorage.setItem = new Proxy(localStorage.setItem, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Access to \"localStorage\" Object.", `${args[0]}=${args[1]}`);

                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    sessionStorage : () => {
                        sessionStorage.setItem = new Proxy(sessionStorage.setItem, {
                            apply(target, thisArg, args) {
                                addExecuteLog("Access to \"sessionStorage\" Object.", `${args[0]}=${args[1]}`);
                                
                                return Reflect.apply(target, thisArg, args);
                            }
                        });
                    },
                    XMLHttpRequest : () => {
                        const OriginalXHR = window.XMLHttpRequest;
                        window.XMLHttpRequest = class extends OriginalXHR {
                            constructor(...args) {
                                super(...args);
                                addExecuteLog("Execute \"XMLHttpRequest\" Function.", "new XMLHttpRequest()");
                            }
                        };
                    },
                    WebSocket : () => {
                        const OriginalWebSocket = window.WebSocket;
                        window.WebSocket = class extends OriginalWebSocket {
                            constructor(url, protocols) {
                                super(url, protocols);
                                addExecuteLog("Execute \"WebSocket\" Function.", url);
                            }
                        };
                    },
                    documentCookie : () => {
                        Object.defineProperty(document, "cookie", {
                            set(value) {
                                addExecuteLog("Access to \"document.cookie\" Property.", value);
                            }
                        });
                    },
                };

                for (const pattern of patternList) {
                    if (hookList[pattern.patternType]) {
                        hookList[pattern.patternType]();
                    }
                }
            })();
        }, patternList);

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

runDynamicHook();
