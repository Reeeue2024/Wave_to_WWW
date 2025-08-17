// React/src/components/descriptions.js
// 피싱 탐지 결과 페이지에서 사용하는 카테고리 및 모듈 설명 정보 정의

// 모듈 이름의 접두사에 따라 카테고리 이름을 정의
export const categoryMap = {
  Ai: { en: 'AI-based Detection', ko: 'AI 기반 탐지' },
  Url: { en: 'URL Structure Analysis', ko: 'URL 구조 분석' },
  Html: { en: 'HTML Content Analysis', ko: 'HTML 콘텐츠 분석' },
  JsStatic: { en: 'Static JavaScript Analysis', ko: '정적 JavaScript 분석' },
  JsDynamic: { en: 'Dynamic JavaScript Analysis', ko: '동적 JavaScript 분석' }
};

// 각 카테고리에 대한 설명 (DETAILS 탭에서 사용됨)
export const categoryDescriptions = {
  Ai: {
    en: "This section displays results from AI-based phishing detection modules. These modules use trained machine learning models to analyze the URL, webpage structure, and behavioral patterns learned from phishing datasets to assess the risk level.",
    ko: "AI 기반 피싱 탐지 모듈의 결과를 보여줍니다. 학습된 머신러닝 모델이 URL, 웹페이지 구조, 피싱 데이터셋에서 학습한 패턴을 분석해 위험도를 판단합니다."
  },
  Url: {
    en: "This section analyzes the structure and composition of the URL. Features such as excessive length, use of URL shorteners, multiple subdomains, or homograph characters (which visually mimic trusted domains) may indicate phishing attempts.",
    ko: "URL의 구조와 구성 요소를 분석합니다. URL 길이, 단축 URL, 과도한 서브도메인, 시각적으로 유사한 문자를 사용하는지 여부 등을 탐지합니다."
  },
  Html: {
    en: "This section examines the HTML source for suspicious tag usage. Tags like <form>, <iframe>, and <meta refresh> are commonly used by attackers to hide malicious behavior or trigger automatic redirection.",
    ko: "HTML 소스 내에서 의심스러운 태그(`<form>`, `<iframe>`, `<meta refresh>` 등)의 사용 여부를 검사합니다."
  },
  JsStatic: {
    en: "This section analyzes the static JavaScript code embedded in the webpage. It detects hardcoded redirection logic, obfuscated scripts, unauthorized event listeners, or external script loading from suspicious domains.",
    ko: "웹페이지에 포함된 정적 JavaScript 코드 내 하드코딩된 리디렉션, 난독화된 코드, 외부 스크립트 등을 분석합니다."
  },
  JsDynamic: {
    en: "This section observes JavaScript behavior at runtime. It identifies DOM manipulations, dynamically injected scripts, runtime code obfuscation, or redirect attempts triggered after the page has loaded.",
    ko: "웹페이지 실행 중 동적으로 삽입되거나 조작되는 JavaScript 코드의 행동을 관찰하여 피싱 여부를 판단합니다."
  }
};

// 각 탐지 모듈별 이름, 간단 설명, 상세 설명 정의
export const moduleDescriptions = {
  Ai: {
    name: { en: 'AI', ko: 'AI' },
    description: {
      en: 'Detects phishing using 29 features from URL, HTML, and domain data.',
      ko: 'URL, HTML, 도메인 데이터를 바탕으로 29가지 특징을 분석해 피싱을 탐지합니다.'
    },
    longDescription: {
      en: 'Our AI model analyzes 29 carefully selected features extracted from the URL structure, HTML content, and domain-related information to detect phishing websites. With a detection accuracy of over 96%, it provides reliable and real-time threat assessment based on data-driven insights.',
      ko: 'AI 모델은 URL 구조, HTML 콘텐츠, 도메인 관련 정보를 종합 분석해 피싱 여부를 판단합니다. 탐지 정확도는 96% 이상이며 실시간 위험 평가를 제공합니다.'
    }
  },

  // URL 모듈
  UrlShort: {
    name: { en: 'Shortened URL Usage', ko: '단축 URL 사용 여부' },
    description: {
      en: 'Detects if the URL uses shortening services.',
      ko: 'URL이 단축 서비스를 사용하는지 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Shortened URLs like those from bit.ly or tinyurl hide the destination link, which attackers often exploit to deceive users into clicking malicious links without realizing it. This module flags such usage for inspection.',
      ko: 'bit.ly, tinyurl과 같은 단축 URL은 최종 목적지를 숨겨 사용자 클릭을 유도할 수 있어 피싱에 악용됩니다.'
    }
  },
  UrlSubDomain: {
    name: { en: 'Subdomain Usage', ko: '서브도메인 사용' },
    description: {
      en: 'Detects if the URL has excessive subdomains.',
      ko: 'URL에 과도한 수의 서브도메인이 포함되어 있는지 확인합니다.'
    },
    longDescription: {
      en: 'Phishing domains often use multiple subdomains to impersonate legitimate services (e.g., login.bank.example.com.fake.site). This module evaluates the depth and suspiciousness of subdomain patterns.',
      ko: '피싱 사이트는 `login.bank.example.com.fake.site`처럼 신뢰받는 도메인을 흉내내는 데 서브도메인을 활용합니다.'
    }
  },
  UrlHttp: {
    name: { en: 'HTTP Protocol Usage', ko: 'HTTP 프로토콜 사용' },
    description: {
      en: 'Detects if the URL uses insecure HTTP.',
      ko: '암호화되지 않은 HTTP 프로토콜을 사용하는지 탐지합니다.'
    },
    longDescription: {
      en: 'Phishing sites often avoid HTTPS certificates due to cost or verification. This module checks if the URL uses unencrypted HTTP, indicating potential insecurity or deception.',
      ko: 'HTTPS 인증서 발급을 피한 피싱 사이트는 HTTP를 사용하는 경우가 많습니다.'
    }
  },
  UrlSsl: {
    name: { en: 'SSL Certificate Usage', ko: 'SSL 인증서 사용 여부' },
    description: {
      en: 'Detects if the domain lacks a valid SSL certificate.',
      ko: '도메인이 유효한 SSL 인증서를 갖추지 않았는지 확인합니다.'
    },
    longDescription: {
      en: 'Secure websites typically use verified SSL certificates. This module checks for missing, expired, or self-signed SSL certificates that may indicate phishing or spoofing attempts.',
      ko: '정상적인 사이트는 유효한 SSL 인증서를 사용하며, 만료되었거나 자체 서명된 인증서는 위험 신호입니다.'
    }
  },
  UrlWhois: {
    name: { en: 'WHOIS Data Usage', ko: 'WHOIS 정보 분석' },
    description: {
      en: 'Detects suspicious domain registration information.',
      ko: '의심스러운 도메인 등록 정보를 탐지합니다.'
    },
    longDescription: {
      en: 'WHOIS records provide domain ownership details. Recently registered domains or domains with redacted ownership often indicate malicious intent. This module checks such anomalies.',
      ko: 'WHOIS 데이터에서 등록자 정보가 누락되었거나 너무 최근에 등록된 도메인은 위험합니다.'
    }
  },
  UrlHomograph: {
    name: { en: 'Homograph Usage', ko: '동형이의어(Homograph) 사용' },
    description: {
      en: 'Detects use of visually deceptive characters in domains.',
      ko: '도메인 내 시각적으로 유사한 문자의 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Phishers use homograph attacks to register domains like “gοοgle.com” (with Greek letters) to trick users. This module detects such deceptive character patterns in domain names.',
      ko: '피싱 사이트는 “gοοgle.com”처럼 유사한 외국 문자를 사용하여 정상 도메인을 위장합니다.'
    }
  },

  // HTML 모듈
  HtmlForm: {
    name: { en: 'Form Tag Usage', ko: 'Form 태그 사용' },
    description: {
      en: 'Detects suspicious or missing form actions.',
      ko: '의심스럽거나 누락된 form 액션을 탐지합니다.'
    },
    longDescription: {
      en: 'Phishing pages often include login or payment forms with missing or malicious `action` attributes. This module analyzes forms to detect fake submission paths or credential harvesting attempts.',
      ko: '피싱 페이지는 종종 로그인 또는 결제 양식을 포함하며, 그 안에 악성 제출 경로나 누락된 액션을 포함할 수 있습니다.'
    }
  },
  HtmlIframe: {
    name: { en: 'IFrame Tag Usage', ko: 'IFrame 태그 사용' },
    description: {
      en: 'Detects hidden or potentially malicious iframe tags.',
      ko: '숨겨진 iframe이나 악성 iframe 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'IFrames can embed external content invisibly, enabling malicious redirects or data theft. This module flags iframes with zero size, hidden attributes, or unknown sources.',
      ko: 'IFrame은 외부 콘텐츠를 눈에 띄지 않게 삽입할 수 있어, 피싱 페이지에서 리디렉션이나 정보 탈취에 활용될 수 있습니다.'
    }
  },
  HtmlJsUrl: {
    name: { en: 'JavaScript URL Usage', ko: '자바스크립트 URL 사용' },
    description: {
      en: 'Detects embedded JavaScript URLs like "javascript:".',
      ko: '"javascript:"로 시작하는 URL 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'URLs starting with `javascript:` can execute arbitrary code upon user interaction. This module flags these as potential vectors for drive-by downloads or UI redressing.',
      ko: '`javascript:`로 시작하는 URL은 클릭 시 악성 코드를 실행할 수 있어 위험 요소로 간주됩니다.'
    }
  },
  HtmlLink: {
    name: { en: 'Link Tag Usage', ko: 'Link 태그 사용' },
    description: {
      en: 'Detects external stylesheet or resource links.',
      ko: '외부 CSS나 리소스 링크 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Attackers may load external CSS/JS to obfuscate or control page behavior. This module checks if external resources originate from untrusted or suspicious domains.',
      ko: '공격자는 외부 CSS나 JS를 통해 페이지 동작을 제어하거나 난독화할 수 있습니다.'
    }
  },
  HtmlMetaRefresh: {
    name: { en: 'Meta Refresh Tag Usage', ko: 'Meta Refresh 태그 사용' },
    description: {
      en: 'Detects auto-refresh behavior using meta tags.',
      ko: 'meta 태그를 통한 자동 새로고침(리디렉션) 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Meta-refresh tags can automatically redirect users to another URL without user action, often used in phishing sites to bounce users. This module identifies such behavior.',
      ko: 'meta-refresh는 사용자 동의 없이 다른 페이지로 자동 이동시킬 수 있어 피싱에 활용됩니다.'
    }
  },
  HtmlResourceUrl: {
    name: { en: 'Resource URL Usage', ko: '리소스 URL 사용' },
    description: {
      en: 'Detects loading of external scripts or media.',
      ko: '외부 스크립트나 미디어 리소스 로딩 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'External resources can be used to track, fingerprint, or load malicious content. This module flags URLs pointing to untrusted external hosts in HTML tags like `img`, `script`, or `video`..',
      ko: '외부 자원을 로드하는 것은 사용자 추적, 지문 채취, 악성 코드 삽입에 이용될 수 있습니다.'
    }
  },
  HtmlStyle: {
    name: { en: 'Style Tag Usage', ko: 'Style 태그 사용' },
    description: {
      en: 'Detects suspicious inline CSS or hidden styles.',
      ko: '의심스러운 인라인 스타일이나 숨김 스타일 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Inline styles that obscure content, move elements off-screen, or hide input fields may indicate phishing techniques. This module scans for such styling tricks.',
      ko: '피싱 공격자는 콘텐츠를 가리거나 입력 필드를 숨기는 인라인 CSS를 사용할 수 있습니다.'
    }
  },

  // JS static 모듈
  JsStaticExternal: {
    name: { en: 'External Script Usage', ko: '외부 스크립트 사용' },
    description: {
      en: 'Detects loading of scripts from unknown domains.',
      ko: '알 수 없는 도메인에서 스크립트를 로드하는지 탐지합니다.'
    },
    longDescription: {
      en: 'Loading scripts from third-party domains allows attackers to inject dynamic payloads. This module flags scripts sourced from unverified origins.',
      ko: '공격자는 외부 도메인을 통해 악성 스크립트를 주입할 수 있습니다.'
    }
  },
  JsStaticHook: {
    name: { en: 'Event Hook Usage', ko: '이벤트 후킹 사용' },
    description: {
      en: 'Detects misuse of JavaScript event listeners.',
      ko: '이벤트 리스너의 악용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Event listeners like `onClick` or `onSubmit` can be abused to intercept user actions. This module checks if scripts misuse event hooks to redirect or collect input data.',
      ko: '`onClick`, `onSubmit` 등의 이벤트 리스너가 입력 탈취나 리디렉션에 악용되는지 검사합니다.'
    }
  },
  JsStaticObfuscate: {
    name: { en: 'Code Obfuscation Usage', ko: '코드 난독화 사용' },
    description: {
      en: 'Detects obfuscated or encoded JavaScript code.',
      ko: '난독화되거나 인코딩된 자바스크립트 코드 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Obfuscated JavaScript hides malicious intent by encoding logic in unreadable forms. This module detects patterns like `eval`, `atob`, or hexadecimal/Unicode string composition.',
      ko: '난독화 코드는 악의적 로직을 숨기기 위해 사용되며, 분석을 어렵게 만듭니다.'
    }
  },
  JsStaticRedirect: {
    name: { en: 'Static Redirect Usage', ko: '정적 리디렉션 사용' },
    description: {
      en: 'Detects hardcoded redirection logic.',
      ko: '하드코딩된 리디렉션 코드 사용 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Hardcoded redirects using `window.location` or `meta-refresh` scripts can auto-redirect users without interaction. This module scans for such static redirect logic',
      ko: '`window.location` 등을 통한 자동 이동 코드를 탐지합니다.'
    }
  },
  JsStaticScript: {
    name: { en: 'Script Tag Usage', ko: 'Script 태그 사용' },
    description: {
      en: 'Detects suspicious usage of script tags.',
      ko: 'script 태그 내 악성 코드 삽입 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'This module analyzes the usage of `<script>` tags, especially inline ones, to detect embedded malicious payloads or unauthorized logic directly injected into the page.',
      ko: '`<script>` 태그의 사용 방식(인라인 여부, 외부 로딩 등)을 분석하여 위협을 평가합니다.'
    }
  },

  // JS dynamic 모듈
  JsDynamicDom: {
    name: { en: 'DOM Manipulation Usage', ko: 'DOM 조작 사용' },
    description: {
      en: 'Detects live DOM changes using JavaScript.',
      ko: '실행 중 DOM 변경이 일어나는지 탐지합니다.'
    },
    longDescription: {
      en: 'Phishing pages may dynamically create or modify DOM elements to avoid static detection. This module observes live DOM changes that are abnormal or deceptive..',
      ko: '피싱 사이트는 DOM을 동적으로 생성하거나 조작하여 정적 탐지를 회피할 수 있습니다.'
    }
  },
  JsDynamicExternal: {
    name: { en: 'Script Injection Usage', ko: '스크립트 동적 삽입' },
    description: {
      en: 'Detects dynamically injected scripts at runtime.',
      ko: '실행 중 삽입되는 스크립트를 탐지합니다.'
    },
    longDescription: {
      en: 'JavaScript code that injects `<script>` tags or uses functions like `eval`, `Function()`, or `document.write` dynamically can introduce runtime payloads. This module flags such behaviors.',
      ko: '스크립트 태그를 동적으로 삽입하거나 `eval`, `document.write` 등을 사용하는 경우 탐지합니다.'
    }
  },
  JsDynamicHook: {
    name: { en: 'Event Hook Usage', ko: '동적 이벤트 후킹' },
    description: {
      en: 'Detects dynamic registration of event handlers.',
      ko: '실행 중 등록된 이벤트 핸들러를 탐지합니다.'
    },
    longDescription: {
      en: 'Event listeners registered at runtime (e.g., `addEventListener`) may be used to steal input or alter user experience. This module tracks event hook usage during page interaction.',
      ko: '실행 중 `addEventListener` 등을 통해 등록되는 후킹 시도를 감지합니다.'
    }
  },
  JsDynamicObfuscate: {
    name: { en: 'Code Obfuscation Usage', ko: '실행 중 코드 난독화' },
    description: {
      en: 'Detects runtime code obfuscation in JavaScript.',
      ko: 'JavaScript가 실행 중 스스로 난독화되는지 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'Runtime obfuscation makes code harder to analyze by dynamically generating functions or re-encoding logic. This module watches for suspicious transformations after the page loads.',
      ko: '코드를 실행 중 변형하여 분석을 어렵게 만드는 기법을 탐지합니다.'
    }
  },
  JsDynamicRedirect: {
    name: { en: 'Redirect Usage', ko: '실행 중 리디렉션' },
    description: {
      en: 'Detects JavaScript-based URL redirection.',
      ko: 'JavaScript로 수행되는 리디렉션 여부를 탐지합니다.'
    },
    longDescription: {
      en: 'JavaScript can redirect users post-load via `window.location` or similar methods. Phishers use this to delay redirect until after AI or scanners finish analysis. This module flags such logic.',
      ko: '피싱 공격자는 페이지 로드 이후에 자동 이동을 수행하는 방식으로 탐지를 회피하려고 합니다.'
    }
  }
};

