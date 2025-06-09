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

    // ✅ background.js에 메시지 보내기
    chrome.runtime.sendMessage({
      type: 'TOGGLE_HOVER_ALL_TABS',
      enabled: newState,
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

      <button
        className="visit-button"
        onClick={() => window.open('https://naver.com')}
      >
        Visit Website
      </button>
    </div>
  );
}

export default App;
