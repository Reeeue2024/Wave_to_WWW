// [ Core ] Module - JS : js_dom_dynamic.py - js_dom_dynamic.js

const puppeteer = require("puppeteer");
const { URL } = require("url");

// ( Util ) Add Log
function addLog(logList, message, score) {
    logList.push(`${message} ( + ${score} )`);
}

// ( Util ) Get Pattern List
function getPatternList(inputHostname) {
    return [
        {
            patternType : "hideIframe",
            pattern : /<iframe[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
            patternReason : "Exist Hide Iframe.",
            patternWeight : 5,
        },
        {
            patternType : "externalScript",
            pattern: new RegExp(`<script[^>]+src=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Exist External Script.",
            patternWeight : 5,
        },
        {
            patternType : "externalForm",
            pattern: new RegExp(`<form[^>]+action=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Exist External Form.",
            patternWeight : 5,
        },
        {
            patternType : "httpForm",
            pattern: /<form[^>]+action=["']http:\/\/[^>]*>.*?<input[^>]*type=["']password["']/is,
            patternReason : "Exist HTTP Form.",
            patternWeight : 5,
        },
        {
            patternType : "hideLink",
            pattern: /<a[^>]*(display:\s*none|visibility:\s*hidden|width=["']?0["']?|height=["']?0["']?)/i,
            patternReason : "Exist Hide Link.",
            patternWeight : 5,
        },
        {
            patternType : "redirectIframe",
            pattern: new RegExp(`<iframe[^>]+src=["']https?:\/\/(?!.*${inputHostname})`, "i"),
            patternReason : "Exist Redirect Iframe.",
            patternWeight : 5,
        },
        {
            patternType : "metaRefresh",
            pattern: /<meta[^>]+http-equiv=["']refresh["'][^>]+content=["']\d+;\s*url=/i,
            patternReason : "Exist Meta Refresh.",
            patternWeight : 5,
        },
    ];
}

// ( Util ) Create Hook : "Delay Execute"
function createHook(name) {
    return function (inputFunction) {
        return function (...args) {
            window.logExecute("delayExecute", `Execute "Delay Execute" Function. ( ${name} )`, 25);

            return inputFunction.apply(this, args);
        };
    };
}

// ( Util ) Create Hook : "Mutate DOM"
function setDomMutationObserver() {
    const observer = new MutationObserver(mutationList => {
        for (const mutation of mutationList) {
            if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
                window.logExecute("mutateDOM", `Execute "Mutate DOM" Function.`, 25);
            }
        }
    });

    window.addEventListener("DOMContentLoaded", () => {
        observer.observe(document.body, { childList : true, subtree : true });
    });
}

// ( Main )
async function runDomDynamic() {
    const inputUrl = process.argv[2];

    let flag = false;
    let score = 0;
    const logList = [];

    const executePatternList = new Set(); // uniqueScriptElement : Execute
    const existPatternList = new Set(); // uniqueScriptElement : Exist

    const inputHostname = new URL(inputUrl).hostname;

    const patternList = getPatternList(inputHostname);
    
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
                addLog(logList, `[ Execute ( Pattern ) ] ${patternReason}`, patternWeight);
                score += patternWeight;

                executePatternList.add(patternType);
            }
        });

        // [ 0-2. ] Set Hook
        await page.evaluateOnNewDocument(() => {
            setDomMutationObserver();
            
            const hookTimeout = createHook("setTimeout");
            const hookInterval = createHook("setInterval");

            window.setTimeout = hookTimeout(window.setTimeout);
            window.setInterval = hookInterval(window.setInterval);
        });

        // [ 1. ] Start - ( Input ) URL
        await page.goto(inputUrl, {
            waitUntil : "networkidle0",
            timeout : 20000
        });

        const scriptList = await page.$$eval("script", elements =>
            elements.map(el => el.innerText).filter(Boolean)
        );

        const uniqueScriptList = [ ...new Set(scriptList) ];

        for (const uniqueScriptElement of uniqueScriptList) {
            for (const patternElement of patternList) {
                const patternResult = uniqueScriptElement.match(patternElement.pattern);

                if (patternResult) {
                    const reasonData = patternResult[0].trim()
        
                    flag = true;
                    addLog(logList,`${reasonData}]`, patternElement.patternWeight);
                    score += patternElement.patternWeight;

                    existPatternList.add(patternElement.patternType);
                }

                if (patternElement.pattern.test(uniqueScriptElement)) {
                    flag = true;
                    addLog(logList, patternElement.patternReason, patternElement.patternWeight);
                    score += patternElement.patternWeight;

                    existPatternList.add(patternElement.patternType);
                }
            }
        }

        const aTagList = await page.$$("a");

        for (const aTagElement of aTagList) {
            try {
                await aTagElement.click({ delay : 100 });
            }
            catch (_) {}
        }

        await new Promise(resolve => setTimeout(resolve, 5000));

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

runDomDynamic();
