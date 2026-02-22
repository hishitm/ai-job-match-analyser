import { useState } from 'react'

const PLATFORMS = {
    internshala: 'Internshala',
    linkedin: 'LinkedIn',
    naukri: 'Naukri',
    indeed: 'Indeed',
    glassdoor: 'Glassdoor',
    wellfound: 'Wellfound',
    foundit: 'Foundit',
    generic: 'Job Site',
}

function detectPlatform(url) {
    const u = url.toLowerCase()
    for (const k of Object.keys(PLATFORMS)) {
        if (u.includes(k)) return k
    }
    return 'generic'
}

export default function JobLinksPanel({ urls, onChange }) {
    const [input, setInput] = useState('')
    const [error, setError] = useState('')

    const add = () => {
        const trimmed = input.trim()
        if (!trimmed) return
        if (!trimmed.startsWith('http')) {
            setError('URL must start with http:// or https://')
            return
        }
        if (urls.includes(trimmed)) {
            setError('This URL is already added.')
            return
        }
        if (urls.length >= 5) {
            setError('Maximum 5 job links allowed.')
            return
        }
        onChange([...urls, trimmed])
        setInput('')
        setError('')
    }

    const remove = (url) => onChange(urls.filter(u => u !== url))

    return (
        <div>
            <div className="url-input-row">
                <input
                    className="url-input"
                    type="url"
                    placeholder="https://internshala.com/job/..."
                    value={input}
                    onChange={(e) => { setInput(e.target.value); setError('') }}
                    onKeyDown={(e) => e.key === 'Enter' && add()}
                />
                <button className="btn-add-url" onClick={add} disabled={urls.length >= 5}>＋</button>
            </div>

            {error && (
                <p style={{ fontSize: '0.8rem', color: 'var(--red)', marginBottom: '8px' }}>⚠ {error}</p>
            )}

            {urls.map((url) => {
                const platform = detectPlatform(url)
                const display = url.length > 55 ? url.slice(0, 52) + '…' : url
                return (
                    <div key={url} className="url-tag">
                        <span className="platform-badge">{PLATFORMS[platform]}</span>
                        <span>{display}</span>
                        <button className="btn-remove-url" onClick={() => remove(url)}>✕</button>
                    </div>
                )
            })}

            <p className="url-limit-info">
                {urls.length} / 5 links added &nbsp;·&nbsp; Supports Internshala, LinkedIn, Naukri, Indeed & more
            </p>
        </div>
    )
}
