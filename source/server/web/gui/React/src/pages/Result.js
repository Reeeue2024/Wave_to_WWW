import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import '../styles/Result.css';
import GaugeScore from '../components/GaugeScore';
import logoImage from '../components/logo_header.png';
import GitImage from '../components/github.png';

function Result() {
  const location = useLocation();
  const resultData = location.state;

  const [activeTab, setActiveTab] = useState('detection');

  if (!resultData) {
    return <div>결과 데이터가 없습니다. 홈에서 다시 시도해주세요.</div>;
  }

  const { summary, modules } = resultData;

  const renderModules = (mods) => {
    return mods.map((mod, index) => (
      <div key={index} className={`module-card ${mod.moduleResultFlag ? 'detected' : 'safe'}`}>
        <div className="module-title">{mod.moduleName}</div>
        <div className="module-status">
          {mod.moduleResultFlag ? (
            <span className="detected-text">Detected</span>
          ) : (
            <span className="safe-text">Safe</span>
          )}
        </div>
      </div>
    ));
  };

  return (
    <div className="result-background">
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

      <main className="result-container">
        <div className="result-box">
          <div className="url-section">
            <span className="url-text">{summary.inputUrl}</span>
          </div>

          <GaugeScore score={summary.resultScore} />

          <div className="final-flag">
            <p className="final-flag-text">
              <strong>최종 피싱 여부:</strong>{' '}
              {summary.resultFlag ? (
                <span className="detected-text">피싱 사이트 ❌</span>
              ) : (
                <span className="safe-text">정상 ✅</span>
              )}
            </p>
          </div>

          <p className="detection-text">
            {modules.filter(mod => mod.moduleResultFlag).length} out of the {modules.length} modules reported suspected phishing detection.
          </p>

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

          <div className="tab-content">
            {activeTab === 'detection' && (
              <div className="module-grid">{renderModules(modules)}</div>
            )}
            {activeTab === 'details' && (
  <div className="details-section">
    {modules.map((mod, index) => (
      <div key={index} className="module-detail-card">
        <h4>{mod.moduleName}</h4>
        <p><strong>✅ 실행 여부:</strong> {mod.moduleRun ? '성공' : '실패'}</p>
        <p><strong>🎯 점수:</strong> {mod.moduleScore} / {mod.moduleWeight}</p>
        <p><strong>🚨 탐지 여부:</strong> {mod.moduleResultFlag ? '탐지됨 ❌' : '안전 ✅'}</p>

        <p><strong>📝 탐지 이유:</strong> {mod.reason || '정보 없음'}</p>

        {mod.reasonData && mod.reasonData.length > 0 ? (
          <div>
            <strong>🔗 관련 데이터:</strong>
            <ul>
              {mod.reasonData.map((item, i) => (
                <li key={i}>
                  <a href={item} target="_blank" rel="noopener noreferrer">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p>관련 데이터 없음</p>
        )}

        <hr />
      </div>
    ))}
  </div>
)}

          </div>
        </div>
      </main>

      <footer className="result-footer">
        © 2025 wave to www. All rights reserved.
      </footer>
    </div>
  );
}

export default Result;
