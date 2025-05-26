import React, { useEffect, useState } from 'react';
import './styles.css';
import waveLogo from './assets/www.png';

function App() {
  const [hovering, setHovering] = useState(false);

  useEffect(() => {
    chrome.storage.sync.get('hoveringEnabled', (data) => {
      setHovering(data.hoveringEnabled || false);
    });
  }, []);

  const toggleHovering = () => {
  const newState = !hovering;
  setHovering(newState);
  chrome.storage.sync.set({ hoveringEnabled: newState });

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTabId = tabs[0].id;

    // 현재 탭에 메시지 보내기
    chrome.runtime.sendMessage({ type: 'TOGGLE_HOVER', enabled: newState });

    // ✅ content.js가 주입되지 않은 경우, 수동 주입 시도
    chrome.scripting.executeScript({
      target: { tabId: currentTabId },
      files: ['content.js'],
    });
  });
  };

  return (
    <div className="container">
      <h2>
        wave to <img src={waveLogo} alt="wave logo" className="www" />
      </h2>

      <div className="toggle-row">
        <span>Mouse Hovering Mode</span>
        <label className="switch">
          <input type="checkbox" checked={hovering} onChange={toggleHovering} />
          <span className="slider round"></span>
        </label>
      </div>

      <button className="visit-button" onClick={() => window.open('https://naver.com')}>
        Visit Website
      </button>
    </div>
  );
}

export default App;
