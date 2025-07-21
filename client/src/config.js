// Optimized configuration with better tree shaking and performance
const isDevelopment = process.env.NODE_ENV === "development"
const isProduction = process.env.NODE_ENV === "production"

// Minimal config object to reduce bundle size
const baseConfig = {
  apiUrl: process.env.REACT_APP_API_URL || "https://api.repotorpedo.com",
  environment: process.env.NODE_ENV || "production",
  debug: isDevelopment,
  frontendUrl: "https://repotorpedo.com"
}

// Feature flags - only include what's needed
const features = {
  aiAnalysis: true,
  platformIntegration: true,
  cicdGeneration: true
}

// Domain configuration with lazy loading
const domainConfig = {
  api: "api.repotorpedo.com",
  frontend: "repotorpedo.com"
}

// Optimized environment detection - no console.log in production
if (isDevelopment) {
  console.log("Environment detection:", {
    NODE_ENV: process.env.NODE_ENV,
    REACT_APP_API_URL: process.env.REACT_APP_API_URL,
    API_URL: baseConfig.apiUrl
  })
}

// API URL resolution with caching
let cachedApiUrl = null
export const getApiUrl = () => {
  if (cachedApiUrl) return cachedApiUrl

  cachedApiUrl = isDevelopment ? "http://localhost:8000" : baseConfig.apiUrl

  return cachedApiUrl
}

// Feature flag checker with memoization
const featureCache = new Map()
export const isFeatureEnabled = (feature) => {
  if (featureCache.has(feature)) {
    return featureCache.get(feature)
  }

  const enabled = features[feature] === true
  featureCache.set(feature, enabled)
  return enabled
}

// Optimized logging - tree-shakeable in production
export const log = isDevelopment ? console.log : () => {}
export const logError = isProduction ? console.error : console.warn

// Domain helper with caching
let domainCache = null
export const getDomainUrl = (type = "frontend") => {
  if (domainCache) return domainCache[type]

  domainCache = {
    frontend: `https://${domainConfig.frontend}`,
    api: `https://${domainConfig.api}`
  }

  return domainCache[type]
}

// Export API URL for legacy compatibility
export const API_URL = getApiUrl()

// Export environment variables
export const ENVIRONMENT = baseConfig.environment
export const DEBUG = baseConfig.debug
export const FRONTEND_URL = baseConfig.frontendUrl

// Export features object
export const FEATURES = features

// Export domain config
export const DOMAINS = domainConfig

// Main config export - optimized for tree shaking
const configExport = {
  API_URL,
  FRONTEND_URL: baseConfig.frontendUrl,
  ENVIRONMENT: baseConfig.environment,
  DEBUG: baseConfig.debug,
  FEATURES: features,
  DOMAINS: domainConfig,
  getApiUrl,
  isFeatureEnabled,
  log,
  logError,
  getDomainUrl
}

export default configExport
