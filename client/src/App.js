import React, { useState, useEffect, Suspense, lazy } from "react"
import { Container, Box, Typography, CircularProgress } from "@mui/material"
import { API_URL } from "./config"

// Lazy load components for better performance
const LandingPage = lazy(() => import("./components/LandingPage"))
const RenderDeploy = lazy(() => import("./components/RenderDeploy"))
const FileUpload = lazy(() => import("./components/FileUpload"))
const DeployWebsite = lazy(() => import("./components/DeployWebsite"))
const AuthDebug = lazy(() => import("./components/AuthDebug"))

function App() {
  const [checkingAuth, setCheckingAuth] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [githubUsername, setGithubUsername] = useState("")

  // Loading component for Suspense fallback
  const LoadingFallback = ({ message = "Loading..." }) => (
    <Container maxWidth="md">
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="50vh"
        textAlign="center"
      >
        <CircularProgress size={40} sx={{ mb: 2 }} />
        <Typography variant="body2" color="text.secondary">
          {message}
        </Typography>
      </Box>
    </Container>
  )

  useEffect(() => {
    checkAuthStatus()

    // Check if we're returning from OAuth callback
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get("auth") === "success") {
      const tempToken = urlParams.get("token")
      if (tempToken) {
        exchangeTempToken(tempToken)
      }
      window.history.replaceState({}, document.title, window.location.pathname)
    }
  }, [])

  const exchangeTempToken = async (tempToken) => {
    try {
      console.log("Exchanging temporary token...")
      const response = await fetch(`${API_URL}/api/auth/exchange-token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ temp_token: tempToken })
      })

      if (response.ok) {
        const data = await response.json()
        console.log("Token exchange successful:", data)
        setIsAuthenticated(data.authenticated)
        setGithubUsername(data.username || "")
      } else {
        console.error("Token exchange failed")
        const errorData = await response.json()
        console.error("Error:", errorData)
      }
    } catch (error) {
      console.error("Token exchange error:", error)
    }
  }

  const checkAuthStatus = async () => {
    try {
      console.log("Checking auth status...")
      const response = await fetch(`${API_URL}/api/auth/status`, {
        credentials: "include"
      })
      const data = await response.json()
      console.log("Auth status response:", data)
      setIsAuthenticated(data.authenticated)
      setGithubUsername(data.username || "")
    } catch (error) {
      console.error("Auth check failed:", error)
    } finally {
      setCheckingAuth(false)
    }
  }

  // Show debug page if URL contains /debug
  if (window.location.pathname === "/debug") {
    return (
      <Suspense fallback={<LoadingFallback message="Loading debug tools..." />}>
        <AuthDebug />
      </Suspense>
    )
  }

  // Show loading while checking authentication
  if (checkingAuth) {
    return (
      <Container maxWidth="md">
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
          textAlign="center"
        >
          <CircularProgress size={60} sx={{ mb: 3 }} />
          <Typography variant="h6" color="text.secondary">
            Loading your workspace...
          </Typography>
        </Box>
      </Container>
    )
  }

  // Show modern landing page for unauthenticated users
  if (!isAuthenticated) {
    return (
      <Suspense
        fallback={<LoadingFallback message="Loading landing page..." />}
      >
        <LandingPage
          onGetStarted={() => {
            // When user clicks get started, we can redirect to auth or show next step
            console.log("User clicked get started!")
          }}
        />
      </Suspense>
    )
  }

  // Show authenticated dashboard
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Welcome to RepoTorpedo
        </Typography>
        <Typography variant="body1" sx={{ mb: 4 }}>
          Authenticated as: {githubUsername}
        </Typography>

        <Box sx={{ display: "grid", gap: 4 }}>
          <Suspense
            fallback={<LoadingFallback message="Loading deployment tools..." />}
          >
            <RenderDeploy />
          </Suspense>

          <Suspense
            fallback={<LoadingFallback message="Loading file upload..." />}
          >
            <FileUpload />
          </Suspense>

          <Suspense
            fallback={<LoadingFallback message="Loading website deploy..." />}
          >
            <DeployWebsite />
          </Suspense>
        </Box>
      </Box>
    </Container>
  )
}

export default App
