// src/components/UrlInputBox.js

import React, { useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast, cssTransition } from 'react-toastify';
import WaveLoader from './WaveLoader';
import 'react-toastify/dist/ReactToastify.css';
import './UrlInputBox.css';
import searchIcon from '../assets/img/search_icon.png';

// 필요한 경우 상대경로로 프록시 사용(백엔드/Nginx 설정에 맞춰 '' 또는 'http://localhost:3000'로)
const API_BASE = ''; // 예: '' → 같은 도메인/프록시, 'http://localhost:3000' → 직접 호출

// 커스텀 토스트(애니메이션 제거)
const NoAnimation = cssTransition({
  enter: 'no-enter',
  exit: 'no-exit',
  duration: [1, 1],
});

function UrlInputBox() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const canceled = useRef(false);

  // URL 유효성 검사
  const isValidUrl = (value) => {
    const pattern = new RegExp(
      '^(https?:\\/\\/)?' +
        '(([\\da-z.-]+)\\.([a-z.]{2,6})|' +
        '(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +
        '(\\:[0-9]{1,5})?' +
        '(\\/[-a-zA-Z0-9()@:%_+.~#?&//=]*)?$',
      'i'
    );
    return pattern.test(value);
  };

  // 중앙 토스트
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

  // 폼 제출
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isValidUrl(url)) {
      showCenteredToast('The URL format is invalid.');
      return;
    }

    setLoading(true);

    try {
      // 1) 탐지 요청
      const { data } = await axios.post(
        `${API_BASE}/detect/url`,
        { url },
        { headers: { 'client-type': 'web' }, timeout: 30000 }
      );

      const payload = data?.data || data || {};

      // 2) 요약 스키마 정규화
      const summary = {
        inputUrl: String(payload.input_url ?? ''),
        resultFlag: !!payload.engine_result_flag,
        resultScore: Number(payload.engine_result_score ?? 0) || 0,
        reportedToKisa: !!(payload.reported_to_kisa ?? false),
      };

      // 3) 모듈 스키마 정규화
      const modulesRaw = Array.isArray(payload.module_result_dictionary_list)
        ? payload.module_result_dictionary_list
        : [];

      const modules = modulesRaw.map((m) => {
        const reasonData = m?.module_result_data?.reason_data;
        let normalizedReason = m?.module_result_data?.reason ?? null;

        // reason이 비어있고 reason_data만 있는 경우 보조로 채움
        if (normalizedReason == null && reasonData != null) {
          if (Array.isArray(reasonData)) normalizedReason = reasonData.map(String).slice(0, 20);
          else if (typeof reasonData === 'object')
            normalizedReason = Object.entries(reasonData)
              .slice(0, 20)
              .map(([k, v]) => `${k}: ${String(v)}`);
          else normalizedReason = String(reasonData);
        }

        return {
          moduleName: String(m?.module_class_name ?? ''),
          moduleResultFlag: !!m?.module_result_flag,
          moduleScore: typeof m?.module_score === 'number' ? m.module_score : null,
          moduleWeight: typeof m?.module_weight === 'number' ? m.module_weight : null,
          moduleRun: typeof m?.module_run === 'boolean' ? m.module_run : null,
          reason: normalizedReason ?? null,
        };
      });

      // 4) 로딩 해제 후 결과 페이지 이동 (로더에 갇히지 않도록 선해제)
      if (!canceled.current) {
        setLoading(false);
        navigate('/result', { state: { summary, modules } });
      }
    } catch (err) {
      console.error('Detect flow error:', err);
      const msg =
        err?.response?.data?.message
          ? String(err.response.data.message)
          : err?.message
          ? String(err.message)
          : 'Server error.';
      showCenteredToast(msg);

      if (canceled.current) {
        navigate('/');
      }
    } finally {
      // 어떤 경우에도 로딩 해제(중복 호출되어도 안전)
      setLoading(false);
    }
  };

  // 로딩 화면
  if (loading)
    return (
      <WaveLoader
        url={url}
        onCancelHome={() => {
          canceled.current = true;
          setLoading(false);
          navigate('/');
        }}
      />
    );

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
