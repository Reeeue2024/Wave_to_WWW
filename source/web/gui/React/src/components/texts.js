// src/components/texts.js

export const texts = {
  en: {
    search: 'Search',
    about: 'About',
    scanning: 'Scanning the waves of the web...',
    detected: 'Phishing',        
    safe: 'Safe',
    phishingSummary: (x, y) => `${x} out of the ${y} modules reported suspected phishing detection.`,
    detection: 'DETECTION',
    details: 'DETAILS',

    detectedCard: 'Detected',
    phishingFinal: 'Phishing',
  },
  ko: {
    search: '검색',
    about: '소개',
    scanning: '웹의 파도를 스캔 중...',
    detected: 'Phishing',       
    safe: 'Safe',
    phishingSummary: (x, y) => `총 ${y}개 모듈 중 ${x}개가 피싱으로 탐지되었습니다.`,
    detection: '탐지 요약',
    details: '상세 정보',

    detectedCard: 'Detected',
    phishingFinal: 'Phishing',
  }
};
