// src/pages/Home.js

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css'; // 스타일 시트

import UrlInputBox from '../components/UrlInputBox'; // URL 입력 컴포넌트
import Header from '../components/Header';

import logoHeader from '../assets/img/logo_header.png';
import logo from '../assets/img/logo.png';
import fish1 from '../assets/img/fish1.png';
import fish2 from '../assets/img/fish2.png';
import sparkle from '../assets/img/sparkle.png';

function Home() {
  const navigate = useNavigate(); // 페이지 이동을 위한 hook
  const [initialLoading, setInitialLoading] = useState(true);

  const [showTooltip, setShowTooltip] = useState(false)

  // 로딩 애니메이션 3초 후 종료
  useEffect(() => {
    const timer = setTimeout(() => setInitialLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handleGmailClick = (e) => {
    e.preventDefault();
    setShowTooltip(true);
    setTimeout(() => setShowTooltip(false), 6000);
  };

  return (
    <>
      {/* 초기 로딩 애니메이션 (3초) */}
      {initialLoading ? (
        <div className="wave-loader">
          <div className="full-screen-wave" />
          <img src={logoHeader} alt="logo" className="loader-logo" />
        </div>
      ) : (
        <div className="home-wrapper fade-in">
          <Header />
          {/* 본문 배경 영역 */}
          <main className="home-background">
            {/* 돌아다니는 blob 이펙트 */}
            <div className="blob blob-top-right"></div>
            <div className="blob blob-bottom-left"></div>

            {/* 중앙 콘텐츠: 로고 + 입력창 */}
            <div className="center-content">
              {/* 로고 및 장식 요소 */}
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

              {/* URL 입력 창 */}
              <div className="input-section">
                <UrlInputBox />
              </div>
            </div>
          </main>

          {/* 하단 푸터 */}
          <footer className="home-footer">
            © 2025 wave to www. All rights reserved.
          </footer>
        </div>
      )}
    </>
  );
}

export default Home;
