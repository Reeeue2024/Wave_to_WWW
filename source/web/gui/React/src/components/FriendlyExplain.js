// src/components/FriendlyExplain.js

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { getLang } from './lang';

export default function FriendlyExplain({ summary, modules }) {
    const lang = getLang(); // 'ko' | 'en'
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(true);
    const [err, setErr] = useState('');
    const abortRef = useRef(null);

    // 서버 스키마(ExplainRequest)에 맞게 클린업
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
                // reason은 문자열/배열/객체 케이스가 있어 백엔드가 처리하기 쉽게 그대로 전달하되 과도한 길이는 절단
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

    // 로컬 경량 요약(서버 실패시 사용)
    const makeLocalFallback = () => {
        const total = payload.modules.length;
        const detected = payload.modules.filter((m) => m.moduleResultFlag).length;
        const score = payload.summary.resultScore ?? 0;

        if (lang === 'ko') {
            return (
                `Overall score: ${Math.round(score)}%\n` +
                `Suspicious indicators detected in:\n` +
                payload.modules
                    .filter((m) => m.moduleResultFlag)
                    .map((m) => `• ${m.moduleName}`)
                    .slice(0, 8)
                    .join('\n') +
                (detected > 8 ? `\n...and ${detected - 8} more` : '') +
                `\n\n※ Showing a lightweight summary due to a server error.`
            );
        }
        return (
            `Overall score: ${Math.round(score)}%\n` +
            `Suspicious indicators detected in:\n` +
            payload.modules
                .filter((m) => m.moduleResultFlag)
                .map((m) => `• ${m.moduleName}`)
                .slice(0, 8)
                .join('\n') +
            (detected > 8 ? `\n...and ${detected - 8} more` : '') +
            `\n\n※ Showing a lightweight summary due to a server error.`
        );
    };

    useEffect(() => {
        // 기존 요청 취소
        if (abortRef.current) abortRef.current.abort();
        const controller = new AbortController();
        abortRef.current = controller;

        (async () => {
            setLoading(true);
            setErr('');
            setText('');

            try {
                // 프록시 경유(개발/도커/배포 공통)
                const res = await fetch('/explain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload), // ✅ 스키마: { lang, summary, modules }
                    signal: controller.signal,
                });

                if (!res.ok) {
                    // 4xx/5xx는 로컬 요약으로 대체
                    setErr(`HTTP ${res.status}`);
                    setText(makeLocalFallback());
                    return;
                }

                const data = await res.json();
                // 백엔드는 { ok, data: { explanation, lang } } 형태를 반환
                const serverText =
                    data?.data?.explanation ??
                    data?.explanation ?? // 혹시 다른 버전 대비
                    '';

                if (!serverText) {
                    setErr('Empty response');
                    setText(makeLocalFallback());
                    return;
                }

                setText(serverText);
            } catch (e) {
                if (e?.name === 'AbortError') return; // 언마운트/언어전환 등
                setErr('network');
                setText(makeLocalFallback());
            } finally {
                setLoading(false);
            }
        })();

        return () => controller.abort();
    }, [payload]); // lang/summary/modules 변경 시 재요청

    return (
        <div style={{ textAlign: 'left', width: '100%' }}>
            <div style={{ fontWeight: 600, marginBottom: 8, textAlign: 'center', color: '#171717' }}>
                {lang === 'ko' ? '해설' : 'Explanation'}
            </div>

            {loading && (
                <div style={{ opacity: 0.7 }}>
                    {lang === 'ko' ? '설명을 생성하는 중…' : 'Generating explanation…'}
                </div>
            )}

            {!!err && !loading && (
                <div style={{ color: '#B95250', marginBottom: 8 }}>
                    {lang === 'ko' ? '서버 응답에 문제가 있어요.' : 'There was a problem with the server response.'}
                </div>
            )}

            {!loading && (
                <div
                className="explain-scroll"
                    style={{
                        fontSize: 14,
                        lineHeight: 1.6,
                        color: '#171717',
                        whiteSpace: 'pre-wrap',
                        height: 300,
                        overflowY: 'scroll',
                        scrollbarGutter: 'stable both-edges'
                    }}
                >
                    {text}
                </div>
            )}
        </div>
    );
}
