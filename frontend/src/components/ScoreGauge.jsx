import { useEffect, useRef } from 'react'

function getColor(score) {
    if (score >= 75) return 'var(--green)'
    if (score >= 55) return 'var(--purple)'
    if (score >= 35) return 'var(--gold)'
    return 'var(--red)'
}

export default function ScoreGauge({ value = 0, label = 'Match', size = 140 }) {
    const circleRef = useRef()
    const r = 52
    const cx = size / 2
    const cy = size / 2
    const circumference = 2 * Math.PI * r
    const offset = circumference - (value / 100) * circumference
    const color = getColor(value)

    useEffect(() => {
        if (circleRef.current) {
            circleRef.current.style.strokeDashoffset = offset
        }
    }, [offset])

    return (
        <div className="gauge-wrap" style={{ width: size, height: size }}>
            <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
                {/* Track */}
                <circle
                    cx={cx} cy={cy} r={r}
                    fill="none"
                    stroke="rgba(255,255,255,0.06)"
                    strokeWidth="10"
                />
                {/* Glow filter */}
                <defs>
                    <filter id={`glow-${label}`}>
                        <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>
                {/* Progress arc */}
                <circle
                    ref={circleRef}
                    cx={cx} cy={cy} r={r}
                    fill="none"
                    stroke={color}
                    strokeWidth="10"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={circumference}
                    transform={`rotate(-90 ${cx} ${cy})`}
                    style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)', filter: `url(#glow-${label})` }}
                />
            </svg>
            <div className="gauge-label">
                <span className="gauge-value" style={{ color }}>{value}<span style={{ fontSize: '0.9rem' }}>%</span></span>
                <span className="gauge-sub">{label}</span>
            </div>
        </div>
    )
}
