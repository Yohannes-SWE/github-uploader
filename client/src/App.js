import React, { useState, useEffect, Suspense, lazy } from "react"
import {
  Container,
  Box,
  Typography,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from "@mui/material"
import { GitHub, CloudUpload, Help, Launch } from "@mui/icons-material"
import { API_URL } from "./config"

// Lazy load heavy components for better performance
const RenderDeploy = lazy(() => import("./components/RenderDeploy"))
const FileUpload = lazy(() => import("./components/FileUpload"))
const DeployWebsite = lazy(() => import("./components/DeployWebsite"))
const AuthDebug = lazy(() => import("./components/AuthDebug"))
const LandingPage = lazy(() => import("./components/LandingPage"))

// Step Panel component
function StepPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`step-panel-${index}`}
      aria-labelledby={`step-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

function App() {
  const [currentStep, setCurrentStep] = useState(0)
  const [checkingAuth, setCheckingAuth] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [githubUsername, setGithubUsername] = useState("")
  const [showHelp, setShowHelp] = useState(false)
  const [showLanding, setShowLanding] = useState(true)
  const [onboardingStep, setOnboardingStep] = useState(0)
  const [helpOpen, setHelpOpen] = useState(false)

  useEffect(() => {
    checkAuthStatus()

    // Check if we're returning from OAuth callback
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get("auth") === "success") {
      const tempToken = urlParams.get("token")
      if (tempToken) {
        // Exchange temporary token for session
        exchangeTempToken(tempToken)
      }
      // Clear the URL parameters
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

  const handleNext = () => {
    setCurrentStep((prevStep) => prevStep + 1)
  }

  const handleBack = () => {
    setCurrentStep((prevStep) => prevStep - 1)
  }

  const handleStepClick = (step) => {
    setCurrentStep(step)
  }

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

  // Show debug page if URL contains /debug
  if (window.location.pathname === "/debug") {
    return (
      <Suspense fallback={<LoadingFallback message="Loading debug tools..." />}>
        <AuthDebug />
      </Suspense>
    )
  }

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

  if (!isAuthenticated) {
    if (showLanding) {
      return (
        <Suspense
          fallback={<LoadingFallback message="Loading landing page..." />}
        >
          <LandingPage onGetStarted={() => setShowLanding(false)} />
        </Suspense>
      )
    }
    // Onboarding wizard for unauthenticated users
    return (
      <>
        <Container maxWidth="sm">
          <Box sx={{ mt: 6 }}>
            <Stepper
              activeStep={onboardingStep}
              alternativeLabel
              sx={{ mb: 4 }}
            >
              <Step>
                <StepLabel>Connect GitHub</StepLabel>
              </Step>
              <Step>
                <StepLabel>Connect Render</StepLabel>
              </Step>
              <Step>
                <StepLabel>Upload Files</StepLabel>
              </Step>
              <Step>
                <StepLabel>Deploy</StepLabel>
              </Step>
            </Stepper>
            {onboardingStep === 0 && (
              <Paper sx={{ p: 4, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                  Step 1: Connect GitHub
                </Typography>
                <Typography
                  variant="body1"
                  color="text.secondary"
                  sx={{ mb: 3 }}
                >
                  We'll connect to your GitHub account to store your website
                  files. No technical knowledge required.
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<GitHub />}
                  onClick={() =>
                    (window.location.href = `${API_URL}/api/auth/github/login`)
                  }
                  sx={{ py: 1.5, fontSize: "1.1rem" }}
                >
                  Continue with GitHub
                </Button>
              </Paper>
            )}
            {onboardingStep === 1 && (
              <Paper sx={{ p: 4, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                  Step 2: Connect Render
                </Typography>
                <Typography
                  variant="body1"
                  color="text.secondary"
                  sx={{ mb: 3 }}
                >
                  Connect your Render account for free hosting. This is where
                  your website will live on the internet.
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<CloudUpload />}
                  onClick={() => setOnboardingStep(2)}
                  sx={{ py: 1.5, fontSize: "1.1rem" }}
                >
                  Connect Render
                </Button>
              </Paper>
            )}
            {onboardingStep === 2 && (
              <Paper sx={{ p: 4, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                  Step 3: Upload Files
                </Typography>
                <Typography
                  variant="body1"
                  color="text.secondary"
                  sx={{ mb: 3 }}
                >
                  Drag and drop your website files (HTML, CSS, images, etc.)
                  below.
                </Typography>
                <FileUpload onUploadComplete={() => setOnboardingStep(3)} />
              </Paper>
            )}
            {onboardingStep === 3 && (
              <Paper sx={{ p: 4, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                  Step 4: Deploy
                </Typography>
                <Typography
                  variant="body1"
                  color="text.secondary"
                  sx={{ mb: 3 }}
                >
                  You're ready to deploy! Click below to launch your website to
                  the world.
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<Launch />}
                  onClick={() => window.location.reload()}
                  sx={{ py: 1.5, fontSize: "1.1rem" }}
                >
                  Deploy Now
                </Button>
              </Paper>
            )}
          </Box>
        </Container>
        <Button
          variant="text"
          color="primary"
          sx={{ mt: 2, ml: 2 }}
          onClick={() => setHelpOpen(true)}
        >
          Help / FAQ
        </Button>
        <Dialog open={helpOpen} onClose={() => setHelpOpen(false)}>
          <DialogTitle>Help & FAQ</DialogTitle>
          <DialogContent dividers>
            <Typography variant="h6" gutterBottom>
              What is Render?
            </Typography>
            <Typography variant="body2" gutterBottom>
              Render is a modern cloud platform that lets you deploy websites
              and apps easily, with free hosting for static sites.
            </Typography>
            <Typography variant="h6" gutterBottom>
              Is my data safe?
            </Typography>
            <Typography variant="body2" gutterBottom>
              Yes! Your credentials are never shared, and all deployments use
              secure OAuth authentication. Files are only used for your
              deployment.
            </Typography>
            <Typography variant="h6" gutterBottom>
              How do I get support?
            </Typography>
            <Typography variant="body2">
              Email{" "}
              <a href="mailto:support@repotorpedo.com">
                support@repotorpedo.com
              </a>{" "}
              or use the feedback form in the app.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setHelpOpen(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </>
    )
  }

  // Main app after authentication
  return (
    <Container maxWidth="lg">
      <Box sx={{ width: "100%", mt: 3 }}>
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2
            }}
          >
            <Box>
              <Typography
                variant="h3"
                gutterBottom
                sx={{ fontWeight: 700, color: "#1976d2" }}
              >
                Deploy Your Website
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Welcome back, {githubUsername}! Let's get your website online.
              </Typography>
            </Box>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Tooltip title="Help">
                <IconButton onClick={() => setShowHelp(!showHelp)}>
                  <Help />
                </IconButton>
              </Tooltip>
              <Button
                variant="outlined"
                onClick={async () => {
                  await fetch(`${API_URL}/api/auth/logout`, {
                    method: "POST",
                    credentials: "include"
                  })
                  setIsAuthenticated(false)
                }}
              >
                Logout
              </Button>
            </Box>
          </Box>

          {/* Progress Stepper */}
          <Stepper activeStep={currentStep} alternativeLabel sx={{ mb: 4 }}>
            <Step>
              <StepLabel
                StepIconProps={{
                  onClick: () => handleStepClick(0),
                  sx: { cursor: "pointer" }
                }}
              >
                Connect Render
              </StepLabel>
            </Step>
            <Step>
              <StepLabel
                StepIconProps={{
                  onClick: () => handleStepClick(1),
                  sx: { cursor: "pointer" }
                }}
              >
                Upload Files
              </StepLabel>
            </Step>
            <Step>
              <StepLabel
                StepIconProps={{
                  onClick: () => handleStepClick(2),
                  sx: { cursor: "pointer" }
                }}
              >
                Deploy Website
              </StepLabel>
            </Step>
          </Stepper>
        </Box>

        {/* Help Section */}
        {showHelp && (
          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Guide
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              <strong>Step 1:</strong> Connect your Render account for free
              hosting
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              <strong>Step 2:</strong> Upload your website files (HTML, CSS,
              images, etc.)
            </Typography>
            <Typography variant="body2">
              <strong>Step 3:</strong> Deploy and get your live website URL
            </Typography>
          </Alert>
        )}

        {/* Step Content */}
        <StepPanel value={currentStep} index={0}>
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Step 1: Connect Your Hosting Account
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              We'll connect to Render to host your website for free. This is
              where your website will live on the internet.
            </Typography>
            <Suspense
              fallback={
                <LoadingFallback message="Loading deployment tools..." />
              }
            >
              <RenderDeploy />
            </Suspense>
          </Paper>
        </StepPanel>

        <StepPanel value={currentStep} index={1}>
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Step 2: Upload Your Website Files
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Drag and drop your website files here. We support HTML, CSS,
              JavaScript, images, and more.
            </Typography>
            <Suspense
              fallback={<LoadingFallback message="Loading file upload..." />}
            >
              <FileUpload />
            </Suspense>
          </Paper>
        </StepPanel>

        <StepPanel value={currentStep} index={2}>
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Step 3: Deploy Your Website
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Click deploy to make your website live on the internet. You'll get
              a public URL to share with others.
            </Typography>
            <Suspense
              fallback={<LoadingFallback message="Loading website deploy..." />}
            >
              <DeployWebsite />
            </Suspense>
          </Paper>
        </StepPanel>

        {/* Navigation */}
        <Box sx={{ display: "flex", justifyContent: "space-between", mt: 4 }}>
          <Button
            disabled={currentStep === 0}
            onClick={handleBack}
            sx={{ mr: 1 }}
          >
            Back
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={currentStep === 2}
          >
            {currentStep === 2 ? "Finish" : "Next"}
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

export default App
