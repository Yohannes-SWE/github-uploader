import React from "react"
import "./LandingPage.css"

const LandingPage = ({ onGetStarted }) => (
  <div className="landing-container">
    <img src="/logo.png" alt="RepoTorpedo Logo" className="brand-logo" />
    <header className="landing-header">
      <h1 style={{ color: "#F28C28" }}>
        Deploy Your Website Globally in Minutes
      </h1>
      <p className="landing-subtitle" style={{ color: "#183046" }}>
        No coding required. Instantly launch your site to the world with GitHub
        and Render.
      </p>
      <button className="get-started-btn" onClick={onGetStarted}>
        Get Started
      </button>
    </header>
    <section className="landing-features">
      <div className="feature">
        <strong>1.</strong> Connect your GitHub account securely
      </div>
      <div className="feature">
        <strong>2.</strong> Connect your Render account or use OAuth
      </div>
      <div className="feature">
        <strong>3.</strong> Drag & drop your website files
      </div>
      <div className="feature">
        <strong>4.</strong> Deploy and share your live site instantly
      </div>
    </section>
  </div>
)

export default LandingPage
