import React from "react"
import {
  Box,
  Typography,
  Button,
  Paper,
  IconButton,
  Tooltip
} from "@mui/material"
import { CheckCircle, ContentCopy, Share, Replay } from "@mui/icons-material"
import { useState } from "react"
import { addDeploymentToHistory } from "./DeploymentHistory"

const DeploySuccess = ({ siteUrl, onDeployAnother }) => {
  const [feedback, setFeedback] = useState(null)
  React.useEffect(() => {
    if (siteUrl) {
      addDeploymentToHistory({
        url: siteUrl,
        date: new Date().toLocaleString(),
        status: "Success"
      })
    }
  }, [siteUrl])
  const handleCopy = () => {
    navigator.clipboard.writeText(siteUrl)
  }
  const handleShare = () => {
    if (navigator.share) {
      navigator.share({ title: "My Deployed Site", url: siteUrl })
    } else {
      handleCopy()
      alert("Link copied! You can now share it.")
    }
  }
  return (
    <Paper sx={{ p: 4, textAlign: "center", mt: 6 }}>
      <CheckCircle sx={{ fontSize: 60, color: "#4caf50", mb: 2 }} />
      <Typography variant="h4" gutterBottom>
        Deployment Successful!
      </Typography>
      <Typography variant="body1" sx={{ mb: 3 }}>
        Your website is live at:
      </Typography>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mb: 2
        }}
      >
        <a
          href={siteUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            fontSize: 18,
            fontWeight: 600,
            color: "#1976d2",
            marginRight: 8
          }}
        >
          {siteUrl}
        </a>
        <Tooltip title="Copy link">
          <IconButton onClick={handleCopy}>
            <ContentCopy />
          </IconButton>
        </Tooltip>
        <Tooltip title="Share">
          <IconButton onClick={handleShare}>
            <Share />
          </IconButton>
        </Tooltip>
      </Box>
      <Button
        variant="outlined"
        startIcon={<Replay />}
        onClick={onDeployAnother}
        sx={{ mt: 2 }}
      >
        Deploy Another Site
      </Button>
      {/* Feedback prompt */}
      <Box sx={{ mt: 4 }}>
        {feedback === null ? (
          <>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Was this helpful?
            </Typography>
            <Button
              size="small"
              variant="contained"
              color="success"
              sx={{ mr: 1 }}
              onClick={() => setFeedback(true)}
            >
              Yes
            </Button>
            <Button
              size="small"
              variant="outlined"
              color="error"
              onClick={() => setFeedback(false)}
            >
              No
            </Button>
          </>
        ) : (
          <Typography variant="body2" color="text.secondary">
            Thank you for your feedback!
          </Typography>
        )}
      </Box>
    </Paper>
  )
}

export default DeploySuccess
