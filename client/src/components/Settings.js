import React, { useState, useEffect } from "react"
import { Paper, Typography, TextField, Button, Box, Chip } from "@mui/material"

const Settings = () => {
  const [displayName, setDisplayName] = useState("")
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const name = localStorage.getItem("displayName") || ""
    setDisplayName(name)
  }, [])

  const handleSave = () => {
    localStorage.setItem("displayName", displayName)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  // Simulate connected accounts (replace with real auth status if available)
  const githubConnected = true
  const renderConnected = true

  return (
    <Paper sx={{ p: 4, mt: 6, maxWidth: 500, mx: "auto" }}>
      <Typography variant="h5" gutterBottom>
        Settings & Profile
      </Typography>
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1">Display Name</Typography>
        <TextField
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          size="small"
          sx={{ mt: 1, mr: 2 }}
        />
        <Button variant="contained" onClick={handleSave} sx={{ mt: 1 }}>
          Save
        </Button>
        {saved && <Chip label="Saved!" color="success" sx={{ ml: 2 }} />}
      </Box>
      <Box>
        <Typography variant="subtitle1" sx={{ mb: 1 }}>
          Connected Accounts
        </Typography>
        <Chip
          label="GitHub Connected"
          color={githubConnected ? "success" : "default"}
          sx={{ mr: 1 }}
        />
        <Chip
          label="Render Connected"
          color={renderConnected ? "success" : "default"}
        />
      </Box>
    </Paper>
  )
}

export default Settings
