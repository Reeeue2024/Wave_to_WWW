console.log('✅ content.js loaded!');

let hoverTooltip;
let hoverEnabled = true;

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

// 토글 버튼 상태 연동
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'TOGGLE_HOVER') {
    hoverEnabled = message.enabled;
    console.log('🟡 Hovering 기능 상태 변경됨:', hoverEnabled);
  }
});

// 확장 상태 기억하기
chrome.storage.sync.get('hoveringEnabled', (data) => {
  hoverEnabled = data.hoveringEnabled ?? true;
});

// ✅ 마우스 호버링 이벤트 (백엔드 연동 포함)
document.addEventListener('mouseover', async (e) => {  // ← async 추가
  if (!hoverEnabled) return;

  const link = e.target.closest('a[href]');
  if (!link) return;

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
        ? '⚠️ 피싱 의심 사이트!'
        : '✅ 안전한 링크';
      createTooltip(message);
      showTooltip(e.pageX, e.pageY);
    } else {
      createTooltip('❌ 검사 실패');
      showTooltip(e.pageX, e.pageY);
    }
  } catch (err) {
    console.error('❌ 서버 통신 실패:', err);
    createTooltip('❌ 서버 오류');
    showTooltip(e.pageX, e.pageY);
  }
});

// 마우스 벗어날 때 툴팁 숨김
document.addEventListener('mouseout', () => {
  hideTooltip();
});
