import React, { useState, useEffect } from "react"
import RenderAuth from "./RenderAuth"
import "./RenderDeploy.css"

const RenderDeploy = () => {
  const [renderAuthenticated, setRenderAuthenticated] = useState(false)
  const [userInfo, setUserInfo] = useState(null)
  const [githubRepo, setGithubRepo] = useState("")
  const [projectName, setProjectName] = useState("")
  const [customEnvVars, setCustomEnvVars] = useState("")
  const [isDeploying, setIsDeploying] = useState(false)
  const [deploymentResult, setDeploymentResult] = useState(null)
  const [deploymentHistory, setDeploymentHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)

  useEffect(() => {
    checkRenderAuthStatus()
    loadDeploymentHistory()
  }, [])

  const checkRenderAuthStatus = async () => {
    try {
      const response = await fetch("/api/auth/render/status", {
        credentials: "include"
      })

      if (response.ok) {
        const data = await response.json()
        setRenderAuthenticated(data.render_authenticated)
        setUserInfo(data.user_info)
      }
    } catch (error) {
      console.error("Error checking Render auth status:", error)
    }
  }

  const handleAuthComplete = (userInfo) => {
    setRenderAuthenticated(!!userInfo)
    setUserInfo(userInfo)
  }

  const loadDeploymentHistory = async () => {
    try {
      const response = await fetch("/api/render/my-deployments", {
        credentials: "include"
      })

      if (response.ok) {
        const data = await response.json()
        setDeploymentHistory(data.deployments || [])
      }
    } catch (error) {
      console.error("Error loading deployment history:", error)
    }
  }

  const handleDeploy = async (e) => {
    e.preventDefault()

    if (!githubRepo.trim()) {
      setDeploymentResult({
        type: "error",
        message: "Please enter a GitHub repository"
      })
      return
    }

    setIsDeploying(true)
    setDeploymentResult(null)

    try {
      // Parse environment variables
      const envVars = {}
      if (customEnvVars.trim()) {
        customEnvVars.split("\n").forEach((line) => {
          const [key, ...valueParts] = line.split("=")
          if (key && valueParts.length > 0) {
            envVars[key.trim()] = valueParts.join("=").trim()
          }
        })
      }

      const response = await fetch("/api/render/deploy", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          github_repo: githubRepo,
          project_name: projectName || undefined,
          custom_env_vars: Object.keys(envVars).length > 0 ? envVars : undefined
        })
      })

      const data = await response.json()

      if (response.ok) {
        setDeploymentResult({
          type: "success",
          message: data.message,
          deployment: data.deployment,
          deploymentId: data.deployment_id
        })

        // Clear form
        setGithubRepo("")
        setProjectName("")
        setCustomEnvVars("")

        // Reload deployment history
        loadDeploymentHistory()
      } else {
        setDeploymentResult({
          type: "error",
          message: data.detail || "Deployment failed"
        })
      }
    } catch (error) {
      setDeploymentResult({
        type: "error",
        message: "Network error. Please try again."
      })
    } finally {
      setIsDeploying(false)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  const getDeploymentUrls = (deployment) => {
    const urls = []
    if (deployment.deployment_urls) {
      Object.entries(deployment.deployment_urls).forEach(([type, url]) => {
        urls.push({ type, url })
      })
    }
    return urls
  }

  if (!renderAuthenticated) {
    return (
      <div className="render-deploy-container">
        <div className="deploy-header">
          <h2>🚀 Deploy to Render</h2>
          <p>Connect your Render account to start deploying applications</p>
        </div>
        <RenderAuth onAuthComplete={handleAuthComplete} />
      </div>
    )
  }

  return (
    <div className="render-deploy-container">
      <div className="deploy-header">
        <h2>🚀 Deploy to Render</h2>
        <p>Deploy any application to Render with automatic configuration</p>
        {userInfo && (
          <div className="user-info-badge">
            Connected as: {userInfo.name || userInfo.email}
          </div>
        )}
      </div>

      <div className="deploy-content">
        <div className="deploy-form-section">
          <form onSubmit={handleDeploy} className="deploy-form">
            <div className="form-group">
              <label htmlFor="githubRepo">GitHub Repository *</label>
              <input
                type="text"
                id="githubRepo"
                value={githubRepo}
                onChange={(e) => setGithubRepo(e.target.value)}
                placeholder="owner/repository-name"
                className="form-control"
                disabled={isDeploying}
                required
              />
              <small className="form-text">
                Format: username/repository-name (e.g., johndoe/my-react-app)
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="projectName">Project Name (Optional)</label>
              <input
                type="text"
                id="projectName"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="my-awesome-app"
                className="form-control"
                disabled={isDeploying}
              />
              <small className="form-text">
                Leave empty to use repository name. Will be used for service
                naming.
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="customEnvVars">
                Environment Variables (Optional)
              </label>
              <textarea
                id="customEnvVars"
                value={customEnvVars}
                onChange={(e) => setCustomEnvVars(e.target.value)}
                placeholder="NODE_ENV=production&#10;DATABASE_URL=postgresql://...&#10;API_KEY=your-key"
                className="form-control"
                rows="4"
                disabled={isDeploying}
              />
              <small className="form-text">
                One variable per line: KEY=VALUE
              </small>
            </div>

            <button
              type="submit"
              className="btn btn-primary deploy-btn"
              disabled={isDeploying || !githubRepo.trim()}
            >
              {isDeploying ? "Deploying..." : "Deploy to Render"}
            </button>
          </form>
        </div>

        <div className="deploy-results-section">
          {deploymentResult && (
            <div className={`deployment-result ${deploymentResult.type}`}>
              <h4>
                {deploymentResult.type === "success"
                  ? "✅ Deployment Successful"
                  : "❌ Deployment Failed"}
              </h4>
              <p>{deploymentResult.message}</p>

              {deploymentResult.deployment && (
                <div className="deployment-details">
                  <h5>Deployment Details:</h5>
                  <div className="deployment-urls">
                    {getDeploymentUrls(deploymentResult.deployment).map(
                      ({ type, url }) => (
                        <div key={type} className="deployment-url">
                          <strong>
                            {type.charAt(0).toUpperCase() + type.slice(1)}:
                          </strong>
                          <a
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {url}
                          </a>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="deployment-history">
            <div className="history-header">
              <h4>📋 Recent Deployments</h4>
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="btn btn-secondary btn-sm"
              >
                {showHistory ? "Hide" : "Show"} History
              </button>
            </div>

            {showHistory && deploymentHistory.length > 0 && (
              <div className="history-list">
                {deploymentHistory.map((deployment) => (
                  <div key={deployment.id} className="history-item">
                    <div className="history-item-header">
                      <strong>
                        {deployment.project_name || deployment.github_repo}
                      </strong>
                      <span className="history-timestamp">
                        {formatTimestamp(deployment.timestamp)}
                      </span>
                    </div>
                    <div className="history-item-details">
                      <div>
                        Repository:{" "}
                        {deployment.github_repo || deployment.repo_url}
                      </div>
                      <div>Type: {deployment.result.app_type}</div>
                      {getDeploymentUrls(deployment.result).map(
                        ({ type, url }) => (
                          <div key={type} className="history-url">
                            <strong>{type}:</strong>{" "}
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              {url}
                            </a>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {showHistory && deploymentHistory.length === 0 && (
              <p className="no-history">
                No deployments yet. Deploy your first application!
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RenderDeploy
