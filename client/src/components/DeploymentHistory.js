import React, { useEffect, useState } from "react"
import {
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  Box,
  Link as MuiLink,
  Button
} from "@mui/material"

const getHistory = () => {
  const data = localStorage.getItem("deploymentHistory")
  return data ? JSON.parse(data) : []
}

export const addDeploymentToHistory = (deployment) => {
  const history = getHistory()
  localStorage.setItem(
    "deploymentHistory",
    JSON.stringify([deployment, ...history])
  )
}

const DeploymentHistory = () => {
  const [deployments, setDeployments] = useState(getHistory())

  useEffect(() => {
    setDeployments(getHistory())
  }, [])

  const handleExport = () => {
    const dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(deployments, null, 2))
    const downloadAnchorNode = document.createElement("a")
    downloadAnchorNode.setAttribute("href", dataStr)
    downloadAnchorNode.setAttribute("download", "deployment_history.json")
    document.body.appendChild(downloadAnchorNode)
    downloadAnchorNode.click()
    downloadAnchorNode.remove()
  }

  const handleImport = (e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (event) => {
      try {
        const imported = JSON.parse(event.target.result)
        if (Array.isArray(imported)) {
          localStorage.setItem("deploymentHistory", JSON.stringify(imported))
          setDeployments(imported)
        }
      } catch (err) {
        alert("Invalid file format.")
      }
    }
    reader.readAsText(file)
  }

  return (
    <Paper sx={{ p: 4, mt: 6 }}>
      <Typography variant="h5" gutterBottom>
        Deployment History
      </Typography>
      <Box sx={{ mb: 2 }}>
        <Button variant="outlined" sx={{ mr: 2 }} onClick={handleExport}>
          Export History
        </Button>
        <Button variant="outlined" component="label">
          Import History
          <input
            type="file"
            accept="application/json"
            hidden
            onChange={handleImport}
          />
        </Button>
      </Box>
      <List>
        {deployments.length === 0 && (
          <ListItem>
            <ListItemText primary="No deployments yet." />
          </ListItem>
        )}
        {deployments.map((deploy, idx) => (
          <ListItem key={idx} divider>
            <ListItemText
              primary={
                <MuiLink
                  href={deploy.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {deploy.url}
                </MuiLink>
              }
              secondary={deploy.date}
            />
            <Box>
              <Chip
                label={deploy.status}
                color={deploy.status === "Success" ? "success" : "error"}
              />
            </Box>
          </ListItem>
        ))}
      </List>
    </Paper>
  )
}

export default DeploymentHistory
