// src/setupProxy.js
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    ['/detect', '/explain'], // 이 경로만 백엔드로 전달
    createProxyMiddleware({
      target: 'http://server:3000', // 도커 서비스명 + 내부 포트
      changeOrigin: true,
    })
  );
};
