// src/components/FriendlyExplain.js
import React, { useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { getLang } from './lang';

// 마크다운/별표 제거기
function stripMd(s = '') {
  return s
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/__(.*?)__/g, '$1')
    .replace(/\*(?!\*)([^*\n]+?)\*(?!\*)/g, '$1')
    .replace(/`([^`]+?)`/g, '$1')
    .replace(/^\s{0,3}#{1,6}\s*/gm, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/^\s*[-*]\s+\[.\]\s*/gm, '- ')
    .replace(/\*\*/g, '')
    .replace(/__/g, '')
    .replace(/```/g, '');
}

export default function FriendlyExplain({ summary, modules }) {
  const lang = getLang();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const abortRef = useRef(null);

  const payload = useMemo(() => {
    const safeSummary = {
      inputUrl: summary?.inputUrl ?? '',
      resultFlag: !!summary?.resultFlag,
      resultScore: typeof summary?.resultScore === 'number' ? summary.resultScore : 0,
      reportedToKisa: !!summary?.reportedToKisa,
    };
    const safeModules = Array.isArray(modules)
      ? modules.map((m) => ({
        moduleName: String(m.moduleName ?? ''),
        moduleResultFlag: !!m.moduleResultFlag,
        moduleScore: typeof m.moduleScore === 'number' ? m.moduleScore : null,
        moduleWeight: typeof m.moduleWeight === 'number' ? m.moduleWeight : null,
        moduleRun: typeof m.moduleRun === 'boolean' ? m.moduleRun : null,
        reason: (() => {
          const r = m.reason;
          if (r == null) return null;
          if (typeof r === 'string') return r.slice(0, 1000);
          if (Array.isArray(r)) return r.slice(0, 20).map((x) => String(x).slice(0, 500));
          if (typeof r === 'object') return Object.fromEntries(Object.entries(r).slice(0, 20));
          return String(r).slice(0, 1000);
        })(),
      }))
      : [];
    return { lang, summary: safeSummary, modules: safeModules };
  }, [lang, summary, modules]);

  const makeLocalFallback = useCallback(() => {
    const detected = payload.modules.filter((m) => m.moduleResultFlag).length;
    const score = payload.summary.resultScore ?? 0;
    const list = payload.modules
      .filter((m) => m.moduleResultFlag)
      .map((m) => `• ${m.moduleName}`)
      .slice(0, 8)
      .join('\n');
    const more = detected > 8 ? `\n...and ${detected - 8} more` : '';
    const raw =
      lang === 'ko'
        ? `총점: ${Math.round(score)}%\n위험 신호가 감지된 항목:\n${list}${more}\n\n※ 서버 오류로 간략 해설을 표시합니다.`
        : `Overall score: ${Math.round(score)}%\nSuspicious indicators detected in:\n${list}${more}\n\n※ Showing a lightweight summary due to a server error.`;
    return stripMd(raw);
  }, [payload, lang]);

  useEffect(() => {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    let startTimer = null;
    let abortTimer = null;

    const run = async () => {
      setLoading(true);
      setErr('');
      setText('');

      abortTimer = setTimeout(() => {
        try {
          controller.abort(new DOMException('Timeout', 'AbortError'));
        } catch (_) { }
      }, 20000);

      try {
        const res = await fetch('/explain', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: controller.signal,
        });

        if (!res.ok) {
          setErr(`HTTP ${res.status}`);
          setText(makeLocalFallback());
          return;
        }

        const data = await res.json();
        const serverText = data?.data?.explanation ?? data?.explanation ?? '';
        if (!serverText) {
          setErr('Empty response');
          setText(makeLocalFallback());
          return;
        }
        setText(stripMd(serverText));
      } catch (e) {
        if (e?.name !== 'AbortError') {
          setErr('network');
          setText(makeLocalFallback());
        }
      } finally {
        if (abortTimer) clearTimeout(abortTimer);
        setLoading(false);
      }
    };

    startTimer = setTimeout(run, 0);

    return () => {
      if (startTimer) clearTimeout(startTimer);
      if (abortTimer) clearTimeout(abortTimer);
      controller.abort();
    };
  }, [payload, makeLocalFallback]);

  // === 인라인 스피너 스타일 정의 ===
  const spinnerStyle = {
    width: 24,
    height: 24,
    border: '3px solid #ccc',
    borderTop: '3px solid #171717',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  };

  return (
    <div style={{ textAlign: 'left', width: '100%' }}>
      <div style={{ fontWeight: 600, marginBottom: 8, textAlign: 'center', color: '#171717' }}>
        {lang === 'ko' ? '해설' : 'Explanation'}
      </div>

      <div
        className="explain-scroll"
        style={{
          fontSize: 14,
          lineHeight: 1.6,
          color: '#171717',
          whiteSpace: 'pre-wrap',
          height: 300,
          overflowY: 'scroll',
          scrollbarGutter: 'stable both-edges',
        }}
      >
        {loading && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center', // 세로 가운데
              alignItems: 'center',     // 가로 가운데
              height: '100%',
              opacity: 0.9,
            }}
          >
            <div className="spinner"></div>
            <div style={{ marginTop: 30 }}>
              {lang === 'ko' ? '설명을 생성하는 중…' : 'Generating explanation…'}
            </div>

            <style>
              {`
              .spinner {
                width: 10px;
                height: 10px;
                border-radius: 10px;
                box-shadow: 28px 0px 0 0 #2185B7,
                            22.7px 16.5px 0 0 #2185B7,
                            8.68px 26.6px 0 0 #2185B7,
                            -8.68px 26.6px 0 0 #2185B7,
                            -22.7px 16.5px 0 0 #2185B7;
                animation: spinner-b87k6z 1s infinite linear;
              }

              @keyframes spinner-b87k6z {
                to {
                  transform: rotate(360deg);
                }
              }
            `}
            </style>
          </div>
        )}


        {!loading && err && (
          <div style={{ color: '#B95250', marginBottom: 8 }}>
            {lang === 'ko' ? '서버 응답에 문제가 있어요.' : 'There was a problem with the server response.'}
          </div>
        )}

        {!loading && text}
      </div>

      {/* 인라인 keyframes */}
      <style>
        {`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
}
