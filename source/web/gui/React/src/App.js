// src/App.js
// 라우팅과 전역 토스트 설정을 포함한 React 앱의 진입점(App 컴포넌트)

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Result from './pages/Result';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [isToastVisible, setIsToastVisible] = useState(false);

  // 토스트 상태를 감지하여 표시 여부를 관리
  useEffect(() => {
    const id = toast.onChange((payload) => {
      setIsToastVisible(payload.status === 'active');
    });
    return () => toast.dismiss(id);
  }, []);

  return (
    <Router>
      {/* 전역 토스트 컨테이너 설정 */}
      <ToastContainer
        autoClose={2000}     
        position="top-left"
        toastClassName="center-toast"
        bodyClassName="center-toast-body"
        closeOnClick
        hideProgressBar={false}
        draggable={false}
      />

      {/* 페이지 라우팅 설정 */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </Router>
  );
}

export default App;
