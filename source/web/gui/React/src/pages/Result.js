// src/pages/Result.js
// 피싱 탐지 결과 페이지

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/Result.css';

import GaugeScore from '../components/GaugeScore';
import WaveLoader from '../components/WaveLoader';
import ResultUrlBox from '../components/ResultUrlBox';
import UrlInputBox from '../components/UrlInputBox';
import FriendlyExplain from '../components/FriendlyExplain';

import Header from '../components/Header';

import KisaImage from '../assets/img/kisa.png';

import SummaryCards from '../components/SummaryCards';

// 언어 변환
import { getLang } from '../components/lang';
import { texts } from '../components/texts';

// 카테고리 및 모듈 설명 맵
import { categoryMap, categoryDescriptions, moduleDescriptions } from '../components/descriptions';


function Result() {
  const lang = getLang(); // 현재 언어: 'en' 또는 'ko'

  const location = useLocation(); // 이전 페이지에서 받은 state 접근
  const navigate = useNavigate(); // 페이지 이동용
  const resultData = location.state; // 전달받은 결과 데이터
  const [activeTab, setActiveTab] = useState('detection'); // 탭 상태
  const [loading, setLoading] = useState(true); // 로딩 상태
  const userInputUrl = resultData?.inputUrl;
  const [showTooltip, setShowTooltip] = useState(false)
  const [editingUrl, setEditingUrl] = useState(false);

  // 로딩 화면 2초 후 제거
  useEffect(() => {
    const fromLangSwitch = sessionStorage.getItem('langSwitch');

    if (fromLangSwitch) {
      setLoading(false);
      sessionStorage.removeItem('langSwitch');
    } else {
      const timer = setTimeout(() => setLoading(false), 2000);
      return () => clearTimeout(timer);
    }
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

  const isPhishing = summary.resultScore >= 70;

  const phishingCount = modules.filter(mod => mod.moduleResultFlag).length;
  const totalCount = modules.length;

  const aiModule = modules.find((mod) => mod.moduleName === 'Ai');
  const aiScore = aiModule?.reason?.match(/[\d.]+/)?.[0] ?? null;
  const topReason = aiModule?.reason || modules.find(m => m.moduleResultFlag)?.reason;
  const detectedModules = modules
    .filter((mod) => mod.moduleResultFlag)
    .map((mod) => mod.moduleName); // 또는 moduleDescriptions[mod.moduleName]?.name[lang] 도 가능

  // 모듈 이름 접두사 기준으로 카테고리 분류
  const inferCategoryKey = (name) => {
    for (const prefix in categoryMap) {
      if (name.startsWith(prefix)) return prefix;
    }
    return 'Other';
  };

  // 카테고리별로 모듈 정리
  const categoryKeys = Object.keys(categoryMap);
  const categorizedModules = {};
  categoryKeys.forEach((key) => (categorizedModules[key] = []));
  modules.forEach((mod) => {
    const categoryKey = inferCategoryKey(mod.moduleName);
    if (categorizedModules[categoryKey]) {
      categorizedModules[categoryKey].push(mod);
    }
  });

  // DETECTION 탭용 모듈 카드 렌더링
  const renderModules = (mods) => mods.map((mod, index) => {
    const info = moduleDescriptions[mod.moduleName] || {
      name: { en: mod.moduleName, ko: mod.moduleName },
      description: { en: 'No description available.', ko: '설명이 없습니다.' },
    };

    return (
      <div
        key={index}
        className={`module-card ${mod.moduleResultFlag ? 'detected' : 'safe'}`}
        onClick={() => {
          setActiveTab('details');
          setTimeout(() => {
            const target = document.getElementById(`detail-${mod.moduleName}`);
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 100);
        }}
      >
        <div className="module-title">{info.name[lang]}</div>
        <div className="module-description">{info.description[lang]}</div>
        <div className="module-status">
          {mod.moduleResultFlag
            ? <span className="detected-text-card">{texts[lang].detected}</span>
            : <span className="safe-text-card">{texts[lang].safe}</span>}
        </div>
      </div>
    );
  });

  // reason 및 관련 링크 렌더링
  const renderReasonsWithData = (reason, data, moduleName) => {
    //moduleName을 추가하여 AI일 경우에는 reason만 하나의 문장으로 출력하도록 하였습니다.
    if (moduleName === 'Ai') {
      return (
        <ul className="reason-list">
          <li><strong>{reason}</strong></li>
        </ul>
      );
    }
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
        .split('/(?<=[.!?])\s+/g') //.단위로 쪼개게 되어서 30.80%가 split 되었던 거라서 문장 단위로 쪼개도록 split 하였습니다.
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
      name: { en: mod.moduleName, ko: mod.moduleName },
      description: { en: 'No description.', ko: '설명이 없습니다.' },
      longDescription: { en: 'No detailed description.', ko: '상세 설명이 없습니다.' },
    };

    const isAiModule = mod.moduleName === 'Ai';

    let aiProb = 0;
    if (isAiModule && typeof mod.reason === 'string') {
      const match = mod.reason.match(/[\d.]+/);
      aiProb = match ? parseFloat(match[0]) : 0;
    }

    return (
      <div
        key={index}
        id={`detail-${mod.moduleName}`}
        className={`module-detail-card ${mod.moduleResultFlag ? 'detected' : 'safe'}`}
      >
        <p className="module-detail-title">{info.name[lang]}</p>
        <p>{info.longDescription[lang] || info.description[lang]}</p>
        <p className={mod.moduleResultFlag ? 'detected-text-card' : 'safe-text-card'}>
          {mod.moduleResultFlag ? texts[lang].detected : texts[lang].safe}
        </p>
        <p><strong>Execution:</strong> {mod.moduleRun ? 'Success' : 'Fail'}</p>

        {!isAiModule && (
          <>
            <p><strong>Score:</strong> {mod.moduleScore} / {mod.moduleWeight}</p>
            <div><strong>Reason:</strong></div>
            {renderReasonsWithData(mod.reason, mod.reasonData, mod.moduleName)}
          </>
        )}

        {/* AI 모듈일 경우 확률 막대 그래프 표시 */}
        {isAiModule && (
          <div className="ai-bar-wrapper">
            <div className="ai-bar-label-emph">{aiProb.toFixed(2)}%</div>
            <div className="ai-bar">
              <div
                className="ai-bar-fill"
                style={{
                  width: `${aiProb}%`,
                  backgroundColor: aiProb >= 70 ? '#B95250' : '#2185B7'
                }}
              />
            </div>
          </div>
        )}
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
        <div className={`result-box ${isPhishing ? 'detected' : 'safe'}`}>
          {/* URL 정보와 게이지 점수 표시 */}
          <div className="input-section2">
            {editingUrl ? (
              <UrlInputBox />
            ) : (
              <div onClick={() => setEditingUrl(true)} style={{ cursor: 'pointer' }}>
                <ResultUrlBox inputUrl={summary.inputUrl} isPhishing={isPhishing} />
              </div>
            )}
          </div>

          <GaugeScore score={summary.resultScore} isPhishing={isPhishing} />

          {/* 최종 판단 표시 */}
          <div className="final-flag">
            <p className="final-flag-text">
              {isPhishing
                ? <span className="detected-text">{texts[lang].detected}</span>
                : <span className="safe-text">{texts[lang].safe}</span>}
            </p>
          </div>

          {/* 키사 신고 여부 */}
          <div className='Kisa'>
            {isPhishing && summary.reportedToKisa && (
              <p className="kisa-report-text">The URL has been reported to <img src={KisaImage} className="kisa-icon" /></p>
            )}
          </div>

          {/* 결과 요약 카드 추가 위치 */}
          <SummaryCards
            phishingCount={phishingCount}
            totalCount={totalCount}
            aiScore={parseFloat(aiScore)}
            topReason={typeof topReason === 'string' ? topReason.slice(0, 100) : 'N/A'}
            isReported={summary.reportedToKisa}
            detectedModules={detectedModules}
            summary={summary}
            modules={modules}
          />

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
            {categoryKeys.map((key) => (
              <div key={key} className="category-section">
                <h3 className="category-title">{categoryMap[key][lang]}</h3>
                {activeTab === 'details' && (
                  <p className="category-description">{categoryDescriptions[key][lang]}</p>
                )}
                <div className={activeTab === 'detection' ? 'module-grid' : 'details-section'}>
                  {activeTab === 'detection'
                    ? renderModules(categorizedModules[key])
                    : renderDetails(categorizedModules[key])}
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* 하단 푸터 */}
      < footer className="result-footer" >
        © 2025 wave to www.All rights reserved.
      </footer >
    </div >
  );
}

export default Result;