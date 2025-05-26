import React from 'react';
import '../styles/Home.css';
import UrlInputBox from '../components/UrlInputBox';
import logoImage from '../components/logo_header.png';
import GitImage from '../components/github.png';

function Home() {
  return (
    <div className="home-wrapper">
      {/* 헤더 */}
      <header className="home-header">
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

      {/* 메인 콘텐츠 컨테이너 (배경 이미지 포함) */}
      <main className="home-background">
        {/* 배경 이미지 */}
        <img
          src={`${process.env.PUBLIC_URL}/Ellipse33.png`}
          alt="Decorative floating shape top-right"
          className="moving-image top-right"
        />
        <img
          src={`${process.env.PUBLIC_URL}/Ellipse34.png`}
          alt="Decorative floating shape bottom-left"
          className="moving-image bottom-left"
        />

        <div className="center-content">
          {/* 타이틀 로고 섹션 */}
          <div className="logo-section">
            <div className="title-logo-row">
              <img
                src={`${process.env.PUBLIC_URL}/wave_to.png`}
                alt="wave to"
                className="title_wave_to"
              />
              <img
                src={`${process.env.PUBLIC_URL}/www.png`}
                alt="www"
                className="title_www"
              />
            </div>

            {/* 데코 애셋 섹션 */}
            <div className="logo-decoration-layer">
              <img src="/fish1.png" alt="fish1" className="decor fish1" />
              <img src="/sparkle.png" alt="sparkle" className="decor sparkle1" />
              <img src="/fish2.png" alt="fish2" className="decor fish2" />
              <img src="/sparkle.png" alt="sparkle" className="decor sparkle2" />
              <img src="/fish1.png" alt="fish3" className="decor fish3" />
            </div>
          </div>

          {/* 입력창 섹션 */}
          <div className="input-section">
            <UrlInputBox />
          </div>
        </div>
      </main>

      {/* 푸터 */}
      <footer className="home-footer">
        © 2025 wave to www. All rights reserved.
      </footer>
    </div>
  );
}

export default Home;
