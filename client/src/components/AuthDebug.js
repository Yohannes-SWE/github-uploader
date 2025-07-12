import React, { useState, useEffect } from "react"
import { API_URL } from "../config"

const AuthDebug = () => {
  const [authStatus, setAuthStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [urlParams, setUrlParams] = useState({})

  useEffect(() => {
    // Get URL parameters
    const params = new URLSearchParams(window.location.search)
    const paramsObj = {}
    for (const [key, value] of params) {
      paramsObj[key] = value
    }
    setUrlParams(paramsObj)

    // Check auth status
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    setLoading(true)
    try {
      console.log("Checking auth status from debug component...")
      const response = await fetch(`${API_URL}/api/auth/status`, {
        credentials: "include"
      })
      const data = await response.json()
      console.log("Auth status response:", data)
      setAuthStatus(data)
    } catch (error) {
      console.error("Auth check failed:", error)
      setAuthStatus({ error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const startOAuth = () => {
    window.location.href = `${API_URL}/api/auth/github/login`
  }

  const clearUrlParams = () => {
    window.history.replaceState({}, document.title, window.location.pathname)
    setUrlParams({})
  }

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>OAuth Debug Page</h1>

      <div style={{ marginBottom: "20px" }}>
        <h3>URL Parameters:</h3>
        <pre>{JSON.stringify(urlParams, null, 2)}</pre>
        {Object.keys(urlParams).length > 0 && (
          <button onClick={clearUrlParams}>Clear URL Parameters</button>
        )}
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h3>Authentication Status:</h3>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <pre>{JSON.stringify(authStatus, null, 2)}</pre>
        )}
        <button onClick={checkAuthStatus}>Refresh Auth Status</button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h3>Actions:</h3>
        <button onClick={startOAuth} style={{ marginRight: "10px" }}>
          Start GitHub OAuth
        </button>
        <button onClick={() => (window.location.href = "/")}>
          Go to Main App
        </button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h3>Debug Info:</h3>
        <p>
          <strong>Current URL:</strong> {window.location.href}
        </p>
        <p>
          <strong>API URL:</strong> {API_URL}
        </p>
        <p>
          <strong>Cookies:</strong> {document.cookie || "No cookies"}
        </p>
      </div>
    </div>
  )
}

export default AuthDebug
