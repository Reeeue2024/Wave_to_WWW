// src/pages/Home.js

import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

import UrlInputBox from '../components/UrlInputBox';
import Header from '../components/Header';
import { getLang } from '../components/lang';

import logoHeader from '../assets/img/logo_header.png';
import logo from '../assets/img/logo.png';
import fish1 from '../assets/img/fish1.png';
import fish2 from '../assets/img/fish2.png';
import sparkle from '../assets/img/sparkle.png';

function Home() {
  const navigate = useNavigate();
  const lang = getLang();

  const [initialLoading, setInitialLoading] = useState(() => {
    return sessionStorage.getItem('waveFirstVisitShown') ? false : true;
  });
  const [fadeOutLoading, setFadeOutLoading] = useState(false);

  const snapRef = useRef(null);

  // 초기 로딩 애니메이션
  useEffect(() => {
    if (!initialLoading) return;
    const t1 = setTimeout(() => setFadeOutLoading(true), 1300);
    const t2 = setTimeout(() => {
      setInitialLoading(false);
      sessionStorage.setItem('waveFirstVisitShown', 'true');
    }, 1800);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [initialLoading]);

  // 헤더/푸터 높이를 CSS 변수로 반영 (슬라이드 높이 = 100dvh - header - footer)
  useEffect(() => {
    const setVars = () => {
      const header = document.querySelector('.home-header');
      const footer = document.querySelector('.home-footer');
      const hH = header ? header.offsetHeight : 0;
      const fH = footer ? footer.offsetHeight : 0;
      document.documentElement.style.setProperty('--header-h', `${hH}px`);
      document.documentElement.style.setProperty('--footer-h', `${fH}px`);
    };
    setVars();
    window.addEventListener('resize', setVars);
    // 이미지 로고 등 로드 후 다시 계산
    window.addEventListener('load', setVars);
    return () => {
      window.removeEventListener('resize', setVars);
      window.removeEventListener('load', setVars);
    };
  }, []);

  // 키보드 ↑/↓ 로 슬라이드 전환 (옵션)
  useEffect(() => {
    const handler = (e) => {
      const container = snapRef.current;
      if (!container) return;
      const slides = Array.from(container.querySelectorAll('.slide'));
      const top = container.scrollTop;
      const vh = container.clientHeight;
      const idx = Math.round(top / vh);

      if (e.key === 'ArrowDown' || e.key === 'PageDown') {
        const next = slides[Math.min(idx + 1, slides.length - 1)];
        next?.scrollIntoView({ behavior: 'smooth' });
      }
      if (e.key === 'ArrowUp' || e.key === 'PageUp') {
        const prev = slides[Math.max(idx - 1, 0)];
        prev?.scrollIntoView({ behavior: 'smooth' });
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const goNext = () => {
    const container = snapRef.current;
    if (!container) return;
    const slides = container.querySelectorAll('.slide');
    slides[1]?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      {/* 초기 로딩 */}
      {initialLoading ? (
        <div className={`wave-loader ${fadeOutLoading ? 'fade-out' : ''}`}>
          <div className="full-screen-wave" />
          <img src={logoHeader} alt="logo" className="loader-logo" />
        </div>
      ) : (
        <div className="home-wrapper fade-in">
          {/* 고정 헤더 */}
          <Header />

          {/* '푸터 위'에서만 슬라이드처럼 움직이는 영역 */}
          <div className="snap-container" ref={snapRef}>
            {/* 슬라이드 1: 메인 */}
            <section className="slide hero">
              <main className="home-background">
                <div className="blob blob-top-right"></div>
                <div className="blob blob-bottom-left"></div>

                <div className="center-content">
                  <div className="logo-container">
                    <div className="logo-decoration-layer">
                      <img src={fish1} alt="fish1" className="decor fish1" />
                      <img src={sparkle} alt="sparkle" className="decor sparkle1" />
                      <img src={fish2} alt="fish2" className="decor fish2" />
                      <img src={fish1} alt="fish3" className="decor fish3" />
                      <img src={sparkle} alt="sparkle" className="decor sparkle2" />
                    </div>
                    <img src={logo} alt="main-logo" className="main-logo" />
                  </div>

                  <div className="input-section">
                    <UrlInputBox />
                  </div>

                  {/* 스크롤 유도 */}
                  <button className="scroll-hint" onClick={goNext} aria-label="Next section">
                    <span className="scroll-hint-text">
                      {lang === 'ko' ? '이 사이트는 무엇을 하나요?' : 'What does this site do?'}
                    </span>
                    <span className="chevron">⌄</span>
                  </button>
                </div>
              </main>
            </section>

            {/* 슬라이드 2: 소개 섹션 */}
            <section className="slide about-slide">
              <div className="about-inner single-slide">

                <h2 className="about-title">
                  What does <img src={logo} alt="Wave to WWW" className="about-logo-inline" /> do?
                </h2>

                {/* 리드 */}
                <p className="about-lead">
                  {lang === 'ko'
                    ? 'wave to www는 단순한 안전/위험 판정에서 끝나지 않습니다. URL·HTML·JS에 대한 정적·동적 분석과 AI 모델을 결합해 피싱 위험을 정밀 탐지하고, 카드/차트로 “왜 위험한지”를 함께 설명합니다.'
                    : 'wave to www goes beyond a simple safe/detected verdict. It combines static & dynamic URL/HTML/JS analysis with an AI model, and explains “why” with visual cards and charts.'}
                </p>

                {/* 기능 카드 4개 */}
                <div className="feature-row">
                  <div className="feature-card">
                    <div className="feature-icon">📦</div>
                    <h3>{lang === 'ko' ? '모듈' : 'Modules'}</h3>
                    <p>
                      {lang === 'ko'
                        ? '주소(URL), 웹페이지 구조(HTML), 스크립트(JS)를 세밀하게 검사해 숨은 위험까지 찾아냅니다.'
                        : 'Thoroughly checks the URL, page structure (HTML), and scripts (JS) to uncover hidden risks.'}
                    </p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon">🤖</div>
                    <h3>AI</h3>
                    <p>
                      {lang === 'ko'
                        ? '머신러닝 기반 AI가 수많은 피싱 패턴을 학습해, 사람 눈으로 놓치기 쉬운 위협도 탐지합니다.'
                        : 'AI trained on phishing patterns detects threats that are hard to notice with the human eye.'}
                    </p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon">⚡</div>
                    <h3>{lang === 'ko' ? '크롬 확장' : 'Chrome Extension'}</h3>
                    <p>
                      {lang === 'ko'
                        ? '웹서핑 중 마우스를 올리면 즉시 위험 여부를 알려주어 클릭 전에 막을 수 있습니다.'
                        : 'Shows instant alerts while browsing so you can avoid danger before clicking.'}
                    </p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon">🛡️</div>
                    <h3>KISA</h3>
                    <p>
                      {lang === 'ko'
                        ? '위험 사이트가 발견되면 한국인터넷진흥원(KISA)에 자동 신고되어 빠른 차단이 이뤄집니다.'
                        : 'Suspicious sites are auto-reported to KISA for quick blocking and protection.'}
                    </p>
                  </div>
                </div>

                {/* 작동 방식: 카드 트랙 */}
                <div className="howitworks-track">
                  <h4>{lang === 'ko' ? '어떻게 동작하나요?' : 'How does it work?'}</h4>

                  <div className="track-row">
                    {/* 01 */}
                    <div className="step-card">
                      <div className="step-head">
                        <span className="step-no">01</span>
                        <span className="step-underline" />
                      </div>
                      <p className="step-text">
                        {lang === 'ko'
                          ? 'URL 입력하거나\n링크에 마우스 올리기'
                          : 'Enter URL or\nhover over links'}
                      </p>
                    </div>

                    {/* 02 */}
                    <div className="step-card">
                      <div className="step-head">
                        <span className="step-no">02</span>
                        <span className="step-underline" />
                      </div>
                      <p className="step-text">
                        {lang === 'ko'
                          ? 'AI + 규칙 기반으로\n다중 모듈 분석'
                          : 'AI + rule-based\nmulti-module analysis'}
                      </p>
                    </div>

                    {/* 03 */}
                    <div className="step-card">
                      <div className="step-head">
                        <span className="step-no">03</span>
                        <span className="step-underline" />
                      </div>
                      <p className="step-text">
                        {lang === 'ko'
                          ? '탐지 결과와 근거를\n시각적으로 제공'
                          : 'Visual results with\nclear evidence'}
                      </p>
                    </div>

                    {/* 04 */}
                    <div className="step-card">
                      <div className="step-head">
                        <span className="step-no">04</span>
                        <span className="step-underline" />
                      </div>
                      <p className="step-text">
                        {lang === 'ko'
                          ? '피싱 사이트 발견 시\nKISA 자동 신고'
                          : 'Auto-report to KISA\nwhen phishing detected'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* CTA */}
                <div className="about-cta">
                  <button
                    className="btn cta"
                    onClick={() => snapRef.current?.scrollTo({ top: 0, behavior: 'smooth' })}
                  >
                    {lang === 'ko' ? 'URL 분석하기' : 'Analyze a URL'}
                  </button>
                </div>

              </div>
            </section>

          </div>

          {/* footer */}
          <footer className="home-footer">
            © 2025 wave to www. All rights reserved.
          </footer>
        </div>
      )}
    </>
  );
}

export default Home;
