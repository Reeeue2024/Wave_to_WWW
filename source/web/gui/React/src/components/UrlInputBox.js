// src/components/UrlInputBox.js

import React, { useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast, cssTransition } from 'react-toastify';
import WaveLoader from './WaveLoader';
import 'react-toastify/dist/ReactToastify.css';
import './UrlInputBox.css';
import searchIcon from '../assets/img/search_icon.png';

// 커스텀 토스트 애니메이션 제거 설정 (입장/퇴장 효과 없음)
const NoAnimation = cssTransition({
  enter: 'no-enter',
  exit: 'no-exit',
  duration: [1, 1],
});


function UrlInputBox() {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [serverError, setServerError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const canceled = useRef(false);

  // URL 유효성 검사 정규표현식
  const isValidUrl = (value) => {
    const pattern = new RegExp('^(https?:\\/\\/)?' +
      '(([\\da-z.-]+)\\.([a-z.]{2,6})|' +
      '(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +
      '(\\:[0-9]{1,5})?' +
      '(\\/[-a-zA-Z0-9()@:%_+.~#?&//=]*)?$', 'i');
    return pattern.test(value);
  };

  // 중앙에 커스텀 토스트 메시지를 표시하는 함수
  const showCenteredToast = (msg) => {
    toast.error(msg, {
      transition: NoAnimation,
      autoClose: 2000,
      toastClassName: 'center-toast',
      bodyClassName: 'center-toast-body',
      progressClassName: 'custom-toast-progress',
      onOpen: () => {
        const overlay = document.createElement('div');
        overlay.className = 'toast-dim-overlay';
        document.body.appendChild(overlay);
      },
      onClose: () => {
        const overlay = document.querySelector('.toast-dim-overlay');
        if (overlay) overlay.remove();
      },
    });
  };

  // 폼 제출 이벤트 처리
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isValidUrl(url)) {
      const msg = 'The URL format is invalid.';
      setError(msg);
      setServerError('');
      showCenteredToast(msg);
      return;
    }

    setError('');
    setServerError('');
    setLoading(true);

    try {
      // 백엔드 서버로 URL 분석 요청
      const response = await axios.post(
        'http://localhost:3000/detect/url',
        { url },
        {
          headers: { 'client-type': 'web' },
          timeout: 30000,
        }
      );

      const payload = response.data.data || response.data;

      // 요약 결과 저장
      const scanResult = {
        inputUrl: payload.input_url,
        resultFlag: payload.engine_result_flag,
        resultScore: payload.engine_result_score,
        reportedToKisa: payload.reported_to_kisa ?? false  //  키사 플래그 파싱
      };

      // 모듈별 분석 결과 정리
      const scanModuleResultMap = Array.isArray(payload.module_result_dictionary_list)
  ? payload.module_result_dictionary_list.map((module) => ({
      moduleName: module.module_class_name,
      moduleRun: module.module_run,
      moduleScore: module.module_score,
      moduleWeight: module.module_weight,
      moduleResultFlag: module.module_result_flag,
      moduleError: module.module_error || null,
      reason: module.module_result_data?.reason || null,
      reasonData: (() => {
        const data = module.module_result_data?.reason_data;

        // ✅ AI 모듈일 때: 객체로 올 경우 처리
        if (
          module.module_class_name === 'Ai' &&
          typeof data === 'object' &&
          data !== null &&
          !Array.isArray(data)
        ) {
          return Object.entries(data).map(([key, value]) => `${key}: ${value}`);
        }

        // ✅ 일반적인 배열/string 처리
        if (Array.isArray(data)) return data.map((d) => String(d));
        if (typeof data === 'string') return [data];
        if (data != null) return [String(data)];

        return null;
      })(),
    }))
  : [];


      // 페이지 이동 (결과 페이지로)
      if (!canceled.current) {
        navigate('/result', {
          state: {
            summary: scanResult,
            modules: scanModuleResultMap,
          },
        });
      }

    } catch (err) {
      console.error('Axios error:', err);
      let msg = '';
      if (err.response) msg = err.response.data.message || 'Server error.';
      else if (err.request) msg = 'No response from server.';
      else msg = `Request error: ${err.message}`;

      setServerError(msg);
      showCenteredToast(msg);

      // 취소 상태일 경우 홈으로 이동, 아니면 로딩 해제
      if (canceled.current) {
        navigate('/');
      } else {
        setLoading(false);
      }
    }
  };

  // 로딩 중이면 WaveLoader 로딩 화면 출력
  if (loading) return <WaveLoader url={url} onCancelHome={() => {
    canceled.current = true;
    setLoading(false); // 로딩 종료
    navigate('/');     // 홈으로 이동
  }} />;

  return (
    <div className="url-input-wrapper">
      <form className="url-input-form" onSubmit={handleSubmit}>
        <div className="url-input-box">
          <img src={searchIcon} alt="Search" className="search-icon" />
          <input
            type="text"
            placeholder="Enter the URL"
            className="url-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
      </form>
    </div>
  );
}

export default UrlInputBox;
