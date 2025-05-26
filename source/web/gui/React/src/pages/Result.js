import React, { useState } from 'react';
import '../styles/Result.css';
import UrlInputBox from '../components/UrlInputBox';
import GaugeScore from '../components/GaugeScore';
import logoImage from '../components/logo_header.png';
import GitImage from '../components/github.png';

function Result() {
    // 현재 활성화된 탭 상태를 저장 ('detection' 또는 'details')
    const [activeTab, setActiveTab] = useState('detection');

    // 모듈 카드 목록을 렌더링하는 함수
    // type: 모듈 종류 (예: URL, HTML, JS_Static 등)
    // count: 렌더링할 모듈 수
    const renderModules = (type, count) => {
        const modules = [];
        for (let i = 1; i <= count; i++) {
            const isDetected = Math.random() < 0.3;
            // 모듈 하나의 카드 JSX 생성
            modules.push(
                <div key={`${type}-${i}`} className={`module-card ${isDetected ? 'detected' : 'safe'}`}>
                    {/* 모듈 이름 */}
                    <div className="module-title">{`${type} Module ${i}`}</div>
                    {/* 탐지 여부에 따라 출력 */}
                    <div className="module-status">
                        {isDetected ? <><span className="detected-text">Detected</span></> : <><span className="safe-text">Safe</span></>}
                    </div>
                </div>
            );
        }
        return modules;
    };

    return (
        <div className="result-background">
            {/* 전체 상단 헤더 */}
            <header className="result-header">
                <img src={logoImage} alt="Logo" className="logo-image" />
                <div className="nav-buttons">
                    <button className="btn white">Search</button>
                    <button className="btn white">About</button>
                    <a
                        className="github-link"
                        href="https://github.com"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <img src={GitImage} alt="GitHub" className="github-icon" />
                    </a>
                </div>
            </header>

            {/* 메인 콘텐츠 컨테이너 */}
            <main className="result-container">
                <div className="result-box">
                    {/* 입력된 URL 표시 */}
                    <div className="url-section">
                        <span className="url-text">https://github.com/reeeue/PROJECT</span>
                    </div>

                    {/* 게이지 점수 컴포넌트 */}
                    <GaugeScore score={78} />

                    {/* 모듈 감지 요약 */}
                    <p className="detection-text">
                        <span className="red">5</span> out of the 23 modules reported suspected phishing detection.
                    </p>

                    {/* 탭 헤더 */}
                    <div className="tabs-header">
                        <button
                            className={`tab-button ${activeTab === 'detection' ? 'active' : ''}`}
                            onClick={() => setActiveTab('detection')}
                        >
                            DETECTION
                        </button>
                        <button
                            className={`tab-button ${activeTab === 'details' ? 'active' : ''}`}
                            onClick={() => setActiveTab('details')}
                        >
                            DETAILS
                        </button>
                    </div>

                    {/* 탭 본문 내용 */}
                    <div className="tab-content">
                        {activeTab === 'detection' && (
                            <div>
                                {/* 각 카테고리별 모듈 리스트 */}
                                <h4>URL</h4>
                                <div className="module-grid">
                                    {renderModules('URL', 6)}
                                </div>

                                <h4>HTML</h4>
                                <div className="module-grid">
                                    {renderModules('HTML', 7)}
                                </div>

                                <h4>JS_Static</h4>
                                <div className="module-grid">
                                    {renderModules('JS_Static', 5)}
                                </div>

                                <h4>JS_Dynamic</h4>
                                <div className="module-grid">
                                    {renderModules('JS_Dynamic', 5)}
                                </div>
                            </div>
                        )}
                        {activeTab === 'details' && (
                            <div>
                                <h4>Feature Details</h4>
                                <p>...여기에 상세 정보가 들어갑니다.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>

            {/* 하단 푸터 */}
            <footer className="result-footer">
                © 2025 wave to www. All rights reserved.
            </footer>
        </div>
    );
}

export default Result;
