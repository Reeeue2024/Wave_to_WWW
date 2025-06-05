// src/components/ResultUrlBox.js
// 결과 화면에서 사용자가 입력한 URL을 시각적으로 표시하는 컴포넌트를 정의

import React from 'react';
import './UrlInputBox.css'; 
import searchIcon from '../assets/img/search_icon.png'; 

// 결과 화면에서 URL을 보여주는 컴포넌트
function ResultUrlBox({ inputUrl, isPhishing }) {
  return (
    <div
      // 피싱 여부에 따라 테두리 색상(glow) 적용
      className={`url-input-wrapper result-mode ${
        isPhishing ? 'danger-glow' : 'safe-glow'
      }`}
      // 상하 마진 조정
      style={{ marginTop: '-35px', marginBottom: '30px' }}
    >
      <div
        className="url-input-box"
        style={{ pointerEvents: 'none' }} // 입력창 클릭/수정 불가하게 설정
      >
        {/* 검색 아이콘 */}
        <img src={searchIcon} alt="Search" className="search-icon" />
        {/* 분석된 URL 출력 (읽기 전용) */}
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
