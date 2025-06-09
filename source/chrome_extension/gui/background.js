// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log('✅ Background script loaded');
});

// ✅ popup(App.jsx)에서 메시지 수신
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'TOGGLE_HOVER_ALL_TABS') {
    console.log('🌍 [Background] Toggling hovering for all tabs:', message.enabled);

    chrome.tabs.query({}, (tabs) => {
      tabs.forEach((tab) => {
        const url = tab.url;
        if (
          url &&
          !url.startsWith('chrome://') &&
          !url.startsWith('chrome-extension://')
        ) {
          // ✅ content.js 강제 주입
          chrome.scripting.executeScript(
            {
              target: { tabId: tab.id },
              files: ['content.js'],
            },
            () => {
              // ✅ 주입 후 상태 메시지 전송
              chrome.tabs.sendMessage(tab.id, {
                type: 'TOGGLE_HOVER',
                enabled: message.enabled,
              });
            }
          );
        }
      });
    });
  }
});
