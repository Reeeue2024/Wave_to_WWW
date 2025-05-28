// [ Kernel ] Module - JS : js_dynamic_dom.py - js_dynamic_dom.js

const puppeteer = require("puppeteer");
const { URL } = require("url");

// ( Util ) Add Log
function addLog(logList, log) {
    logList.push(`${log}`);
}

// ( Util ) Get Pattern List
function getPatternList(inputHostname) {
    return [
        {
            patternType : "hideIFrame",
            pattern : /<iframe[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
            patternReason : "Execute DOM Mutate with \"Hide IFrame\" Pattern."
        },
        {
            patternType : "redirectIFrame",
            pattern : new RegExp(`<iframe[^>]+src=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Execute DOM Mutate with \"Redirect IFrame\" Pattern."
        },
        {
            patternType : "externalEmbed",
            pattern : /<(object|embed)[^>]+data=["']https?:\/\/[^"]+/i,
            patternReason : "Execute DOM Mutate with \"External Embed\" Pattern."
        },
        {
            patternType : "externalScript",
            pattern : new RegExp(`<script[^>]+src=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Execute DOM Mutate with \"External Script\" Pattern."
        },
        {
            patternType : "externalForm",
            pattern : new RegExp(`<form[^>]+action=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Execute DOM Mutate with \"External Form\" Pattern."
        },
        {
            patternType : "httpFormPassword",
            pattern : /<form[^>]+action=["']http:\/\/[^>]*>.*?<input[^>]*type=["']password["']/is,
            patternReason : "Execute DOM Mutate with \"HTTP Form with Password\" Pattern."
        },
        {
            patternType : "hideLink",
            pattern : /<a[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
            patternReason : "Execute DOM Mutate with \"Hide Link\" Pattern."
        },
        {
            patternType : "metaRefresh",
            pattern : /<meta[^>]+http-equiv=["']refresh["'][^>]+content=["']\d+;\s*url=[^"]+/i,
            patternReason : "Execute DOM Mutate with \"Meta Refresh\" Pattern."
        }
    ];
}

// ( Main )
async function runDynamicDom() {
    const inputUrl = process.argv[2];

    let flag = false; // Flag
    const reasonLogList = []; // Reason
    const reasonDataLogList = []; // Reason Data
    const errorLogList = []; // ERROR

    const executePatternList = new Set(); // Unique
    const inputHostname = new URL(inputUrl).hostname;
    const patternList = getPatternList(inputHostname);

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
        // [ 1. ] Set Hook
        await page.exposeFunction("logExecute", (reason, reasonData) => {
            if (!executePatternList.has(reasonData)) {
                flag = true;
                addLog(reasonLogList, `${reason}`);
                addLog(reasonDataLogList, `${reasonData}`);
                executePatternList.add(reasonData);
            }
        });

        // [ 2. ] DOM Mutation Hook
        await page.evaluateOnNewDocument((patternList) => {
            const observer = new MutationObserver(mutationList => {
                for (const mutation of mutationList) {
                    if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
                        for (const node of mutation.addedNodes) {
                            if (node.nodeType === 1) {
                                const html = node.outerHTML;
                                for (const pattern of patternList) {
                                    const reg = new RegExp(pattern.pattern, pattern.flags || "i");
                                    const match = html.match(reg);
                                    if (match) {
                                        window.logExecute(pattern.patternReason, match[0].trim());
                                    }
                                }
                            }
                        }
                    }
                }
            });

            window.addEventListener("DOMContentLoaded", () => {
                observer.observe(document.body, { childList : true, subtree : true });
            });
        }, patternList.map(p => ({
            pattern : p.pattern.source,
            flags : p.pattern.flags || "",
            patternReason : p.patternReason
        })));

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

runDynamicDom();
