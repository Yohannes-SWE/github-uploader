import React, { useState, useEffect } from "react"
import {
  Container,
  Box,
  Typography,
  Button,
  TextField,
  Paper,
  Grid,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Chip,
  Divider,
  IconButton,
  Tooltip
} from "@mui/material"
import {
  GitHub,
  CloudUpload,
  Settings,
  Link,
  CheckCircle,
  Error,
  Info,
  Help,
  Launch,
  FolderOpen,
  Deploy,
  Security,
  Speed,
  Free
} from "@mui/icons-material"
import RenderDeploy from "./components/RenderDeploy"
import FileUpload from "./components/FileUpload"
import DeployWebsite from "./components/DeployWebsite"

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

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const response = await fetch("/api/auth/status")
      const data = await response.json()
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
    return (
      <Container maxWidth="md">
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="100vh"
          textAlign="center"
        >
          {/* Hero Section */}
          <Box sx={{ mb: 6 }}>
            <Typography
              variant="h2"
              gutterBottom
              sx={{ fontWeight: 700, color: "#1976d2" }}
            >
              Deploy Your Website
            </Typography>
            <Typography
              variant="h5"
              color="text.secondary"
              gutterBottom
              sx={{ mb: 3 }}
            >
              Get your website online in minutes, not hours
            </Typography>
            <Typography
              variant="body1"
              color="text.secondary"
              sx={{ maxWidth: 600, mx: "auto" }}
            >
              Upload your website files and we'll deploy them to the internet
              for free. No technical knowledge required - just drag, drop, and
              deploy!
            </Typography>
          </Box>

          {/* Benefits Cards */}
          <Grid container spacing={3} sx={{ mb: 6, maxWidth: 800 }}>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: "100%", textAlign: "center", p: 2 }}>
                <Speed sx={{ fontSize: 40, color: "#4caf50", mb: 1 }} />
                <Typography variant="h6" gutterBottom>
                  Fast & Easy
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Deploy in under 2 minutes with our guided process
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: "100%", textAlign: "center", p: 2 }}>
                <Free sx={{ fontSize: 40, color: "#ff9800", mb: 1 }} />
                <Typography variant="h6" gutterBottom>
                  100% Free
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Free hosting with 750 hours per month included
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ height: "100%", textAlign: "center", p: 2 }}>
                <Security sx={{ fontSize: 40, color: "#2196f3", mb: 1 }} />
                <Typography variant="h6" gutterBottom>
                  Secure & Reliable
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Automatic HTTPS, backups, and 99.9% uptime
                </Typography>
              </Card>
            </Grid>
          </Grid>

          {/* Login Section */}
          <Paper sx={{ p: 4, maxWidth: 400, width: "100%" }}>
            <Typography variant="h5" gutterBottom textAlign="center">
              Let's Get Started
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              textAlign="center"
              sx={{ mb: 3 }}
            >
              First, we'll connect to your GitHub account to store your website
              files
            </Typography>
            <Button
              variant="contained"
              size="large"
              fullWidth
              startIcon={<GitHub />}
              onClick={() => (window.location.href = "/api/auth/github/login")}
              sx={{
                py: 1.5,
                fontSize: "1.1rem",
                background: "linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)"
              }}
            >
              Continue with GitHub
            </Button>
            <Typography
              variant="caption"
              color="text.secondary"
              textAlign="center"
              sx={{ display: "block", mt: 2 }}
            >
              Don't have GitHub?{" "}
              <a
                href="https://github.com/join"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: "#1976d2" }}
              >
                Create a free account
              </a>
            </Typography>
          </Paper>

          {/* Help Section */}
          <Box sx={{ mt: 4, textAlign: "center" }}>
            <Button
              startIcon={<Help />}
              onClick={() => setShowHelp(!showHelp)}
              color="primary"
            >
              How does this work?
            </Button>
            {showHelp && (
              <Paper sx={{ p: 3, mt: 2, maxWidth: 600 }}>
                <Typography variant="h6" gutterBottom>
                  How It Works
                </Typography>
                <Box component="ol" sx={{ pl: 2 }}>
                  <Typography component="li" sx={{ mb: 1 }}>
                    <strong>Connect GitHub:</strong> We'll connect to your
                    GitHub account to store your website files
                  </Typography>
                  <Typography component="li" sx={{ mb: 1 }}>
                    <strong>Upload Files:</strong> Drag and drop your website
                    files (HTML, CSS, images, etc.)
                  </Typography>
                  <Typography component="li" sx={{ mb: 1 }}>
                    <strong>Connect Render:</strong> We'll help you connect to
                    Render for free hosting
                  </Typography>
                  <Typography component="li" sx={{ mb: 1 }}>
                    <strong>Deploy:</strong> Your website goes live with a
                    public URL in minutes!
                  </Typography>
                </Box>
              </Paper>
            )}
          </Box>
        </Box>
      </Container>
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
                  await fetch("/api/auth/logout", { method: "POST" })
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
            <RenderDeploy />
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
            <FileUpload />
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
            <DeployWebsite />
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
