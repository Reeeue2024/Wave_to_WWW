// src/pages/Result.js
// 피싱 탐지 결과 페이지

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/Result.css';

import GaugeScore from '../components/GaugeScore';
import WaveLoader from '../components/WaveLoader';
import ResultUrlBox from '../components/ResultUrlBox';

import Header from '../components/Header';


// 카테고리 및 모듈 설명 맵
import { categoryMap, categoryDescriptions, moduleDescriptions } from '../components/descriptions';

function Result() {
  const location = useLocation(); // 이전 페이지에서 받은 state 접근
  const navigate = useNavigate(); // 페이지 이동용
  const resultData = location.state; // 전달받은 결과 데이터
  const [activeTab, setActiveTab] = useState('detection'); // 탭 상태
  const [loading, setLoading] = useState(true); // 로딩 상태
  const userInputUrl = resultData?.inputUrl;
  const [showTooltip, setShowTooltip] = useState(false)

  // 로딩 화면 2초 후 제거
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleGmailClick = (e) => {
    e.preventDefault();
    setShowTooltip(true);
    setTimeout(() => setShowTooltip(false), 6000);
  };

  // resultData가 없을 경우 에러 처리
  if (!resultData) {
    return <div>Result data not found. Please try again from the home page.</div>;
  }

  const { summary, modules } = resultData;
  const phishingCount = modules.filter(mod => mod.moduleResultFlag).length;
  const totalCount = modules.length;


  // 모듈 이름 접두사 기준으로 카테고리 분류
  const inferCategory = (name) => {
    for (const prefix in categoryMap) {
      if (name.startsWith(prefix)) return categoryMap[prefix];
    }
    return 'Other';
  };

  // 카테고리별로 모듈 정리
  const categories = Object.values(categoryMap);
  const categorizedModules = {};
  categories.forEach((cat) => (categorizedModules[cat] = []));
  modules.forEach((mod) => {
    const category = inferCategory(mod.moduleName);
    if (categorizedModules[category]) {
      categorizedModules[category].push(mod);
    }
  });

  // DETECTION 탭용 모듈 카드 렌더링
  const renderModules = (mods) => mods.map((mod, index) => {
    const info = moduleDescriptions[mod.moduleName] || {
      name: mod.moduleName.replace(/^(Ai|Url|Html|JsStatic|JsDynamic)/, ''),
      description: 'No description available.'
    };

    return (
      <div
        key={index}
        className={`module-card ${mod.moduleResultFlag ? 'detected' : 'safe'}`}
        onClick={() => {
          setActiveTab('details'); // 클릭 시 DETAILS 탭으로 전환
          setTimeout(() => {
            const target = document.getElementById(`detail-${mod.moduleName}`);
            if (target) {
              target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }, 100);
        }}
      >
        <div className="module-title">{info.name}</div>
        <div className="module-description">{info.description}</div>
        <div className="module-status">
          {mod.moduleResultFlag
            ? <span className="detected-text-card">Detected</span>
            : <span className="safe-text-card">Safe</span>}
        </div>
      </div>
    );
  });

  // reason 및 관련 링크 렌더링
  const renderReasonsWithData = (reason, data) => {
    // case 1: reason, data 모두 배열
    if (Array.isArray(reason) && Array.isArray(data)) {
      const filtered = reason
        .map((r, i) => {
          const text = typeof r === 'string' ? r.trim() : '';
          const href = typeof data[i] === 'string' ? data[i].trim() : '';
          if (!text && !href) return null;
          return { text, href };
        })
        .filter(item => item !== null);

      if (filtered.length === 0) return null;

      return (
        <ul className="reason-list">
          {filtered.map((item, i) => (
            <li key={i}>
              {item.text && <strong>{item.text}</strong>}
              {item.href && (
                <div>
                  <a href={item.href} target="_blank" rel="noopener noreferrer">
                    {item.href}
                  </a>
                </div>
              )}
            </li>
          ))}
        </ul>
      );
    }

    // case 2: reason이 문자열일 때
    if (typeof reason === 'string') {
      const reasons = reason
        .split('.')
        .map(r => r.trim())
        .filter(r => r !== '');

      const filtered = reasons.map((r, i) => {
        const href = typeof data?.[i] === 'string' ? data[i].trim() : '';
        return { text: r, href };
      });

      if (filtered.length === 0) return null;

      return (
        <ul className="reason-list">
          {filtered.map((item, i) => (
            <li key={i}>
              {item.text && <strong>{item.text}</strong>}
              {item.href && (
                <div>
                  <a href={item.href} target="_blank" rel="noopener noreferrer">
                    {item.href}
                  </a>
                </div>
              )}
            </li>
          ))}
        </ul>
      );
    }

    // case 3: data만 배열일 때
    if (Array.isArray(data)) {
      const validLinks = data
        .filter(d => typeof d === 'string' && d.trim() !== '');

      if (validLinks.length === 0) return null;

      return (
        <ul className="reason-list">
          {validLinks.map((d, i) => (
            <li key={i}>
              <a href={d} target="_blank" rel="noopener noreferrer">
                {d}
              </a>
            </li>
          ))}
        </ul>
      );
    }

    return <p>No reason provided.</p>;
  };



  // DETAILS 탭용 상세 모듈 설명 렌더링
  const renderDetails = (mods) => mods.map((mod, index) => {
    const info = moduleDescriptions[mod.moduleName] || {
      name: mod.moduleName.replace(/^(Ai|Url|Html|JsStatic|JsDynamic)/, ''),
      description: 'No description available.',
      longDescription: 'No detailed description available.'
    };

    return (
      <div
        key={index}
        id={`detail-${mod.moduleName}`} // 클릭 시 이동할 위치용 ID
        className={`module-detail-card ${mod.moduleResultFlag ? 'detected' : 'safe'}`}
      >
        <h4>{info.name}</h4>
        <p>{info.longDescription || info.description}</p>
        <p className={mod.moduleResultFlag ? 'detected-text-card' : 'safe-text-card'}>
          {mod.moduleResultFlag ? 'Detected' : 'Safe'}
        </p>
        <p><strong>Execution:</strong> {mod.moduleRun ? 'Success' : 'Fail'}</p>
        <p><strong>Score:</strong> {mod.moduleScore} / {mod.moduleWeight}</p>
        <div><strong>Reason:</strong></div>
        {renderReasonsWithData(mod.reason, mod.reasonData)}
        <hr />
      </div>
    );
  });

  // 로딩 중일 경우 로더 표시
  if (loading) return <WaveLoader url={userInputUrl} />;

  // 결과 페이지 전체 렌더링
  return (

    <div className="result-background">
      <Header />
      {/* 본문 결과 영역 */}
      <main className="result-container">
        {/* 배경 블롭 */}
        <div className="blob blob1"></div>
        <div className="blob blob2"></div>
        <div className="blob blob3"></div>
        <div className="blob blob4"></div>

        {/* 결과 박스 */}
        <div className={`result-box ${summary.resultFlag ? 'detected' : 'safe'}`}>
          {/* URL 정보와 게이지 점수 표시 */}
          <ResultUrlBox inputUrl={summary.inputUrl} isPhishing={summary.resultFlag} />
          <GaugeScore score={summary.resultScore} isPhishing={summary.resultFlag} />

          {/* 최종 판단 표시 */}
          <div className="final-flag">
            {summary.reportedToKisa && (                                                    //이 부분이 키사 보고 문장 추가한 부분입니다.
            <p className="kisa-report-text">📤 해당 URL은 키사(KISA)에 보고되었습니다.</p>
            )}
            <p className="final-flag-text">
              {summary.resultFlag
                ? <span className="detected-text">Phishing</span>
                : <span className="safe-text">Safe</span>}
            </p>
          </div>

          {/* 탐지 모듈 통계 */}
          <p className={`detection-text ${summary.resultFlag ? 'red' : 'blue'}`}>
            <span className={summary.resultFlag ? 'detected-number' : 'safe-number'}>
              {phishingCount}
            </span> out of the <span className="safe-number">{totalCount}</span> modules reported suspected phishing detection.
          </p>

          {/* 탭 전환 버튼 */}
          <div className="tabs-header">
            <button className={`tab-button ${activeTab === 'detection' ? 'active' : ''}`} onClick={() => setActiveTab('detection')}>
              DETECTION
            </button>
            <button className={`tab-button ${activeTab === 'details' ? 'active' : ''}`} onClick={() => setActiveTab('details')}>
              DETAILS
            </button>
          </div>

          {/* 탭별 콘텐츠 표시 */}
          <div className="tab-content">
            {categories.map((category) => (
              <div key={category} className="category-section">
                <h3 className="category-title">{category}</h3>
                {activeTab === 'details' && (
                  <p className="category-description">
                    {categoryDescriptions[Object.keys(categoryMap).find(key => categoryMap[key] === category)]}
                  </p>
                )}
                <div className={activeTab === 'detection' ? 'module-grid' : 'details-section'}>
                  {activeTab === 'detection'
                    ? renderModules(categorizedModules[category])
                    : renderDetails(categorizedModules[category])}
                </div>
              </div>
            ))}
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
