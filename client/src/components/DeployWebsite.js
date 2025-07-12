import React, { useState } from "react"
import {
  Box,
  Typography,
  Button,
  Paper,
  Alert,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider
} from "@mui/material"
import {
  Launch,
  CheckCircle,
  Error,
  Schedule,
  Security,
  Speed,
  Link,
  ContentCopy
} from "@mui/icons-material"

const DeployWebsite = () => {
  const [deploying, setDeploying] = useState(false)
  const [deployProgress, setDeployProgress] = useState(0)
  const [deployStatus, setDeployStatus] = useState("ready") // ready, deploying, success, error
  const [websiteUrl, setWebsiteUrl] = useState("")

  const handleDeploy = async () => {
    setDeploying(true)
    setDeployStatus("deploying")
    setDeployProgress(0)

    try {
      // Simulate deployment progress
      const steps = [
        { progress: 20, message: "Preparing your files..." },
        { progress: 40, message: "Uploading to hosting..." },
        { progress: 60, message: "Configuring your website..." },
        { progress: 80, message: "Setting up security..." },
        { progress: 95, message: "Finalizing deployment..." },
        { progress: 100, message: "Your website is live!" }
      ]

      for (const step of steps) {
        setDeployProgress(step.progress)
        await new Promise((resolve) => setTimeout(resolve, 1000))
      }

      // Simulate successful deployment
      setDeployStatus("success")
      setWebsiteUrl("https://your-website-name.onrender.com")
    } catch (error) {
      console.error("Deployment failed:", error)
      setDeployStatus("error")
    } finally {
      setDeploying(false)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(websiteUrl)
  }

  const getStatusMessage = () => {
    switch (deployStatus) {
      case "ready":
        return "Ready to deploy your website to the internet"
      case "deploying":
        return "Deploying your website... This usually takes 1-2 minutes"
      case "success":
        return "🎉 Your website is now live on the internet!"
      case "error":
        return "Something went wrong. Please try again."
      default:
        return ""
    }
  }

  const getStatusColor = () => {
    switch (deployStatus) {
      case "ready":
        return "info"
      case "deploying":
        return "info"
      case "success":
        return "success"
      case "error":
        return "error"
      default:
        return "info"
    }
  }

  return (
    <Box>
      {/* Deployment Status */}
      <Alert severity={getStatusColor()} sx={{ mb: 3 }}>
        <Typography variant="body1">{getStatusMessage()}</Typography>
      </Alert>

      {/* Deployment Progress */}
      {deploying && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Deploying Your Website
          </Typography>
          <LinearProgress
            variant="determinate"
            value={deployProgress}
            sx={{ mb: 2, height: 8, borderRadius: 4 }}
          />
          <Typography variant="body2" color="text.secondary">
            {deployProgress}% complete
          </Typography>
        </Paper>
      )}

      {/* Success State */}
      {deployStatus === "success" && (
        <Paper sx={{ p: 4, mb: 3, textAlign: "center" }}>
          <CheckCircle sx={{ fontSize: 80, color: "#4caf50", mb: 2 }} />
          <Typography variant="h4" gutterBottom sx={{ color: "#4caf50" }}>
            Website Deployed Successfully!
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Your website is now live and accessible to anyone on the internet
          </Typography>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 2,
              mb: 3
            }}
          >
            <Typography variant="h6">Your Website URL:</Typography>
            <Chip
              label={websiteUrl}
              variant="outlined"
              icon={<Link />}
              sx={{ fontSize: "1rem", py: 1 }}
            />
            <Button
              variant="outlined"
              startIcon={<ContentCopy />}
              onClick={copyToClipboard}
              size="small"
            >
              Copy
            </Button>
          </Box>

          <Box sx={{ display: "flex", gap: 2, justifyContent: "center" }}>
            <Button
              variant="contained"
              startIcon={<Launch />}
              href={websiteUrl}
              target="_blank"
              rel="noopener noreferrer"
              size="large"
            >
              Visit Website
            </Button>
            <Button
              variant="outlined"
              onClick={() => window.location.reload()}
              size="large"
            >
              Deploy Another
            </Button>
          </Box>
        </Paper>
      )}

      {/* Error State */}
      {deployStatus === "error" && (
        <Paper sx={{ p: 4, mb: 3, textAlign: "center" }}>
          <Error sx={{ fontSize: 80, color: "#f44336", mb: 2 }} />
          <Typography variant="h5" gutterBottom sx={{ color: "#f44336" }}>
            Deployment Failed
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Something went wrong during deployment. Please try again.
          </Typography>
          <Button
            variant="contained"
            onClick={() => {
              setDeployStatus("ready")
              setDeployProgress(0)
            }}
            size="large"
          >
            Try Again
          </Button>
        </Paper>
      )}

      {/* Ready State */}
      {deployStatus === "ready" && (
        <Paper sx={{ p: 4, mb: 3, textAlign: "center" }}>
          <Launch sx={{ fontSize: 80, color: "#1976d2", mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            Ready to Deploy
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Click the button below to make your website live on the internet
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<Launch />}
            onClick={handleDeploy}
            disabled={deploying}
            sx={{
              py: 1.5,
              fontSize: "1.1rem",
              background: "linear-gradient(45deg, #4caf50 30%, #66bb6a 90%)"
            }}
          >
            Deploy Website
          </Button>
        </Paper>
      )}

      {/* What Happens Next */}
      <Paper sx={{ p: 3, backgroundColor: "#f8f9fa" }}>
        <Typography variant="h6" gutterBottom>
          What happens when you deploy?
        </Typography>
        <List>
          <ListItem>
            <ListItemIcon>
              <Speed color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Fast Deployment"
              secondary="Your website goes live in 1-2 minutes"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Security color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Automatic Security"
              secondary="HTTPS encryption and security headers"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Link color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Public URL"
              secondary="Get a shareable link to your website"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Schedule color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Always Online"
              secondary="Your website stays up 24/7"
            />
          </ListItem>
        </List>
      </Paper>

      {/* Tips */}
      <Paper sx={{ p: 3, mt: 3, backgroundColor: "#e3f2fd" }}>
        <Typography variant="h6" gutterBottom>
          💡 Pro Tips
        </Typography>
        <Box component="ul" sx={{ pl: 2, m: 0 }}>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Share your URL:</strong> Send the link to friends, family,
            or clients
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Update anytime:</strong> Upload new files to update your
            website
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Free hosting:</strong> Your website stays online for free
          </Typography>
          <Typography component="li" variant="body2">
            <strong>No technical knowledge needed:</strong> We handle all the
            complex stuff
          </Typography>
        </Box>
      </Paper>
    </Box>
  )
}

export default DeployWebsite
