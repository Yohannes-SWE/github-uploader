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
  Tabs,
  Tab,
  Chip
} from "@mui/material"
import { CloudUpload, GitHub, Settings, Link } from "@mui/icons-material"
import PlatformConnector from "./components/PlatformConnector"

// Tab Panel component
function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

function App() {
  const [tabValue, setTabValue] = useState(0)
  const [checkingAuth, setCheckingAuth] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [githubUsername, setGithubUsername] = useState("")
  const [files, setFiles] = useState([])
  const [repoName, setRepoName] = useState("")
  const [commitMessage, setCommitMessage] = useState("Initial commit")
  const [selectedPlatform, setSelectedPlatform] = useState("")
  const [cicdPlatform, setCicdPlatform] = useState("github-actions")
  const [projectType, setProjectType] = useState("auto")
  const [aiSuggestions, setAiSuggestions] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStatus, setUploadStatus] = useState("")
  const [uploadResult, setUploadResult] = useState(null)
  const [connectedPlatforms, setConnectedPlatforms] = useState([])

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

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  const handlePlatformConnected = (platform) => {
    setConnectedPlatforms((prev) => [...prev, platform])
  }

  if (checkingAuth) {
    return (
      <Container maxWidth="md">
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
        >
          <CircularProgress />
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
        >
          <Typography variant="h3" gutterBottom>
            GitHub Uploader
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Upload projects to GitHub with AI assistance and CI/CD automation
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<GitHub />}
            onClick={() => (window.location.href = "/api/auth/github/login")}
            sx={{ mt: 3 }}
          >
            Login with GitHub
          </Button>
        </Box>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: "100%", mt: 3 }}>
        <Typography variant="h4" gutterBottom>
          GitHub Uploader
        </Typography>
        <Typography variant="body1" color="text.secondary" gutterBottom>
          Welcome, {githubUsername}! Connect platforms and upload your projects.
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: "divider", mt: 3 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="main tabs"
          >
            <Tab label="Upload Project" icon={<CloudUpload />} />
            <Tab label="Platform Connections" icon={<Link />} />
            <Tab label="Settings" icon={<Settings />} />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          {/* Upload Project Tab */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              {/* Existing upload functionality */}
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Upload Project
                </Typography>
                {/* Your existing upload form components */}
              </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
              {/* Connected Platforms Summary */}
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Connected Platforms
                </Typography>
                {connectedPlatforms.length > 0 ? (
                  <Box>
                    {connectedPlatforms.map((platform) => (
                      <Chip
                        key={platform}
                        label={platform}
                        color="success"
                        sx={{ mr: 1, mb: 1 }}
                      />
                    ))}
                  </Box>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No platforms connected yet. Connect platforms to enable
                    automatic deployment.
                  </Typography>
                )}
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {/* Platform Connections Tab */}
          <PlatformConnector onPlatformConnected={handlePlatformConnected} />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          {/* Settings Tab */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Settings
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage your account settings and preferences.
            </Typography>
            <Button
              variant="outlined"
              onClick={async () => {
                await fetch("/api/auth/logout", { method: "POST" })
                setIsAuthenticated(false)
              }}
              sx={{ mt: 2 }}
            >
              Logout
            </Button>
          </Paper>
        </TabPanel>
      </Box>
    </Container>
  )
}

export default App
