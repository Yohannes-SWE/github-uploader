// Configuration for different environments
const config = {
  development: {
    apiUrl: "http://localhost:8000",
    environment: "development",
    debug: true,
    features: {
      aiAnalysis: true,
      platformIntegration: true,
      cicdGeneration: true
    }
  },
  production: {
    apiUrl:
      process.env.REACT_APP_API_URL ||
      "https://repotorpedo-backend.onrender.com",
    environment: "production",
    debug: false,
    features: {
      aiAnalysis: true,
      platformIntegration: true,
      cicdGeneration: true
    }
  }
}

// Get current environment - default to production if on Render
const isRenderDeployment = window.location.hostname.includes("onrender.com")
const environment =
  process.env.REACT_APP_ENVIRONMENT ||
  (isRenderDeployment ? "production" : "development")

// Debug logging
console.log("Environment detection:", {
  REACT_APP_ENVIRONMENT: process.env.REACT_APP_ENVIRONMENT,
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  isRenderDeployment: isRenderDeployment,
  detectedEnvironment: environment
})

// Export current configuration
export const currentConfig = config[environment]

// Export API URL for easy access
export const API_URL = currentConfig.apiUrl

// Debug logging
console.log("API URL resolved:", API_URL)

// Export environment info
export const ENVIRONMENT = currentConfig.environment
export const DEBUG = currentConfig.debug

// Export feature flags
export const FEATURES = currentConfig.features

// Export domain information
export const DOMAINS = {
  frontend: "repotorpedo-frontend.onrender.com",
  backend: "repotorpedo-backend.onrender.com"
}

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${API_URL}${endpoint}`
}

// Helper function to check if feature is enabled
export const isFeatureEnabled = (feature) => {
  return FEATURES[feature] || false
}

// Helper function for logging (respects debug setting)
export const log = (message, data = null) => {
  if (DEBUG) {
    console.log(`[${ENVIRONMENT}] ${message}`, data)
  }
}

// Helper function for error logging
export const logError = (message, error = null) => {
  console.error(`[${ENVIRONMENT}] ERROR: ${message}`, error)
}

// Helper function to get domain URLs
export const getDomainUrl = (type = "frontend") => {
  const protocol = ENVIRONMENT === "production" ? "https" : "http"
  const domain = DOMAINS[type]
  return `${protocol}://${domain}`
}

export default currentConfig
