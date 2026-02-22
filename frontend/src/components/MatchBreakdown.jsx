export default function MatchBreakdown({ matched = [], missing = [], resumeSkills = [] }) {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            {/* Matched */}
            {matched.length > 0 && (
                <div>
                    <p className="skill-section-title">✅ Skills you have ({matched.length})</p>
                    <div className="skill-chips">
                        {matched.map(s => (
                            <span key={s} className="skill-chip matched">✓ {s}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Missing */}
            {missing.length > 0 && (
                <div>
                    <p className="skill-section-title">❌ Skills to acquire ({missing.length})</p>
                    <div className="skill-chips">
                        {missing.map(s => (
                            <span key={s} className="skill-chip missing">✕ {s}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* All resume skills if nothing from JD matched */}
            {matched.length === 0 && missing.length === 0 && resumeSkills.length > 0 && (
                <div>
                    <p className="skill-section-title">Your Skills ({resumeSkills.length})</p>
                    <div className="skill-chips">
                        {resumeSkills.slice(0, 24).map(s => (
                            <span key={s} className="skill-chip resume">{s}</span>
                        ))}
                    </div>
                </div>
            )}

            {matched.length === 0 && missing.length === 0 && resumeSkills.length === 0 && (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    No skills could be extracted from this job or resume text.
                </p>
            )}
        </div>
    )
}
