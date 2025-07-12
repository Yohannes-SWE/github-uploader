import React, { useState, useEffect } from "react"
import { API_URL } from "../config"

const SetupWizard = ({ onSetupComplete }) => {
  const [step, setStep] = useState(1)
  const [clientId, setClientId] = useState("")
  const [clientSecret, setClientSecret] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [instructions, setInstructions] = useState([])

  useEffect(() => {
    loadInstructions()
  }, [])

  const loadInstructions = async () => {
    try {
      const response = await fetch(`${API_URL}/api/setup/instructions`)
      const data = await response.json()
      setInstructions(data.instructions)
    } catch (err) {
      console.error("Failed to load instructions:", err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    setSuccess("")

    try {
      const formData = new FormData()
      formData.append("client_id", clientId)
      formData.append("client_secret", clientSecret)

      const response = await fetch(`${API_URL}/api/setup/github`, {
        method: "POST",
        body: formData
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess("GitHub OAuth configured successfully!")
        setTimeout(() => {
          onSetupComplete()
        }, 2000)
      } else {
        setError(data.error || "Failed to configure GitHub OAuth")
      }
    } catch (err) {
      setError("Network error. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setSuccess("Copied to clipboard!")
    setTimeout(() => setSuccess(""), 2000)
  }

  if (step === 1) {
    return (
      <div className="setup-wizard">
        <div className="setup-container">
          <h2>🚀 Welcome to RepoTorpedo Setup</h2>
          <p>
            Let's get your GitHub OAuth app configured so you can deploy
            websites!
          </p>

          <div className="setup-steps">
            <div className="step active">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Create GitHub OAuth App</h3>
                <p>
                  First, you need to create a GitHub OAuth application to allow
                  this app to access your repositories.
                </p>

                <div className="instructions">
                  <h4>Step-by-step instructions:</h4>
                  <ol>
                    {instructions.map((instruction, index) => (
                      <li key={index}>{instruction}</li>
                    ))}
                  </ol>
                </div>

                <div className="callback-url-section">
                  <h4>Callback URL for your GitHub OAuth App:</h4>
                  <div className="url-display">
                    <code>
                      https://repotorpedo-backend.onrender.com/api/auth/github/callback
                    </code>
                    <button
                      onClick={() =>
                        copyToClipboard(
                          "https://repotorpedo-backend.onrender.com/api/auth/github/callback"
                        )
                      }
                      className="copy-btn"
                    >
                      Copy
                    </button>
                  </div>
                </div>

                <button onClick={() => setStep(2)} className="next-btn">
                  I've created my GitHub OAuth App →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="setup-wizard">
      <div className="setup-container">
        <h2>🔧 Configure GitHub OAuth</h2>
        <p>Enter your GitHub OAuth App credentials below:</p>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleSubmit} className="setup-form">
          <div className="form-group">
            <label htmlFor="clientId">GitHub Client ID:</label>
            <input
              type="text"
              id="clientId"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
              placeholder="Enter your GitHub Client ID"
              required
            />
            <small>Found in your GitHub OAuth App settings</small>
          </div>

          <div className="form-group">
            <label htmlFor="clientSecret">GitHub Client Secret:</label>
            <input
              type="password"
              id="clientSecret"
              value={clientSecret}
              onChange={(e) => setClientSecret(e.target.value)}
              placeholder="Enter your GitHub Client Secret"
              required
            />
            <small>Found in your GitHub OAuth App settings</small>
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="back-btn"
            >
              ← Back to Instructions
            </button>
            <button
              type="submit"
              disabled={loading || !clientId || !clientSecret}
              className="submit-btn"
            >
              {loading ? "Configuring..." : "Configure OAuth"}
            </button>
          </div>
        </form>

        <div className="help-section">
          <h4>Need help?</h4>
          <ul>
            <li>
              Make sure your GitHub OAuth App's callback URL is exactly:{" "}
              <code>
                https://repotorpedo-backend.onrender.com/api/auth/github/callback
              </code>
            </li>
            <li>
              Ensure your OAuth App has the "repo" and "user" scopes enabled
            </li>
            <li>
              Double-check that you've copied the Client ID and Client Secret
              correctly
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default SetupWizard
