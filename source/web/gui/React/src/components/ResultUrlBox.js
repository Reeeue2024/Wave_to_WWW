// src/components/ResultUrlBox.js

import React from 'react';
import './UrlInputBox.css'; 
import searchIcon from '../assets/img/search_icon.png';

function ResultUrlBox({ inputUrl, isPhishing }) {
  return (
    <div className={`url-input-wrapper ${isPhishing ? 'danger-glow' : 'safe-glow'}`}>
      <div className="url-input-box" style={{ pointerEvents: 'none' }}>
        <img src={searchIcon} alt="Search" className="search-icon" />
        <input
          type="text"
          className="url-input"
          value={inputUrl}
          readOnly
          style={{ fontWeight: 'bold' }}
        />
      </div>
    </div>
  );
}

export default ResultUrlBox;
