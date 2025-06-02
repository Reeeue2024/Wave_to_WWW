// src/components/UrlInputBox.js
// 사용자가 입력한 URL을 검증하고 백엔드에 전송하여 피싱 여부를 분석한 뒤 결과 페이지로 이동하는 입력 폼 컴포넌트

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast, cssTransition } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './UrlInputBox.css';
import searchIcon from '../assets/img/search_icon.png';

// 토스트 애니메이션 제거를 위한 설정
const NoAnimation = cssTransition({
  enter: 'no-enter',
  exit: 'no-exit',
  duration: [1, 1],
});

function UrlInputBox() {
  // URL 입력값, 오류 상태 관리
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [serverError, setServerError] = useState('');
  const navigate = useNavigate();

  // URL 형식 유효성 검사 함수
  const isValidUrl = (value) => {
    const pattern = new RegExp('^(https?:\\/\\/)?' +  // http 또는 https 프로토콜
      '(([\\da-z.-]+)\\.([a-z.]{2,6})|' +              // 도메인명
      '(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +              // 또는 IPv4
      '(\\:[0-9]{1,5})?' +                             // 포트 번호
      '(\\/[-a-zA-Z0-9()@:%_+.~#?&//=]*)?$', 'i');      // 경로
    return pattern.test(value);
  };

  // 사용자 중심의 에러 토스트 출력 함수
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

  // 제출 버튼 클릭 시 실행되는 이벤트 핸들러
  const handleSubmit = async (e) => {
    e.preventDefault(); // 기본 폼 제출 막기

    // URL 형식이 유효하지 않으면 오류 처리
    if (!isValidUrl(url)) {
      const msg = 'The URL format is invalid.';
      setError(msg);
      setServerError('');
      showCenteredToast(msg);
      return;
    }

    // 오류 초기화
    setError('');
    setServerError('');

    try {
      // 백엔드 API로 URL 전송
      const response = await axios.post(
        'http://localhost:3000/detect/url',
        { url },
        {
          headers: { 'client-type': 'web' },
          timeout: 30000,
        }
      );

      const payload = response.data.data || response.data;

      // 결과 요약 정보 구성
      const scanResult = {
        inputUrl: payload.input_url,
        resultFlag: payload.engine_result_flag,
        resultScore: payload.engine_result_score,
      };

      // 모듈별 상세 결과 가공
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
              if (Array.isArray(data)) {
                return data.map((d) => (typeof d === 'string' ? d : String(d)));
              } else if (typeof data === 'string') {
                return [data];
              } else if (data !== null && data !== undefined) {
                return [String(data)];
              } else {
                return null;
              }
            })(),
          }))
        : [];

      // 결과 페이지로 이동하며 상태 전달
      navigate('/result', {
        state: {
          summary: scanResult,
          modules: scanModuleResultMap,
          inputUrl: url,
        },
      });
    } catch (err) {
      // 네트워크 또는 서버 오류 처리
      console.error('Axios error:', err);
      let msg = '';
      if (err.response) {
        msg = err.response.data.message || 'Server responded with error.';
      } else if (err.request) {
        msg = 'No response received.';
      } else {
        msg = `Request setup error. (${err.message})`;
      }
      setServerError(msg);
      showCenteredToast(msg);
    }
  };

  return (
    <div className="url-input-wrapper">
      <form className="url-input-form" onSubmit={handleSubmit}>
        <div className="url-input-box">
          {/* 검색 아이콘 */}
          <img src={searchIcon} alt="Search" className="search-icon" />
          {/* URL 입력창 */}
          <input
            type="text"
            placeholder="Enter the URL"
            className="url-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)} // 입력값 변경 반영
          />
        </div>
      </form>
    </div>
  );
}

export default UrlInputBox;
