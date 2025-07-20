import React from "react"

const Header = () => (
  <header
    style={{
      background: "#183046",
      padding: "0.75rem 2rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      boxShadow: "0 2px 8px rgba(24,48,70,0.06)"
    }}
    aria-label="Main header"
  >
    <div style={{ display: "flex", alignItems: "center" }}>
      <a href="/" tabIndex={0} aria-label="Home - RepoTorpedo">
        <img
          src="/logo.png"
          alt="RepoTorpedo Logo"
          style={{ height: 40, marginRight: 16 }}
        />
      </a>
      <span
        style={{
          color: "#fff",
          fontWeight: 700,
          fontSize: "1.7rem",
          letterSpacing: 1,
          textShadow: "1px 1px 2px #000"
        }}
      >
        REPO
        <span style={{ color: "#F28C28", textShadow: "1px 1px 2px #000" }}>
          TORPEDO
        </span>
      </span>
    </div>
    {/* Placeholder for navigation or user actions */}
    <div></div>
  </header>
)

export default Header
