import React, { useState, useEffect } from "react"
import { API_URL } from "../config"
import "./RenderSetup.css"

const RenderSetup = ({ onSetupComplete }) => {
  const [apiKey, setApiKey] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState(null)
  const [renderConfigured, setRenderConfigured] = useState(false)

  useEffect(() => {
    checkRenderStatus()
  }, [])

  const checkRenderStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/render/status`, {
        credentials: "include"
      })

      if (response.ok) {
        const data = await response.json()
        setRenderConfigured(data.render_configured)
        if (data.render_configured) {
          setStatus({
            type: "success",
            message: "Render credentials already configured"
          })
        }
      }
    } catch (error) {
      console.error("Error checking Render status:", error)
    }
  }

  const handleSetup = async (e) => {
    e.preventDefault()

    if (!apiKey.trim()) {
      setStatus({ type: "error", message: "Please enter your Render API key" })
      return
    }

    setIsLoading(true)
    setStatus(null)

    try {
      const response = await fetch(`${API_URL}/api/render/setup`, {
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
        setRenderConfigured(true)
        setApiKey("") // Clear the input for security
        if (onSetupComplete) {
          onSetupComplete()
        }
      } else {
        setStatus({
          type: "error",
          message: data.detail || "Failed to set up Render credentials"
        })
      }
    } catch (error) {
      setStatus({ type: "error", message: "Network error. Please try again." })
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearCredentials = async () => {
    try {
      const response = await fetch(`${API_URL}/api/render/clear-credentials`, {
        method: "POST",
        credentials: "include"
      })

      if (response.ok) {
        setRenderConfigured(false)
        setStatus({ type: "success", message: "Render credentials cleared" })
      }
    } catch (error) {
      setStatus({ type: "error", message: "Failed to clear credentials" })
    }
  }

  const getApiKeyInstructions = () => {
    return (
      <div className="api-key-instructions">
        <h4>How to get your Render API key:</h4>
        <ol>
          <li>
            Go to{" "}
            <a
              href="https://dashboard.render.com/account/api-keys"
              target="_blank"
              rel="noopener noreferrer"
            >
              Render Dashboard
            </a>
          </li>
          <li>Click on "API Keys" in the left sidebar</li>
          <li>Click "New API Key"</li>
          <li>Give it a name (e.g., "GitHub Uploader")</li>
          <li>Copy the generated API key</li>
          <li>Paste it in the field above</li>
        </ol>
        <div className="security-note">
          <strong>🔒 Security Note:</strong> Your API key is stored securely in
          your browser session only. It's never saved to our servers and will be
          cleared when you close your browser.
        </div>
      </div>
    )
  }

  if (renderConfigured) {
    return (
      <div className="render-setup-container">
        <div className="render-setup-card">
          <div className="setup-header">
            <h3>✅ Render Credentials Configured</h3>
            <p>You're ready to deploy applications to Render!</p>
          </div>

          {status && (
            <div className={`status-message ${status.type}`}>
              {status.message}
            </div>
          )}

          <div className="setup-actions">
            <button
              onClick={handleClearCredentials}
              className="btn btn-secondary"
            >
              Clear Credentials
            </button>
            <button
              onClick={() => setRenderConfigured(false)}
              className="btn btn-primary"
            >
              Update API Key
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="render-setup-container">
      <div className="render-setup-card">
        <div className="setup-header">
          <h3>🔧 Set Up Render Credentials</h3>
          <p>Connect your Render account to deploy applications</p>
        </div>

        {status && (
          <div className={`status-message ${status.type}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSetup} className="setup-form">
          <div className="form-group">
            <label htmlFor="apiKey">Render API Key</label>
            <input
              type="password"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="rnd_..."
              className="form-control"
              disabled={isLoading}
            />
            <small className="form-text">
              Your API key starts with "rnd_" and is used to deploy to your
              Render account
            </small>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading || !apiKey.trim()}
          >
            {isLoading ? "Verifying..." : "Set Up Render"}
          </button>
        </form>

        {getApiKeyInstructions()}
      </div>
    </div>
  )
}

export default RenderSetup
