// Configuration for different environments
const config = {
  development: {
    apiUrl: "https://api.repotorpedo.com",
    environment: "development",
    debug: true,
    features: {
      aiAnalysis: true,
      platformIntegration: true,
      cicdGeneration: true
    }
  },
  production: {
    apiUrl: process.env.REACT_APP_API_URL || "https://api.repotorpedo.com",
    environment: "production",
    debug: false,
    features: {
      aiAnalysis: true,
      platformIntegration: true,
      cicdGeneration: true
    }
  }
}

// Force production environment to always use production URLs
const environment = "production"

// Debug logging
console.log("Environment detection:", {
  REACT_APP_ENVIRONMENT: process.env.REACT_APP_ENVIRONMENT,
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  forcedEnvironment: environment
})

// Export current configuration
export const currentConfig = config[environment]

// Export API URL for easy access - always use production URL
export const API_URL =
  process.env.REACT_APP_API_URL || "https://api.repotorpedo.com"

// Debug logging
console.log("API URL resolved:", API_URL)

// Export environment info
export const ENVIRONMENT = currentConfig.environment
export const DEBUG = currentConfig.debug

// Export feature flags
export const FEATURES = currentConfig.features

// Export domain information
export const DOMAINS = {
  frontend: "repotorpedo.com",
  backend: "api.repotorpedo.com"
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
  const protocol = "https"
  const domain = DOMAINS[type]
  return `${protocol}://${domain}`
}

export default {
  API_URL,
  FRONTEND_URL: "https://repotorpedo.com",
  ENVIRONMENT,
  DEBUG,
  FEATURES,
  DOMAINS,
  getApiUrl,
  isFeatureEnabled,
  log,
  logError,
  getDomainUrl
}
