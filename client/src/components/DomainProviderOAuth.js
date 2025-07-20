import React, { useState, useEffect } from "react"
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Alert,
  CircularProgress,
  Chip,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from "@mui/material"
import {
  Cloud,
  Security,
  CheckCircle,
  Error,
  Launch,
  Domain,
  Key,
  AccountCircle
} from "@mui/icons-material"
import { API_URL } from "../config"

const DomainProviderOAuth = ({ onProviderConnected }) => {
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState(false)
  const [error, setError] = useState(null)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedProvider, setSelectedProvider] = useState(null)

  useEffect(() => {
    loadProviders()
  }, [])

  const loadProviders = async () => {
    try {
      setLoading(true)
      const response = await fetch(
        `${API_URL}/api/domain-providers/supported`,
        {
          credentials: "include"
        }
      )

      if (response.ok) {
        const data = await response.json()
        setProviders(data.providers)
      } else {
        setError("Failed to load domain providers")
      }
    } catch (err) {
      setError("Network error loading providers")
    } finally {
      setLoading(false)
    }
  }

  const handleOAuthLogin = async (provider) => {
    try {
      setConnecting(true)
      setError(null)

      // Initiate OAuth flow
      const response = await fetch(
        `${API_URL}/api/domain-providers/oauth/login/${provider}`,
        {
          credentials: "include"
        }
      )

      if (response.ok) {
        const data = await response.json()

        // Open OAuth popup
        const popup = window.open(
          data.auth_url,
          `${provider}_oauth`,
          "width=600,height=700,scrollbars=yes,resizable=yes"
        )

        // Poll for popup closure and check for success
        const checkClosed = setInterval(() => {
          if (popup.closed) {
            clearInterval(checkClosed)
            setConnecting(false)

            // Reload providers to show updated status
            loadProviders()

            // Notify parent component
            if (onProviderConnected) {
              onProviderConnected(provider)
            }
          }
        }, 1000)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || "Failed to initiate OAuth login")
        setConnecting(false)
      }
    } catch (err) {
      setError("Network error during OAuth login")
      setConnecting(false)
    }
  }

  const handleApiKeyConnect = (provider) => {
    setSelectedProvider(provider)
    setShowDetails(true)
  }

  const getProviderIcon = (providerName) => {
    const icons = {
      godaddy: <Domain />,
      cloudflare: <Cloud />,
      namecheap: <Key />,
      squarespace: <AccountCircle />
    }
    return icons[providerName] || <Domain />
  }

  const getAuthMethodColor = (authMethod) => {
    return authMethod === "oauth" ? "success" : "primary"
  }

  const getAuthMethodLabel = (authMethod) => {
    return authMethod === "oauth" ? "OAuth Login" : "API Key"
  }

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="200px"
      >
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Connect Domain Providers
      </Typography>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Connect your domain provider accounts to automatically configure DNS
        records during deployment. OAuth login is recommended for a seamless
        experience.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {providers.map((provider) => (
          <Grid item xs={12} sm={6} md={4} key={provider.name}>
            <Card
              sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                position: "relative"
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box display="flex" alignItems="center" mb={2}>
                  {getProviderIcon(provider.name)}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    {provider.display_name}
                  </Typography>
                </Box>

                <Box mb={2}>
                  <Chip
                    label={getAuthMethodLabel(provider.auth_method)}
                    color={getAuthMethodColor(provider.auth_method)}
                    size="small"
                    icon={
                      provider.auth_method === "oauth" ? <Security /> : <Key />
                    }
                  />
                </Box>

                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 2 }}
                >
                  {provider.features?.slice(0, 3).join(", ")}
                  {provider.features?.length > 3 && "..."}
                </Typography>

                <Box sx={{ mt: "auto" }}>
                  {provider.auth_method === "oauth" ? (
                    <Button
                      variant="contained"
                      color="primary"
                      fullWidth
                      onClick={() => handleOAuthLogin(provider.name)}
                      disabled={connecting}
                      startIcon={
                        connecting ? <CircularProgress size={16} /> : <Launch />
                      }
                    >
                      {connecting ? "Connecting..." : "Login with OAuth"}
                    </Button>
                  ) : (
                    <Button
                      variant="outlined"
                      color="primary"
                      fullWidth
                      onClick={() => handleApiKeyConnect(provider)}
                      startIcon={<Key />}
                    >
                      Use API Key
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* OAuth Status Dialog */}
      <Dialog
        open={showDetails}
        onClose={() => setShowDetails(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Connect {selectedProvider?.display_name} with API Key
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            To use API key authentication, you'll need to manually enter your
            credentials. OAuth login is recommended for a better experience.
          </Typography>

          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              <strong>Getting API Credentials:</strong>
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle fontSize="small" />
                </ListItemIcon>
                <ListItemText
                  primary="Go to your domain provider's developer portal"
                  secondary="Find the API or developer section"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle fontSize="small" />
                </ListItemIcon>
                <ListItemText
                  primary="Generate API key and secret"
                  secondary="Ensure you have DNS management permissions"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle fontSize="small" />
                </ListItemIcon>
                <ListItemText
                  primary="Enter credentials in the app"
                  secondary="Your credentials are stored securely"
                />
              </ListItem>
            </List>
          </Alert>

          <Typography variant="body2">
            <strong>API Documentation:</strong>{" "}
            <a
              href={selectedProvider?.api_docs}
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: "inherit" }}
            >
              {selectedProvider?.api_docs}
            </a>
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDetails(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => {
              setShowDetails(false)
              // Redirect to API key setup
              window.location.href = "/domain-providers/setup"
            }}
          >
            Continue with API Key
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default DomainProviderOAuth
