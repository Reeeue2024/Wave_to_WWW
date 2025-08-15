// src/components/GaugeScore.js

import React, { useEffect, useState } from 'react';
import { CircularProgressbarWithChildren, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css'; // 설치한 스타일
import './GaugeScore.css';

function GaugeScore({ score }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const isPhishing = score >= 70;
  const color = isPhishing ? '#B95250' : '#2185B7';

  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      current += 1;
      setAnimatedScore(current);
      if (current >= score) clearInterval(interval);
    }, 10); // 10ms 간격으로 증가 (0.83초 정도 소요)

    return () => clearInterval(interval);
  }, [score]);

  return (
    <div className={`gauge-wrapper ${isPhishing ? 'danger' : 'safe'}`}>
      <div className="donut-chart">
        <CircularProgressbarWithChildren
          value={animatedScore}
          maxValue={100}
          strokeWidth={12}
          styles={buildStyles({
            pathColor: color,
            trailColor: '#eeeeee',
          })}
        >
          <div className={`score-big ${isPhishing ? 'text-danger' : 'text-safe'}`}>
            {animatedScore}%
          </div>
          <div className="score-label">Phishing Risk</div>
        </CircularProgressbarWithChildren>
      </div>
    </div>
  );
}

export default GaugeScore;
