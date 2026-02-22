import { useState } from 'react'
import ScoreGauge from './ScoreGauge'
import MatchBreakdown from './MatchBreakdown'
import InsightsPanel from './InsightsPanel'

const FIT_CLASS = {
    'Excellent Fit': 'excellent',
    'Strong Fit': 'strong',
    'Good Fit': 'good',
    'Partial Fit': 'partial',
    'Low Fit': 'low',
    'Poor Fit': 'poor',
}

export default function JobCard({ result, resumeSkills, index }) {
    const [tab, setTab] = useState('skills')

    if (!result.success) {
        return (
            <div className="job-result-card" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="job-card-header">
                    <div>
                        <div className="job-card-title" style={{ color: 'var(--red)' }}>⚠ Failed to load job</div>
                        <div className="job-card-company">{result.url}</div>
                        <div className="job-card-location" style={{ color: 'var(--red)', marginTop: 6 }}>
                            Error: {result.error}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    const { job, match_score, ats_score, ats_grade, ats_summary, ats_details,
        fit_label, probability, matched_skills, missing_skills, insights, improvements } = result

    return (
        <div className="job-result-card" style={{ animationDelay: `${index * 0.12}s` }}>
            {/* Header */}
            <div className="job-card-header">
                <div>
                    <span className="job-platform-chip">{job.platform}</span>
                    <div className="job-card-title" style={{ marginTop: 8 }}>{job.title || 'Job Posting'}</div>
                    {job.company && <div className="job-card-company">🏢 {job.company}</div>}
                    {job.location && <div className="job-card-location">📍 {job.location}</div>}
                </div>
                <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ marginLeft: 'auto', fontSize: '0.82rem', color: 'var(--purple)', textDecoration: 'none', flexShrink: 0 }}
                >
                    View Job ↗
                </a>
            </div>

            {/* Body */}
            <div className="job-card-body">
                {/* Score Sidebar */}
                <div className="score-sidebar">
                    <ScoreGauge value={match_score} label="Match" />

                    <span className={`fit-badge ${FIT_CLASS[fit_label] || 'low'}`}>{fit_label}</span>

                    <div className="probability-box">
                        <div className="prob-label">CHANCE OF INTERVIEW</div>
                        <div className="prob-range" style={{ color: probability?.color }}>
                            {probability?.range || 'N/A'}
                        </div>
                        <div className="prob-desc">{probability?.label}</div>
                    </div>

                    <div className="ats-score-box">
                        <div className="ats-label">ATS SCORE</div>
                        <div>
                            <span className="ats-score-number" style={{ color: ats_score >= 70 ? 'var(--green)' : ats_score >= 50 ? 'var(--gold)' : 'var(--red)' }}>
                                {ats_score}
                            </span>
                            <span className={`ats-grade ${ats_grade}`}>{ats_grade}</span>
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4, lineHeight: 1.4 }}>
                            {ats_summary}
                        </div>
                    </div>
                </div>

                {/* Content Tabs */}
                <div className="job-content-area">
                    <div className="result-tabs">
                        {[
                            { id: 'skills', label: '🎯 Skills Match' },
                            { id: 'insights', label: '💡 Insights' },
                            { id: 'improve', label: '🚀 Improve' },
                            { id: 'ats', label: '🤖 ATS Details' },
                        ].map(t => (
                            <button
                                key={t.id}
                                className={`result-tab ${tab === t.id ? 'active' : ''}`}
                                onClick={() => setTab(t.id)}
                            >
                                {t.label}
                            </button>
                        ))}
                    </div>

                    {tab === 'skills' && (
                        <MatchBreakdown
                            matched={matched_skills}
                            missing={missing_skills}
                            resumeSkills={resumeSkills}
                        />
                    )}

                    {tab === 'insights' && (
                        <InsightsPanel insights={insights} improvements={[]} atsDetails={[]} />
                    )}

                    {tab === 'improve' && (
                        <InsightsPanel insights={[]} improvements={improvements} atsDetails={[]} />
                    )}

                    {tab === 'ats' && (
                        <InsightsPanel insights={[]} improvements={[]} atsDetails={ats_details || []} />
                    )}
                </div>
            </div>
        </div>
    )
}
