import React, { useState, useCallback, memo } from "react"
import PropTypes from "prop-types"
import { Box, Container, Typography, Button, TextField } from "@mui/material"
import { GitHub, ArrowForward } from "@mui/icons-material"
import "./LandingPage.css"

const LandingPage = ({ onGetStarted, className = "" }) => {
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleGetStarted = useCallback(() => {
    if (onGetStarted) {
      onGetStarted()
    }
  }, [onGetStarted])

  const handleEmailSubmit = useCallback(
    async (e) => {
      e.preventDefault()
      if (!email.trim()) return

      setIsLoading(true)
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      handleGetStarted()
      setIsLoading(false)
    },
    [email, handleGetStarted]
  )

  return (
    <Box className={`landing-page ${className}`}>
      {/* Dark background */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "#000000",
          zIndex: -1
        }}
      />

      {/* Minimal Header */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          zIndex: 10,
          py: 2,
          px: 4
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <GitHub sx={{ color: "white", fontSize: 20 }} />
            <Typography
              variant="body1"
              sx={{
                color: "white",
                fontWeight: 500,
                fontSize: "14px"
              }}
            >
              RepoTorpedo
            </Typography>
          </Box>

          <Box sx={{ display: "flex", gap: 4 }}>
            <Typography
              component="a"
              href="#"
              sx={{
                color: "rgba(255,255,255,0.7)",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 400,
                "&:hover": { color: "white" }
              }}
            >
              Blog
            </Typography>
            <Typography
              component="a"
              href="#"
              sx={{
                color: "rgba(255,255,255,0.7)",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 400,
                "&:hover": { color: "white" }
              }}
            >
              Careers
            </Typography>
            <Typography
              component="a"
              href="#"
              sx={{
                color: "rgba(255,255,255,0.7)",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 400,
                "&:hover": { color: "white" }
              }}
            >
              Get access
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Centered Content */}
      <Container maxWidth="md">
        <Box
          sx={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            textAlign: "center",
            px: 2
          }}
        >
          {/* Main Headline */}
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: "2.5rem", sm: "3.5rem", md: "4.5rem" },
              fontWeight: 400,
              color: "white",
              lineHeight: 1.2,
              letterSpacing: "-0.02em",
              mb: 6,
              maxWidth: "800px",
              fontFamily:
                "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
            }}
          >
            Deploy your code in{" "}
            <Box
              component="span"
              sx={{
                color: "rgba(255,255,255,0.4)"
              }}
            >
              seconds, not hours.
            </Box>
          </Typography>

          {/* Simple CTA */}
          <Box
            component="form"
            onSubmit={handleEmailSubmit}
            sx={{
              display: "flex",
              gap: 2,
              maxWidth: "400px",
              width: "100%",
              flexDirection: { xs: "column", sm: "row" },
              mb: 2
            }}
          >
            <TextField
              placeholder="Enter your email"
              variant="outlined"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              sx={{
                flex: 1,
                "& .MuiOutlinedInput-root": {
                  background: "rgba(255,255,255,0.05)",
                  borderRadius: "8px",
                  color: "white",
                  fontSize: "14px",
                  "& fieldset": {
                    borderColor: "rgba(255,255,255,0.2)"
                  },
                  "&:hover fieldset": {
                    borderColor: "rgba(255,255,255,0.3)"
                  },
                  "&.Mui-focused fieldset": {
                    borderColor: "white"
                  }
                },
                "& .MuiInputBase-input::placeholder": {
                  color: "rgba(255,255,255,0.5)",
                  opacity: 1
                }
              }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={!email.trim() || isLoading}
              endIcon={<ArrowForward sx={{ fontSize: 16 }} />}
              sx={{
                background: "white",
                color: "black",
                fontWeight: 500,
                px: 3,
                py: 1.5,
                borderRadius: "8px",
                textTransform: "none",
                fontSize: "14px",
                "&:hover": {
                  background: "rgba(255,255,255,0.9)"
                },
                "&:disabled": {
                  background: "rgba(255,255,255,0.2)",
                  color: "rgba(255,255,255,0.5)"
                }
              }}
            >
              {isLoading ? "Starting..." : "Get Started"}
            </Button>
          </Box>

          <Typography
            variant="body2"
            sx={{
              color: "rgba(255,255,255,0.4)",
              fontSize: "12px",
              fontWeight: 400
            }}
          >
            Free forever • No credit card required
          </Typography>
        </Box>
      </Container>
    </Box>
  )
}

LandingPage.propTypes = {
  onGetStarted: PropTypes.func,
  className: PropTypes.string
}

LandingPage.defaultProps = {
  className: ""
}

// Export memoized component for better performance
export default memo(LandingPage)
