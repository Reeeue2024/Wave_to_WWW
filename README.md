<pre> <code>
/root/source
│
├── web/                                # Web 관련 Code
│   ├── gui/                            # Web - Front-End : React JS
│   └── lib/                            # 관련 Library
│
├── chrome_extension/                   # Chrome Extension 관련 Code
│   ├── gui/                            # Chrome Extension - Front-End : Vanilla JS
│   └── lib/                            # 관련 Library
│
├── server/                             # Server - Back-End : FAST API
│   ├── app/                            # App
│   ├── sessions/                       # Sessions
│   └── api/                            # API
│
├── core_engine/                        # Core Engine
│   ├── fast_engine/                    # Fast Scan Engine : 관련 Plug-In 실행
│   ├── full_engine/                    # Full Scan Engine : 관련 Plug-In 실행
│   └── plugins/                        # Plug-In Modules
│       ├── url_modules/                # Phsihng Web Site의 "URL 관련 특징"을 바탕으로 Scan
│       ├── html_modules/               # Phsihng Web Site의 "HTML 관련 특징"을 바탕으로 Scan
│       ├── js_modules/                 # Phsihng Web Site의 "JS 관련 특징"을 바탕으로 Scan
│       └── etc_modules/                # Phsihng Web Site의 "그 외의 특징"을 바탕으로 Scan
│
├── db/                                 # DB
│   ├── sql_db/                         # SQL DB ( MySQL )
│   └── n_sql_db/                       # N SQL DB ( MongoDB )
│
├── configs/                            # ( 설정 관련 )
│
└── scripts/                            # Scripts
</code> </pre>
