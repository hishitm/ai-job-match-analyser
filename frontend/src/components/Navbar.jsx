export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <div className="brand-icon">🎯</div>
                <span>JobMatch<span style={{ color: 'var(--cyan)' }}>AI</span></span>
            </div>
            <span className="navbar-badge">⚡ Powered by AI</span>
        </nav>
    )
}
