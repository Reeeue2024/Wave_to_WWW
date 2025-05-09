import React from 'react';
import './UrlInputBox.css'; // 별도 스타일 원할 경우

function UrlInputBox() {
  return (
    <div className="url-input-box">
      <span className="search-icon">🔍</span>
      <input
        type="text"
        placeholder="URL을 입력해주세요."
        className="url-input"
      />
    </div>
  );
}

export default UrlInputBox;
