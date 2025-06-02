// React/src/components/descriptions.js
// 피싱 탐지 결과 페이지에서 사용하는 카테고리 및 모듈 설명 정보 정의

// 모듈 이름의 접두사에 따라 카테고리 이름을 정의
export const categoryMap = {
  Ai: 'AI-based Detection',
  Url: 'URL Structure Analysis',
  Html: 'HTML Content Analysis',
  JsStatic: 'Static JavaScript Analysis',
  JsDynamic: 'Dynamic JavaScript Analysis'
};

// 각 카테고리에 대한 설명 (DETAILS 탭에서 사용됨)
export const categoryDescriptions = {
  Ai: "This section displays results from AI-based phishing detection modules. These modules use trained machine learning models to analyze the URL, webpage structure, and behavioral patterns learned from phishing datasets to assess the risk level.",
  Url: "This section analyzes the structure and composition of the URL. Features such as excessive length, use of URL shorteners, multiple subdomains, or homograph characters (which visually mimic trusted domains) may indicate phishing attempts.",
  Html: "This section examines the HTML source for suspicious tag usage. Tags like <form>, <iframe>, and <meta refresh> are commonly used by attackers to hide malicious behavior or trigger automatic redirection.",
  JsStatic: "This section analyzes the static JavaScript code embedded in the webpage. It detects hardcoded redirection logic, obfuscated scripts, unauthorized event listeners, or external script loading from suspicious domains.",
  JsDynamic: "This section observes JavaScript behavior at runtime. It identifies DOM manipulations, dynamically injected scripts, runtime code obfuscation, or redirect attempts triggered after the page has loaded."
};

// 각 탐지 모듈별 이름, 간단 설명, 상세 설명 정의
export const moduleDescriptions = {
  // URL 모듈
  UrlShort: {
    name: 'Shortened URL Usage',
    description: 'Detects if the URL uses shortening services.',
    longDescription: 'Shortened URLs like those from bit.ly or tinyurl hide the destination link, which attackers often exploit to deceive users into clicking malicious links without realizing it. This module flags such usage for inspection.'
  },
  UrlSubDomain: {
    name: 'Subdomain Usage',
    description: 'Detects if the URL has excessive subdomains.',
    longDescription: 'Phishing domains often use multiple subdomains to impersonate legitimate services (e.g., login.bank.example.com.fake.site). This module evaluates the depth and suspiciousness of subdomain patterns.'
  },
  UrlHttp: {
    name: 'HTTP Protocol Usage',
    description: 'Detects if the URL uses insecure HTTP.',
    longDescription: 'Phishing sites often avoid HTTPS certificates due to cost or verification. This module checks if the URL uses unencrypted HTTP, indicating potential insecurity or deception.'
  },
  UrlSsl: {
    name: 'SSL Certificate Usage',
    description: 'Detects if the domain lacks a valid SSL certificate.',
    longDescription: 'Secure websites typically use verified SSL certificates. This module checks for missing, expired, or self-signed SSL certificates that may indicate phishing or spoofing attempts.'
  },
  UrlWhois: {
    name: 'WHOIS Data Usage',
    description: 'Detects suspicious domain registration information.',
    longDescription: 'WHOIS records provide domain ownership details. Recently registered domains or domains with redacted ownership often indicate malicious intent. This module checks such anomalies.'
  },
  UrlHomograph: {
    name: 'Homograph Usage',
    description: 'Detects use of visually deceptive characters in domains.',
    longDescription: 'Phishers use homograph attacks to register domains like “gοοgle.com” (with Greek letters) to trick users. This module detects such deceptive character patterns in domain names.'
  },

  // HTML 모듈
  HtmlForm: {
    name: 'Form Tag Usage',
    description: 'Detects suspicious or missing form actions.',
    longDescription: 'Phishing pages often include login or payment forms with missing or malicious `action` attributes. This module analyzes forms to detect fake submission paths or credential harvesting attempts.'
  },
  HtmlIframe: {
    name: 'IFrame Tag Usage',
    description: 'Detects hidden or potentially malicious iframe tags.',
    longDescription: 'IFrames can embed external content invisibly, enabling malicious redirects or data theft. This module flags iframes with zero size, hidden attributes, or unknown sources.'
  },
  HtmlJsUrl: {
    name: 'JavaScript URL Usage',
    description: 'Detects embedded JavaScript URLs like "javascript:".',
    longDescription: 'URLs starting with `javascript:` can execute arbitrary code upon user interaction. This module flags these as potential vectors for drive-by downloads or UI redressing.'
  },
  HtmlLink: {
    name: 'Link Tag Usage',
    description: 'Detects external stylesheet or resource links.',
    longDescription: 'Attackers may load external CSS/JS to obfuscate or control page behavior. This module checks if external resources originate from untrusted or suspicious domains.'
  },
  HtmlMetaRefresh: {
    name: 'Meta Refresh Tag Usage',
    description: 'Detects auto-refresh behavior using meta tags.',
    longDescription: 'Meta-refresh tags can automatically redirect users to another URL without user action, often used in phishing sites to bounce users. This module identifies such behavior.'
  },
  HtmlResourceUrl: {
    name: 'Resource URL Usage',
    description: 'Detects loading of external scripts or media.',
    longDescription: 'External resources can be used to track, fingerprint, or load malicious content. This module flags URLs pointing to untrusted external hosts in HTML tags like `img`, `script`, or `video`.'
  },
  HtmlStyle: {
    name: 'Style Tag Usage',
    description: 'Detects suspicious inline CSS or hidden styles.',
    longDescription: 'Inline styles that obscure content, move elements off-screen, or hide input fields may indicate phishing techniques. This module scans for such styling tricks.'
  },

  // JS static 모듈
  JsStaticExternal: {
    name: 'External Script Usage',
    description: 'Detects loading of scripts from unknown domains.',
    longDescription: 'Loading scripts from third-party domains allows attackers to inject dynamic payloads. This module flags scripts sourced from unverified origins.'
  },
  JsStaticHook: {
    name: 'Event Hook Usage',
    description: 'Detects misuse of JavaScript event listeners.',
    longDescription: 'Event listeners like `onClick` or `onSubmit` can be abused to intercept user actions. This module checks if scripts misuse event hooks to redirect or collect input data.'
  },
  JsStaticObfuscate: {
    name: 'Code Obfuscation Usage',
    description: 'Detects obfuscated or encoded JavaScript code.',
    longDescription: 'Obfuscated JavaScript hides malicious intent by encoding logic in unreadable forms. This module detects patterns like `eval`, `atob`, or hexadecimal/Unicode string composition.'
  },
  JsStaticRedirect: {
    name: 'Static Redirect Usage',
    description: 'Detects hardcoded redirection logic.',
    longDescription: 'Hardcoded redirects using `window.location` or `meta-refresh` scripts can auto-redirect users without interaction. This module scans for such static redirect logic.'
  },
  JsStaticScript: {
    name: 'Script Tag Usage',
    description: 'Detects suspicious usage of script tags.',
    longDescription: 'This module analyzes the usage of `<script>` tags, especially inline ones, to detect embedded malicious payloads or unauthorized logic directly injected into the page.'
  },

  // JS dynamic 모듈
  JsDynamicDom: {
    name: 'DOM Manipulation Usage',
    description: 'Detects live DOM changes using JavaScript.',
    longDescription: 'Phishing pages may dynamically create or modify DOM elements to avoid static detection. This module observes live DOM changes that are abnormal or deceptive.'
  },
  JsDynamicExternal: {
    name: 'Script Injection Usage',
    description: 'Detects dynamically injected scripts at runtime.',
    longDescription: 'JavaScript code that injects `<script>` tags or uses functions like `eval`, `Function()`, or `document.write` dynamically can introduce runtime payloads. This module flags such behaviors.'
  },
  JsDynamicHook: {
    name: 'Event Hook Usage',
    description: 'Detects dynamic registration of event handlers.',
    longDescription: 'Event listeners registered at runtime (e.g., `addEventListener`) may be used to steal input or alter user experience. This module tracks event hook usage during page interaction.'
  },
  JsDynamicObfuscate: {
    name: 'Code Obfuscation Usage',
    description: 'Detects runtime code obfuscation in JavaScript.',
    longDescription: 'Runtime obfuscation makes code harder to analyze by dynamically generating functions or re-encoding logic. This module watches for suspicious transformations after the page loads.'
  },
  JsDynamicRedirect: {
    name: 'Redirect Usage',
    description: 'Detects JavaScript-based URL redirection.',
    longDescription: 'JavaScript can redirect users post-load via `window.location` or similar methods. Phishers use this to delay redirect until after AI or scanners finish analysis. This module flags such logic.'
  }
};

