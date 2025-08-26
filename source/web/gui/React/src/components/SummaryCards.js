// src/components/SummaryCards.js
import React from 'react';
import './SummaryCards.css';
import { PieChart, Pie, Cell } from 'recharts';
import FriendlyExplain from './FriendlyExplain';

function SummaryCards({ phishingCount, totalCount, aiScore = 0, summary, modules }) {
    const lang = localStorage.getItem('lang') || 'en';
    const safeCount = Math.max(0, totalCount - phishingCount);

    const COLORS = { Detected: '#B95250', Safe: '#2185B7' };

    const CHART_W = 260;
    const CHART_H = 150;
    const INNER_R = 75;
    const OUTER_R = 100;

    const moduleData = [
        { name: 'Detected', value: phishingCount },
        { name: 'Safe', value: safeCount },
    ];

    const aiVal = Math.max(0, Math.min(100, Number(aiScore) || 0));
    const aiData = [
        { name: 'AI', value: aiVal },
        { name: 'Remain', value: 100 - aiVal },
    ];

    // --- 새로 추가된 부분: AI 점수 색상 조건 ---
    const isAiHigh = aiVal >= 70;
    const AI_COLOR = isAiHigh ? '#B95250' : '#2185B7';   // 70↑이면 빨간색
    const AI_BG    = isAiHigh ? '#f3e8e8' : '#e6eef4';   // 배경은 연한 톤
    // -----------------------------------------

    const CX = CHART_W / 2;
    const CY = CHART_H;
    const centerY = CY - INNER_R * 0.55;
    const offsetX = INNER_R * 0.75;
    const leftX = CX - offsetX;
    const rightX = CX + offsetX;

    return (
        <div className="summary-wrapper">
            <h2 className="summary-title">{lang === 'ko' ? '탐지 요약' : 'Detection Summary'}</h2>

            <div className="summary-cards-container two-cols">
                <div className="donut-card">
                    {/* 모듈 요약 */}
                    <PieChart width={CHART_W} height={CHART_H}>
                        <Pie
                            data={moduleData}
                            cx="50%" cy="85%"
                            startAngle={180} endAngle={0}
                            innerRadius={INNER_R} outerRadius={OUTER_R}
                            paddingAngle={3}
                            dataKey="value"
                            cornerRadius={10}
                            isAnimationActive={false}
                        >
                            <Cell fill={COLORS.Detected} />
                            <Cell fill={COLORS.Safe} />
                        </Pie>

                        {/* 왼쪽: 숫자 + 라벨 */}
                        <text
                            x={leftX + 20}
                            y={centerY - 20}
                            textAnchor="middle"
                            dominantBaseline="central"
                            className="donut-center-number"
                            fill={COLORS.Detected}
                        >
                            {phishingCount}
                        </text>
                        <text
                            x={leftX + 36}
                            y={centerY + 5}
                            textAnchor="middle"
                            className="donut-center-caption"
                        >
                            {lang === 'ko' ? 'Detected' : 'Detected'}
                        </text>

                        {/* 오른쪽: 숫자 + 라벨 */}
                        <text
                            x={rightX - 20}
                            y={centerY - 20}
                            textAnchor="middle"
                            dominantBaseline="central"
                            className="donut-center-number"
                            fill={COLORS.Safe}
                        >
                            {safeCount}
                        </text>
                        <text
                            x={rightX - 20}
                            y={centerY + 5}
                            textAnchor="middle"
                            className="donut-center-caption"
                        >
                            {lang === 'ko' ? 'Safe' : 'Safe'}
                        </text>
                    </PieChart>
                    <div className="modules-below">{totalCount} Modules</div>

                    <div className="half-caption">
                        <span className="dot red" /> Detected {totalCount ? ((phishingCount / totalCount) * 100).toFixed(1) : 0}%
                        <span className="caption-sep"> · </span>
                        <span className="dot blue" /> Safe {totalCount ? ((safeCount / totalCount) * 100).toFixed(1) : 0}%
                    </div>

                    {/* AI 점수 (조건 색상 적용) */}
                    <PieChart width={CHART_W} height={CHART_H}>
                        <Pie
                            data={aiData}
                            cx="50%" cy="90%"
                            startAngle={180} endAngle={0}
                            innerRadius={INNER_R} outerRadius={OUTER_R}
                            dataKey="value"
                            cornerRadius={10}
                            isAnimationActive={false}
                        >
                            <Cell fill={AI_COLOR} />
                            <Cell fill={AI_BG} />
                        </Pie>

                        {/* AI 값 중앙 표시 (숫자 색도 조건 적용) */}
                        <text
                            x={CX}
                            y={CY - 58}
                            textAnchor="middle"
                            dominantBaseline="central"
                            className="donut-center-number"
                            fill={AI_COLOR}
                        >
                            {Math.round(aiVal)}%
                        </text>
                        <text
                            x={CX}
                            y={CY - INNER_R * 0.55 + 18}
                            textAnchor="middle"
                            className="donut-center-ai"
                        >
                            AI Score
                        </text>
                    </PieChart>
                </div>

                <div className="explain-card">
                    <FriendlyExplain summary={summary} modules={modules} />
                </div>
            </div>
        </div>
    );
}

export default SummaryCards;
