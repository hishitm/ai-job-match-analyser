import { useState } from 'react'
import Navbar from './components/Navbar'
import UploadZone from './components/UploadZone'
import JobLinksPanel from './components/JobLinksPanel'
import JobCard from './components/JobCard'
import { analyseResume } from './api/client'

const LOADING_STEPS = [
    'Parsing your resume…',
    'Extracting skills with NLP…',
    'Fetching job postings…',
    'Analysing skill requirements…',
    'Calculating ATS scores…',
    'Generating insights…',
]

export default function App() {
    const [file, setFile] = useState(null)
    const [urls, setUrls] = useState([])
    const [loading, setLoading] = useState(false)
    const [loadStep, setLoadStep] = useState(0)
    const [result, setResult] = useState(null)
    const [error, setError] = useState('')

    const canAnalyse = file && urls.length > 0 && !loading

    const handleAnalyse = async () => {
        if (!canAnalyse) return
        setError('')
        setResult(null)
        setLoading(true)
        setLoadStep(0)

        // Animate loading steps
        const stepInterval = setInterval(() => {
            setLoadStep(s => Math.min(s + 1, LOADING_STEPS.length - 1))
        }, 1800)

        try {
            const data = await analyseResume(file, urls)
            setResult(data)
        } catch (err) {
            const msg = err?.response?.data?.detail || err?.message || 'Something went wrong. Please try again.'
            setError(msg)
        } finally {
            clearInterval(stepInterval)
            setLoading(false)
        }
    }

    const handleReset = () => {
        setResult(null)
        setError('')
        setFile(null)
        setUrls([])
    }

    return (
        <>
            <Navbar />

            {/* ── Hero ── */}
            {!result && !loading && (
                <section className="hero">
                    <div className="hero-eyebrow">
                        <span>🎯</span> AI-Powered Resume Intelligence
                    </div>
                    <h1>
                        Know Your{' '}
                        <span className="gradient-text">Job Match Score</span>
                        <br />Before You Apply
                    </h1>
                    <p>
                        Paste job links from Internshala, LinkedIn, or Naukri. Upload your resume.
                        Get your <strong>ATS score</strong>, <strong>match %</strong>, skill gaps, and actionable improvements — instantly.
                    </p>
                </section>
            )}

            {/* ── Input Panels ── */}
            {!result && !loading && (
                <>
                    <div className="input-panels">
                        {/* Job Links */}
                        <div className="panel-card">
                            <div className="panel-title">
                                <div className="panel-icon purple">🔗</div>
                                Job Links
                            </div>
                            <p className="panel-subtitle">
                                Paste up to 5 job posting URLs from any platform
                            </p>
                            <JobLinksPanel urls={urls} onChange={setUrls} />
                        </div>

                        {/* Resume Upload */}
                        <div className="panel-card">
                            <div className="panel-title">
                                <div className="panel-icon cyan">📄</div>
                                Your Resume
                            </div>
                            <p className="panel-subtitle">
                                Upload your CV or resume (PDF or DOCX, max 10 MB)
                            </p>
                            <UploadZone file={file} onChange={setFile} />
                        </div>
                    </div>

                    {error && (
                        <div className="error-banner" style={{ margin: '16px auto', maxWidth: 900 }}>
                            ⚠ {error}
                        </div>
                    )}

                    <div className="analyse-section">
                        <button className="btn-analyse" onClick={handleAnalyse} disabled={!canAnalyse}>
                            {!file && !urls.length
                                ? <><span>📎</span> Add job links & resume to start</>
                                : !file
                                    ? <><span>📄</span> Upload your resume to continue</>
                                    : !urls.length
                                        ? <><span>🔗</span> Add at least one job link</>
                                        : <><span>⚡</span> Analyse My Profile</>
                            }
                        </button>
                        {canAnalyse && (
                            <p style={{ marginTop: 12, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                                Analysing {urls.length} job{urls.length > 1 ? 's' : ''} · This may take 15–30 seconds
                            </p>
                        )}
                    </div>
                </>
            )}

            {/* ── Loading ── */}
            {loading && (
                <div className="loading-overlay">
                    <div className="loading-orb">🤖</div>
                    <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 800, marginBottom: 8 }}>
                        Analysing your profile…
                    </h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
                        Hold tight while we read the job listings and compare your skills.
                    </p>
                    <div className="loading-steps">
                        {LOADING_STEPS.map((step, i) => (
                            <div key={i} className={`loading-step ${i === loadStep ? 'active' : ''}`}>
                                <div className="step-dot" />
                                {step}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* ── Results ── */}
            {result && (
                <div className="results-container">
                    <div className="results-header">
                        <div>
                            <h2>📊 Your Analysis Results</h2>
                            <p style={{ color: 'var(--text-secondary)', marginTop: 4, fontSize: '0.9rem' }}>
                                {result.job_results?.length} job{result.job_results?.length > 1 ? 's' : ''} analysed
                                &nbsp;·&nbsp; {result.skill_count} skills found
                                &nbsp;·&nbsp; {result.experience_level} level detected
                            </p>
                        </div>
                        <button className="btn-reset" onClick={handleReset}>
                            ← Analyse another
                        </button>
                    </div>

                    {/* Resume summary strip */}
                    <div className="resume-strip">
                        <div className="resume-strip-stat">
                            <span className="stat-icon">📄</span>
                            <span className="stat-label">File:</span>
                            <span className="stat-val">{result.resume?.filename}</span>
                        </div>
                        <div className="strip-divider" />
                        <div className="resume-strip-stat">
                            <span className="stat-icon">🔠</span>
                            <span className="stat-label">Words:</span>
                            <span className="stat-val">{result.resume?.word_count}</span>
                        </div>
                        <div className="strip-divider" />
                        <div className="resume-strip-stat">
                            <span className="stat-icon">🧠</span>
                            <span className="stat-label">Skills found:</span>
                            <span className="stat-val" style={{ color: 'var(--cyan)' }}>{result.skill_count}</span>
                        </div>
                        <div className="strip-divider" />
                        <div className="resume-strip-stat">
                            <span className="stat-icon">📈</span>
                            <span className="stat-label">Level:</span>
                            <span className="stat-val" style={{ color: 'var(--purple)' }}>{result.experience_level}</span>
                        </div>
                        <div className="strip-divider" />
                        <div className="resume-strip-stat">
                            <span className="stat-icon">🤖</span>
                            <span className="stat-label">Overall ATS:</span>
                            <span className="stat-val" style={{
                                color: result.overall_ats?.ats_score >= 70 ? 'var(--green)'
                                    : result.overall_ats?.ats_score >= 50 ? 'var(--gold)' : 'var(--red)'
                            }}>
                                {result.overall_ats?.ats_score}/100 ({result.overall_ats?.grade})
                            </span>
                        </div>
                    </div>

                    {/* Skill Clusters */}
                    {result.clusters?.length > 0 && (
                        <>
                            <p className="section-label" style={{ marginBottom: 16 }}>
                                🗂 Your Skill Clusters
                            </p>
                            <div className="clusters-grid" style={{ padding: '0 0 32px' }}>
                                {result.clusters.map(c => (
                                    <div key={c.category} className="cluster-card">
                                        <div className="cluster-header">
                                            <span className="cluster-dot" style={{ background: c.color }} />
                                            <span className="cluster-label">{c.label}</span>
                                            <span className="cluster-count">{c.count} skills</span>
                                        </div>
                                        <div className="skill-chips">
                                            {c.skills.slice(0, 10).map(s => (
                                                <span
                                                    key={s}
                                                    className="skill-chip resume"
                                                    style={{
                                                        background: `${c.color}18`,
                                                        borderColor: `${c.color}40`,
                                                        color: c.color
                                                    }}
                                                >
                                                    {s}
                                                </span>
                                            ))}
                                            {c.skills.length > 10 && (
                                                <span className="skill-chip resume" style={{ opacity: 0.5 }}>
                                                    +{c.skills.length - 10} more
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </>
                    )}

                    {/* Per-Job Results */}
                    <p className="section-label" style={{ marginBottom: 20 }}>
                        💼 Job Match Results
                    </p>
                    {result.job_results?.map((jr, i) => (
                        <JobCard
                            key={jr.url}
                            result={jr}
                            resumeSkills={result.resume_skills}
                            index={i}
                        />
                    ))}
                </div>
            )}
        </>
    )
}
