import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './UrlInputBox.css';

function UrlInputBox() {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [serverError, setServerError] = useState('');
  const navigate = useNavigate();

  const isValidUrl = (value) => {
    const pattern = new RegExp('^(https?:\\/\\/)?' +
      '(([\\da-z.-]+)\\.([a-z.]{2,6})|' +
      '(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +
      '(\\:[0-9]{1,5})?' +
      '(\\/[-a-zA-Z0-9()@:%_+.~#?&//=]*)?$', 'i');
    return pattern.test(value);
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!isValidUrl(url)) {
    setError('올바른 URL 형식이 아닙니다.');
    setServerError('');
    return;
  }

  setError('');
  setServerError('');

  try {
    const response = await axios.post(
      "http://localhost:8000/detect/url",
      { url },
      { headers: { "client-type": "web" },
        timeout: 3000
     }
    );

    console.log("✅ 서버 응답:", response);

    // success 래퍼 유무에 관계없이 처리
    const payload = response.data.data || response.data;

    const scanResult = {
      inputUrl: payload.input_url,
      resultFlag: payload.engine_result_flag,
      resultScore: payload.engine_result_score,
    };

    const scanModuleResultMap = Array.isArray(payload.module_result_dictionary_list)
  ? payload.module_result_dictionary_list.map(module => ({
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
          return data.map(d => typeof d === 'string' ? d.slice(0, 10) : String(d).slice(0, 10));
        } else if (typeof data === 'string') {
          return [data.slice(0, 10)];
        } else if (data !== null && data !== undefined) {
          return [String(data).slice(0, 10)];
        } else {
          return null;
        }
      })()
    }))
  : [];


    navigate('/result', {
      state: {
        summary: scanResult,
        modules: scanModuleResultMap,
      },
    });
  } catch (err) {
  console.error("❌ Axios error:", err);
  if (err.response) {
    console.error("❌ Server responded with error:", err.response);
    setServerError(err.response.data.message || '서버 오류가 발생했습니다.');
  } else if (err.request) {
    console.error("❌ No response received:", err.request);
    setServerError('서버에 연결할 수 없습니다.');
  } else {
    console.error("❌ Request setup error:", err.message);
    setServerError(`요청 설정 중 오류가 발생했습니다. (${err.message})`);
  }
}

};


  return (
    <div className="url-input-wrapper">
      <form className="url-input-form" onSubmit={handleSubmit}>
        <div className="url-input-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="URL을 입력해주세요."
            className="url-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        {error && <div className="error-message">{error}</div>}
        {serverError && <div className="server-error-message">{serverError}</div>}
      </form>
    </div>
  );
}

export default UrlInputBox;
