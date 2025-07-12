import React, { useState, useEffect } from "react"
import { API_URL } from "../config"
import "./RenderAuth.css"

const RenderAuth = ({ onAuthComplete }) => {
  const [authStep, setAuthStep] = useState("init") // init, instructions, verify, success
  const [apiKey, setApiKey] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState(null)
  const [authData, setAuthData] = useState(null)
  const [userInfo, setUserInfo] = useState(null)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/auth/render/status`, {
        credentials: "include"
      })

      if (response.ok) {
        const data = await response.json()
        if (data.render_authenticated) {
          setAuthStep("success")
          setUserInfo(data.user_info)
          setStatus({
            type: "success",
            message: "Already authenticated with Render"
          })
        }
      }
    } catch (error) {
      console.error("Error checking auth status:", error)
    }
  }

  const startAuthFlow = async () => {
    setIsLoading(true)
    setStatus(null)

    try {
      const response = await fetch(`${API_URL}/api/auth/render/login`, {
        credentials: "include"
      })

      if (response.ok) {
        const data = await response.json()
        setAuthData(data)
        setAuthStep("instructions")
      } else {
        setStatus({
          type: "error",
          message: "Failed to start authentication flow"
        })
      }
    } catch (error) {
      setStatus({
        type: "error",
        message: "Network error. Please try again."
      })
    } finally {
      setIsLoading(false)
    }
  }

  const verifyApiKey = async (e) => {
    e.preventDefault()

    if (!apiKey.trim()) {
      setStatus({ type: "error", message: "Please enter your Render API key" })
      return
    }

    if (!apiKey.startsWith("rnd_")) {
      setStatus({
        type: "error",
        message: "Invalid API key format. Render API keys start with 'rnd_'"
      })
      return
    }

    setIsLoading(true)
    setStatus(null)

    try {
      const response = await fetch(`${API_URL}/api/auth/render/verify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ api_key: apiKey })
      })

      const data = await response.json()

      if (response.ok) {
        setStatus({ type: "success", message: data.message })
        setUserInfo(data.user_info)
        setAuthStep("success")
        setApiKey("") // Clear the input for security
        if (onAuthComplete) {
          onAuthComplete(data.user_info)
        }
      } else {
        setStatus({
          type: "error",
          message: data.detail || "Failed to verify API key"
        })
      }
    } catch (error) {
      setStatus({ type: "error", message: "Network error. Please try again." })
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_URL}/api/auth/render/logout`, {
        method: "POST",
        credentials: "include"
      })

      if (response.ok) {
        setAuthStep("init")
        setUserInfo(null)
        setStatus({ type: "success", message: "Logged out successfully" })
        if (onAuthComplete) {
          onAuthComplete(null)
        }
      }
    } catch (error) {
      setStatus({ type: "error", message: "Failed to logout" })
    }
  }

  const openRenderDashboard = () => {
    if (authData?.auth_url) {
      window.open(authData.auth_url, "_blank")
    }
  }

  if (authStep === "success") {
    return (
      <div className="render-auth-container">
        <div className="auth-success-card">
          <div className="success-header">
            <div className="success-icon">✅</div>
            <h3>Connected to Render!</h3>
            <p>You're ready to deploy applications</p>
          </div>

          {userInfo && (
            <div className="user-info">
              <div className="info-item">
                <span className="label">Account:</span>
                <span className="value">{userInfo.name || userInfo.email}</span>
              </div>
              {userInfo.email && (
                <div className="info-item">
                  <span className="label">Email:</span>
                  <span className="value">{userInfo.email}</span>
                </div>
              )}
            </div>
          )}

          <div className="auth-actions">
            <button onClick={handleLogout} className="btn btn-secondary">
              Disconnect Render
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (authStep === "instructions") {
    return (
      <div className="render-auth-container">
        <div className="auth-instructions-card">
          <div className="instructions-header">
            <h3>🔑 Get Your Render API Key</h3>
            <p>Follow these steps to connect your Render account</p>
          </div>

          {status && (
            <div className={`status-message ${status.type}`}>
              {status.message}
            </div>
          )}

          <div className="instructions-steps">
            {authData?.instructions?.steps.map((step, index) => (
              <div key={index} className="step-item">
                <div className="step-number">{index + 1}</div>
                <div className="step-text">{step}</div>
              </div>
            ))}
          </div>

          <div className="instructions-actions">
            <button
              onClick={openRenderDashboard}
              className="btn btn-primary"
              disabled={isLoading}
            >
              {isLoading ? "Opening..." : "Open Render Dashboard"}
            </button>
          </div>

          <div className="api-key-form">
            <h4>Step 6: Enter Your API Key</h4>
            <form onSubmit={verifyApiKey}>
              <div className="form-group">
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="rnd_..."
                  className="form-control"
                  disabled={isLoading}
                />
                <small className="form-text">
                  Paste your Render API key here (starts with "rnd_")
                </small>
              </div>
              <button
                type="submit"
                className="btn btn-success"
                disabled={isLoading || !apiKey.trim()}
              >
                {isLoading ? "Verifying..." : "Connect to Render"}
              </button>
            </form>
          </div>

          <div className="help-section">
            <h4>Need Help?</h4>
            <ul>
              <li>
                <strong>Can't find the API key page?</strong>
                <br />
                Go to{" "}
                <a
                  href="https://dashboard.render.com"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  dashboard.render.com
                </a>{" "}
                → Account → API Keys
              </li>
              <li>
                <strong>API key not working?</strong>
                <br />
                Make sure you copied the entire key (it should be about 64
                characters long)
              </li>
              <li>
                <strong>Getting permission errors?</strong>
                <br />
                Create a new API key with "Full Access" permissions
              </li>
            </ul>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="render-auth-container">
      <div className="auth-init-card">
        <div className="init-header">
          <h3>🚀 Connect to Render</h3>
          <p>Deploy your applications to Render with one click</p>
        </div>

        <div className="auth-benefits">
          <div className="benefit-item">
            <div className="benefit-icon">⚡</div>
            <div className="benefit-text">
              <h4>Quick Deploy</h4>
              <p>Deploy any application in seconds</p>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon">🔒</div>
            <div className="benefit-text">
              <h4>Secure</h4>
              <p>Your API key is stored securely in your session</p>
            </div>
          </div>
          <div className="benefit-item">
            <div className="benefit-icon">🆓</div>
            <div className="benefit-text">
              <h4>Free Tier</h4>
              <p>750 hours/month free hosting</p>
            </div>
          </div>
        </div>

        <button
          onClick={startAuthFlow}
          className="btn btn-primary btn-large"
          disabled={isLoading}
        >
          {isLoading ? "Starting..." : "Connect Render Account"}
        </button>

        <div className="auth-note">
          <p>
            <strong>Note:</strong> You'll need a Render account.
            <a
              href="https://render.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              Sign up for free
            </a>{" "}
            if you don't have one.
          </p>
        </div>
      </div>
    </div>
  )
}

export default RenderAuth
