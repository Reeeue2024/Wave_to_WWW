// src/components/UrlInputBox.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast, cssTransition } from 'react-toastify';
import WaveLoader from './WaveLoader'; // ⬅️ 추가
import 'react-toastify/dist/ReactToastify.css';
import './UrlInputBox.css';
import searchIcon from '../assets/img/search_icon.png';

const NoAnimation = cssTransition({
  enter: 'no-enter',
  exit: 'no-exit',
  duration: [1, 1],
});

function UrlInputBox() {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [serverError, setServerError] = useState('');
  const [loading, setLoading] = useState(false); // ⬅️ WaveLoader 제어용
  const navigate = useNavigate();

  const isValidUrl = (value) => {
    const pattern = new RegExp('^(https?:\\/\\/)?' +
      '(([\\da-z.-]+)\\.([a-z.]{2,6})|' +
      '(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +
      '(\\:[0-9]{1,5})?' +
      '(\\/[-a-zA-Z0-9()@:%_+.~#?&//=]*)?$', 'i');
    return pattern.test(value);
  };

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
    setLoading(true); // ✅ WaveLoader 표시

    try {
      const response = await axios.post(
        'http://localhost:3000/detect/url',
        { url },
        {
          headers: { 'client-type': 'web' },
          timeout: 30000,
        }
      );

      const payload = response.data.data || response.data;

      const scanResult = {
        inputUrl: payload.input_url,
        resultFlag: payload.engine_result_flag,
        resultScore: payload.engine_result_score,
      };

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
            if (Array.isArray(data)) return data.map((d) => String(d));
            else if (typeof data === 'string') return [data];
            else if (data != null) return [String(data)];
            return null;
          })(),
        }))
        : [];

      navigate('/result', {
        state: {
          summary: scanResult,
          modules: scanModuleResultMap,
          inputUrl: url,
        },
      });
    } catch (err) {
      console.error('Axios error:', err);
      let msg = '';
      if (err.response) msg = err.response.data.message || 'Server error.';
      else if (err.request) msg = 'No response from server.';
      else msg = `Request error: ${err.message}`;

      setServerError(msg);
      showCenteredToast(msg);
      setLoading(false); // ❗ 실패 시만 로딩 해제
    }
  };

  if (loading) return <WaveLoader url={url} />; // ✅ 검사 중이면 WaveLoader만 렌더

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
