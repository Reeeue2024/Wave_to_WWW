// src/components/WaveLoader.js
// URL 분석 중 파도 애니메이션 로딩 화면을 표시하는 컴포넌트

import React, { useEffect, useState } from 'react';
import Header from './Header';
import './WaveLoader.css';

// 파도 애니메이션 로딩 화면을 출력하는 컴포넌트
function WaveLoader({ url }) {
  const [waveTop, setWaveTop] = useState(50); // 파도 위치 상태값 (% 단위)

  // 파도 위치를 주기적으로 위로 올리다가 다시 초기화하는 애니메이션 효과
  useEffect(() => {
    let val = 50; // 시작 위치
    const interval = setInterval(() => {
      val -= 1;          // 점점 위로 이동
      setWaveTop(val);
      if (val <= -55) {  // 특정 높이 이상 올라가면 초기화
        val = 50;
        setWaveTop(50);
      }
    }, 25); // 25ms 간격으로 갱신

    return () => clearInterval(interval); // 언마운트 시 인터벌 정리
  }, []);

  return (
    <div className="wave-loader-wrapper wave-loader-active">
      <div className="wave-loader-header">
        <Header />
      </div>
      {/* 원형 테두리 안에 파도 표시 */}
      <div className="circle-wrapper">
        <div className="circle">
          {/* CSS 변수로 파도 위치 전달 */}
          <div className="wave" style={{ '--waveTop': `${waveTop}%` }}></div>
        </div>
      </div>

      {/* 로딩 상태 텍스트 */}
      <div className="loading-text">Scanning the waves of the web...</div>

      {/* 분석 중인 URL이 있으면 표시 */}
      {url && <div className="loading-url">"{url}"</div>}
    </div>
  );
}

export default WaveLoader;
