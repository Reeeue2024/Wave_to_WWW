console.log('✅ content.js loaded!');

// ✅ 중복 주입 방지 플래그
if (window.hasHoverScript) {
  console.log('⚠️ content.js already injected, skipping...');
} else {
  window.hasHoverScript = true;
  console.log('✅ content.js activating...');

  let hoverTooltip;
  let hoverEnabled = true;
  let hoverTimer = null;  // ✅ 디바운스용 타이머 변수 추가

  function createTooltip(text) {
    if (!hoverTooltip) {
      hoverTooltip = document.createElement('div');
      hoverTooltip.style.position = 'fixed';
      hoverTooltip.style.zIndex = '9999';
      hoverTooltip.style.padding = '6px 10px';
      hoverTooltip.style.fontSize = '12px';
      hoverTooltip.style.borderRadius = '5px';
      hoverTooltip.style.backgroundColor = '#333';
      hoverTooltip.style.color = '#fff';
      hoverTooltip.style.boxShadow = '0 0 8px rgba(0,0,0,0.3)';
      hoverTooltip.style.pointerEvents = 'none';
      hoverTooltip.style.display = 'none';
      document.body.appendChild(hoverTooltip);
    }
    hoverTooltip.innerText = text;
  }

  function showTooltip(x, y) {
    if (hoverTooltip) {
      hoverTooltip.style.left = `${x + 15}px`;
      hoverTooltip.style.top = `${y + 15}px`;
      hoverTooltip.style.display = 'block';
    }
  }

  function hideTooltip() {
    if (hoverTooltip) {
      hoverTooltip.style.display = 'none';
    }
  }

  // ✅ 토글 버튼 상태 연동
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'TOGGLE_HOVER') {
      hoverEnabled = message.enabled;
      console.log('🟡 Hovering 기능 상태 변경됨:', hoverEnabled);
    }
  });

  // ✅ 확장 상태 기억하기
  chrome.storage.sync.get('hoveringEnabled', (data) => {
    hoverEnabled = data.hoveringEnabled ?? false;
  });

  // ✅ 마우스 호버링 이벤트 (백엔드 연동 포함, 디바운싱 적용)
  document.addEventListener('mouseover', (e) => {
    if (!hoverEnabled) return;

    const link = e.target.closest('a[href]');
    if (!link) return;

    // ✅ 기존 타이머가 있으면 클리어 (이동 중 요청 방지)
    if (hoverTimer) {
      clearTimeout(hoverTimer);
    }

    // ✅ 새 타이머 시작 (예: 100ms 후 실행)
    hoverTimer = setTimeout(async () => {
      try {
        const res = await fetch('http://localhost:8000/detect/url', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'client-type': 'extension'
          },
          body: JSON.stringify({ url: link.href })
        });

        if (!res.ok) throw new Error('서버 응답 오류');

        const data = await res.json();

        if (data.success) {
          const flag = data.data.engine_result_flag;
          const message = flag
            ? '⚠️ Suspicious phishing site!'
            : '✅ Safe Link';
          createTooltip(message);
          showTooltip(e.pageX, e.pageY);
        } else {
          createTooltip('❌ test failed');
          showTooltip(e.pageX, e.pageY);
        }
      } catch (err) {
        console.error('❌ Server communication failure:', err);
        createTooltip('❌ server error');
        showTooltip(e.pageX, e.pageY);
      }
    }, 500);  // ✅ 여기서 100ms 설정 (테스트로 조정 가능)
  });

  // ✅ 마우스 벗어날 때 툴팁 숨김 + 타이머 클리어
  document.addEventListener('mouseout', () => {
    hideTooltip();
    if (hoverTimer) {
      clearTimeout(hoverTimer);
      hoverTimer = null;
    }
  });
}
