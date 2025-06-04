// src/components/Header.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logoHeader from '../assets/img/logo_header.png';
import GitImage from '../assets/img/github.png';
import GmailImage from '../assets/img/gmail.png';
import ChromeExtensitonImage from '../assets/img/chrome_extension.png';

function Header({ onLogoClick }) {
  const navigate = useNavigate();

  const [showTooltip, setShowTooltip] = useState(false);
  const handleGmailClick = (e) => {
    e.preventDefault();
    setShowTooltip(true);
    setTimeout(() => setShowTooltip(false), 6000);
  };

  return (
    <header className="home-header">
      <img
        src={logoHeader}
        alt="Logo"
        className="logo-image"
        style={{ cursor: 'pointer' }}
        onClick={onLogoClick || (() => navigate('/'))}
      />
      <div className="nav-buttons">
        <button className="btn white">Search</button>
        <button className="btn white">About</button>

        <a
          href="https://chrome.google.com/webstore/detail/your-extension-id"
          className="chrome-icon-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src={ChromeExtensitonImage} alt="Chrome Extension" className="chrome-icon" />
        </a>

        <div className="tooltip-wrapper">
          <div
            className="gmail-icon-link"
            onClick={handleGmailClick}
            style={{ cursor: 'pointer' }}
          >
            <img src={GmailImage} alt="Gmail" className="gmail-icon" />
            {showTooltip && (
              <span className="tooltip-text">
                wavetowww@gmail.com<br />
                <span className="tooltip-sub">Reach out to wave to www</span>
              </span>
            )}
          </div>
        </div>

        <a
          className="github-link"
          href="https://github.com/Reeeue2024/PROJECT"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src={GitImage} alt="GitHub" className="github-icon" />
        </a>
      </div>
    </header>
  );
}

export default Header;
