import { useState, useRef } from 'react'

export default function UploadZone({ file, onChange }) {
    const [dragging, setDragging] = useState(false)
    const inputRef = useRef()

    const handleDrop = (e) => {
        e.preventDefault()
        setDragging(false)
        const f = e.dataTransfer.files[0]
        if (f) onChange(f)
    }

    const fmt = (bytes) => bytes < 1024 * 1024
        ? `${(bytes / 1024).toFixed(1)} KB`
        : `${(bytes / (1024 * 1024)).toFixed(1)} MB`

    return (
        <div>
            {!file ? (
                <div
                    className={`upload-zone ${dragging ? 'dragging' : ''}`}
                    onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
                    onDragLeave={() => setDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => inputRef.current?.click()}
                >
                    <input
                        ref={inputRef}
                        type="file"
                        accept=".pdf,.docx,.doc"
                        onChange={(e) => onChange(e.target.files[0])}
                        style={{ display: 'none' }}
                    />
                    <span className="upload-icon">📄</span>
                    <h3>Drop your resume here</h3>
                    <p>or click to browse files</p>
                    <div className="file-types">
                        <span className="file-type-badge">PDF</span>
                        <span className="file-type-badge">DOCX</span>
                        <span className="file-type-badge">DOC</span>
                    </div>
                </div>
            ) : (
                <div className="uploaded-file">
                    <span style={{ fontSize: '1.5rem' }}>✅</span>
                    <div style={{ flex: 1, minWidth: 0 }}>
                        <div className="file-name" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {file.name}
                        </div>
                        <div className="file-size">{fmt(file.size)}</div>
                    </div>
                    <button className="btn-clear-file" onClick={() => onChange(null)} title="Remove file">✕</button>
                </div>
            )}
        </div>
    )
}
