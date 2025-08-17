// src/components/FriendlyExplain.js
import React, { useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { getLang } from './lang';

// 마크다운/별표 제거기
function stripMd(s = '') {
  return s
    // 굵게/기울임/인라인코드/헤딩/링크/체크박스 등 제거
    .replace(/\*\*(.*?)\*\*/g, '$1')              // **bold**
    .replace(/__(.*?)__/g, '$1')                  // __bold__
    .replace(/\*(?!\*)([^*\n]+?)\*(?!\*)/g, '$1') // *italic*
    .replace(/`([^`]+?)`/g, '$1')                 // `code`
    .replace(/^\s{0,3}#{1,6}\s*/gm, '')           // # heading
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')      // [text](url)
    .replace(/^\s*[-*]\s+\[.\]\s*/gm, '- ')       // - [ ] item
    // 남은 표식들 최종 제거
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
    // 직전 요청 중단
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    let startTimer = null;   // fetch 시작을 "다음 틱"으로 지연
    let abortTimer = null;   // 실제 요청이 시작된 뒤에만 타임아웃 세팅

    const run = async () => {
      setLoading(true);
      setErr('');
      setText('');

      // 요청이 실제로 시작된 시점에만 타임아웃 가동
      abortTimer = setTimeout(() => {
        try { controller.abort(new DOMException('Timeout', 'AbortError')); } catch (_) { }
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
        // 서버 응답을 렌더 전에 정리
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

    // StrictMode에서 중복 요청 방지
    startTimer = setTimeout(run, 0);

    return () => {
      if (startTimer) clearTimeout(startTimer);
      if (abortTimer) clearTimeout(abortTimer);
      controller.abort();
    };
  }, [payload, makeLocalFallback]);

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
        {loading && <div style={{ opacity: 0.7 }}>{lang === 'ko' ? '설명을 생성하는 중…' : 'Generating explanation…'}</div>}

        {!loading && err && (
          <div style={{ color: '#B95250', marginBottom: 8 }}>
            {lang === 'ko' ? '서버 응답에 문제가 있어요.' : 'There was a problem with the server response.'}
          </div>
        )}

        {!loading && text}
      </div>
    </div>
  );
}
