export default function InsightsPanel({ insights = [], improvements = [], atsDetails = [] }) {
    function barClass(score, max) {
        const pct = score / max
        if (pct >= 0.7) return 'green'
        if (pct >= 0.4) return 'yellow'
        return 'red'
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
            {/* Insights */}
            {insights.length > 0 && (
                <div>
                    <p className="skill-section-title">💡 Key Insights</p>
                    <div className="gap-12">
                        {insights.map((ins, i) => (
                            <div key={i} className={`insight-card ${ins.type}`}>
                                <span className="insight-icon">{ins.icon}</span>
                                <div>
                                    <div className="insight-title">{ins.title}</div>
                                    <div className="insight-message">{ins.message}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Improvements */}
            {improvements.length > 0 && (
                <div>
                    <p className="skill-section-title">🚀 How to Improve</p>
                    <div className="gap-12">
                        {improvements.map((imp, i) => (
                            <div key={i} className="improvement-card">
                                <span className="improv-icon">{imp.icon}</span>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                                        <span className="improv-title">{imp.title}</span>
                                        <span className={`priority-tag ${imp.priority}`}>{imp.priority}</span>
                                    </div>
                                    <div className="improv-detail">{imp.detail}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* ATS Detail Breakdown */}
            {atsDetails.length > 0 && (
                <div>
                    <p className="skill-section-title">🤖 ATS Score Breakdown</p>
                    {atsDetails.map((d, i) => (
                        <div key={i} className="ats-detail-row">
                            <span className="ats-detail-name">{d.category}</span>
                            <div className="ats-bar-wrap">
                                <div
                                    className={`ats-bar-fill ${barClass(d.score, d.max)}`}
                                    style={{ width: `${(d.score / d.max) * 100}%` }}
                                />
                            </div>
                            <span className="ats-detail-score">{d.score}/{d.max}</span>
                            <span className="ats-detail-note">{d.note}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
