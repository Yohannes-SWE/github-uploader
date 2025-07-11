import React, { useState, useEffect } from "react"
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from "@mui/material"
import {
  CheckCircle,
  Cancel,
  Link,
  Settings,
  CloudUpload,
  Code
} from "@mui/icons-material"

const PlatformConnector = ({ onPlatformConnected }) => {
  const [platforms, setPlatforms] = useState({})
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState(false)
  const [setupDialog, setSetupDialog] = useState({
    open: false,
    platform: null
  })
  const [setupConfig, setSetupConfig] = useState({})

  const platformConfigs = {
    vercel: {
      name: "Vercel",
      description: "Frontend hosting and deployment",
      icon: "🚀",
      color: "#000000",
      features: [
        "Automatic deployments",
        "Preview deployments",
        "Edge functions"
      ]
    },
    railway: {
      name: "Railway",
      description: "Full-stack hosting platform",
      icon: "🚂",
      color: "#0B0D0E",
      features: ["Database hosting", "Auto-scaling", "Custom domains"]
    },
    netlify: {
      name: "Netlify",
      description: "Static site hosting",
      icon: "🌐",
      color: "#00AD9F",
      features: ["Form handling", "Functions", "CDN"]
    },
    heroku: {
      name: "Heroku",
      description: "Platform-as-a-Service",
      icon: "💜",
      color: "#430098",
      features: ["Add-ons", "Auto-scaling", "Git integration"]
    },
    circleci: {
      name: "CircleCI",
      description: "CI/CD platform",
      icon: "⭕",
      color: "#343434",
      features: ["Parallel jobs", "Docker support", "Orbs"]
    },
    travis: {
      name: "Travis CI",
      description: "Continuous integration",
      icon: "🔧",
      color: "#3EAAAF",
      features: ["GitHub integration", "Matrix builds", "Deployment"]
    },
    github: {
      name: "GitHub",
      description: "Code hosting and collaboration",
      icon: "🐙",
      color: "#181717",
      features: ["Issues", "Pull requests", "Actions"]
    }
  }

  useEffect(() => {
    fetchPlatformStatus()
  }, [])

  const fetchPlatformStatus = async () => {
    try {
      const response = await fetch("/api/platforms/status")
      if (response.ok) {
        const data = await response.json()
        setPlatforms(data)
      }
    } catch (error) {
      console.error("Failed to fetch platform status:", error)
    } finally {
      setLoading(false)
    }
  }

  const connectPlatform = async (platform) => {
    setConnecting(true)
    try {
      const response = await fetch(`/api/platforms/connect/${platform}`)
      if (response.ok) {
        const data = await response.json()
        // Open OAuth window
        const authWindow = window.open(
          data.auth_url,
          `${platform}_oauth`,
          "width=600,height=700,scrollbars=yes,resizable=yes"
        )

        // Poll for window close and check connection
        const checkClosed = setInterval(() => {
          if (authWindow.closed) {
            clearInterval(checkClosed)
            fetchPlatformStatus()
            if (onPlatformConnected) {
              onPlatformConnected(platform)
            }
          }
        }, 1000)
      }
    } catch (error) {
      console.error(`Failed to connect to ${platform}:`, error)
    } finally {
      setConnecting(false)
    }
  }

  const disconnectPlatform = async (platform) => {
    try {
      await fetch(`/api/platforms/disconnect/${platform}`, { method: "POST" })
      fetchPlatformStatus()
    } catch (error) {
      console.error(`Failed to disconnect from ${platform}:`, error)
    }
  }

  const openSetupDialog = (platform) => {
    setSetupDialog({ open: true, platform })
    setSetupConfig({
      name: "",
      description: "",
      framework: "other",
      public: false,
      region: "us"
    })
  }

  const setupPlatform = async () => {
    try {
      const response = await fetch(
        `/api/platforms/setup/${setupDialog.platform}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(setupConfig)
        }
      )

      if (response.ok) {
        const result = await response.json()
        alert(`${platformConfigs[setupDialog.platform].name} setup successful!`)
        setSetupDialog({ open: false, platform: null })
      }
    } catch (error) {
      console.error("Failed to setup platform:", error)
      alert("Failed to setup platform. Please try again.")
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Platform Connections
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Connect your accounts to enable automatic deployment and CI/CD setup
      </Typography>

      <Grid container spacing={3}>
        {Object.entries(platformConfigs).map(([key, config]) => {
          const isConnected = platforms[key]?.connected

          return (
            <Grid item xs={12} sm={6} md={4} key={key}>
              <Card
                sx={{
                  height: "100%",
                  border: isConnected
                    ? `2px solid ${config.color}`
                    : "2px solid transparent",
                  transition: "all 0.3s ease"
                }}
              >
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Typography variant="h4" mr={1}>
                      {config.icon}
                    </Typography>
                    <Box flex={1}>
                      <Typography variant="h6">{config.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {config.description}
                      </Typography>
                    </Box>
                    <Chip
                      icon={isConnected ? <CheckCircle /> : <Cancel />}
                      label={isConnected ? "Connected" : "Disconnected"}
                      color={isConnected ? "success" : "default"}
                      size="small"
                    />
                  </Box>

                  <Box mb={2}>
                    {config.features.map((feature, index) => (
                      <Chip
                        key={index}
                        label={feature}
                        size="small"
                        variant="outlined"
                        sx={{ mr: 0.5, mb: 0.5 }}
                      />
                    ))}
                  </Box>

                  {isConnected && (
                    <Box mb={2}>
                      <Typography variant="body2" color="text.secondary">
                        Connected as: {platforms[key]?.username || "Unknown"}
                      </Typography>
                    </Box>
                  )}

                  <Box display="flex" gap={1}>
                    {!isConnected ? (
                      <Button
                        variant="contained"
                        startIcon={<Link />}
                        onClick={() => connectPlatform(key)}
                        disabled={connecting}
                        fullWidth
                        sx={{ backgroundColor: config.color }}
                      >
                        {connecting ? "Connecting..." : "Connect"}
                      </Button>
                    ) : (
                      <>
                        <Button
                          variant="outlined"
                          startIcon={<Settings />}
                          onClick={() => openSetupDialog(key)}
                          fullWidth
                        >
                          Setup
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => disconnectPlatform(key)}
                          size="small"
                        >
                          Disconnect
                        </Button>
                      </>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )
        })}
      </Grid>

      {/* Setup Dialog */}
      <Dialog
        open={setupDialog.open}
        onClose={() => setSetupDialog({ open: false, platform: null })}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Setup{" "}
          {setupDialog.platform && platformConfigs[setupDialog.platform]?.name}
        </DialogTitle>
        <DialogContent>
          <Box mt={2}>
            <TextField
              label="Project Name"
              value={setupConfig.name}
              onChange={(e) =>
                setSetupConfig({ ...setupConfig, name: e.target.value })
              }
              fullWidth
              margin="normal"
            />
            <TextField
              label="Description"
              value={setupConfig.description}
              onChange={(e) =>
                setSetupConfig({ ...setupConfig, description: e.target.value })
              }
              fullWidth
              margin="normal"
              multiline
              rows={2}
            />
            {setupDialog.platform === "vercel" && (
              <FormControl fullWidth margin="normal">
                <InputLabel>Framework</InputLabel>
                <Select
                  value={setupConfig.framework}
                  onChange={(e) =>
                    setSetupConfig({
                      ...setupConfig,
                      framework: e.target.value
                    })
                  }
                >
                  <MenuItem value="nextjs">Next.js</MenuItem>
                  <MenuItem value="react">React</MenuItem>
                  <MenuItem value="vue">Vue.js</MenuItem>
                  <MenuItem value="angular">Angular</MenuItem>
                  <MenuItem value="nuxt">Nuxt.js</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </Select>
              </FormControl>
            )}
            {setupDialog.platform === "heroku" && (
              <FormControl fullWidth margin="normal">
                <InputLabel>Region</InputLabel>
                <Select
                  value={setupConfig.region}
                  onChange={(e) =>
                    setSetupConfig({ ...setupConfig, region: e.target.value })
                  }
                >
                  <MenuItem value="us">United States</MenuItem>
                  <MenuItem value="eu">Europe</MenuItem>
                  <MenuItem value="au">Australia</MenuItem>
                </Select>
              </FormControl>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setSetupDialog({ open: false, platform: null })}
          >
            Cancel
          </Button>
          <Button onClick={setupPlatform} variant="contained">
            Setup Project
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default PlatformConnector
