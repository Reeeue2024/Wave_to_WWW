// src/components/GaugeScore.js
// 피싱 탐지 점수를 게이지 형태로 시각화하는 컴포넌트를 정의

import React from 'react';
import GaugeChart from 'react-gauge-chart';
import './GaugeScore.css';

// 점수에 따른 게이지 시각화 컴포넌트
function GaugeScore({ score }) {
  const percent = score / 100;           
  const isPhishing = score >= 70;        // 70점 이상이면 피싱 탐지로 판단

  return (
    <div className={`gauge-wrapper ${isPhishing ? 'danger' : 'safe'}`}>
      {/* 게이지 차트 설정 */}
      <GaugeChart
        id="phishing-score-gauge"        
        nrOfLevels={20}                  // 게이지 눈금 레벨
        arcsLength={[0.7, 0.3]}          // 파란 영역(안전) 70%, 빨간 영역(위험) 30%
        colors={['#2185B7', '#B95250']}  // 안전(파랑), 위험(빨강)
        percent={percent}                // 현재 퍼센트 위치
        arcPadding={0.02}                // 색 영역 간 간격
        needleColor="#ffffff"            // 바늘 색상
        needleBaseColor="#ffffff"        // 바늘 베이스 색상
        textColor="transparent"          // 게이지 내 텍스트 숨김
      />
      <div className="gauge-score-text">
        {/* 점수 숫자 표시 (색상은 위험 여부에 따라 변경) */}
        <div className={`score-big ${isPhishing ? 'text-danger' : 'text-safe'}`}>{score}%</div>
        {/* 라벨 텍스트 */}
        <div className="score-label">Phishing Risk</div>
      </div>
    </div>
  );
}

export default GaugeScore; 