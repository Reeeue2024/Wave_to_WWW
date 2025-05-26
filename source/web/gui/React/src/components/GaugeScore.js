// src/components/GaugeScore.js

import React from 'react';
import GaugeChart from 'react-gauge-chart';

// 점수를 받아 시각화하는 게이지 컴포넌트
function GaugeScore({ score }) {
  const percent = score / 100;

  return (
    <div className="gauge-wrapper">
      <GaugeChart
        id="phishing-score-gauge"  // HTML 요소 id
        nrOfLevels={20}            // 눈금 분할 수
        arcsLength={[0.7, 0.3]}    // 색상 영역 비율 (예: 70% 안전, 30% 위험)
        colors={['#2185B7', '#B95250']}  // 안전(파랑), 위험(빨강)
        percent={percent}          // 게이지에 표시할 백분율
        arcPadding={0.02}          // 각 arc 간격
        needleColor="#ffffff"      // 바늘 색
        needleBaseColor="#ffffff"  // 바늘 중심 원 색
        textColor="transparent"    // 게이지 안의 기본 % 텍스트 숨김
      />
      {/* 아래쪽 점수 및 설명 텍스트 */}
      <div className="gauge-score-text">
        <div className="score-big">{score}%</div>   {/* 큰 숫자 점수 */}
        <div className="score-label">Phishing Risk</div>    {/* 설명 텍스트 */}
      </div>
    </div>
  );
}

export default GaugeScore;
