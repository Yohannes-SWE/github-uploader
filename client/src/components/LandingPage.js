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
      {/* Pure black background */}
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

      {/* Minimal Header - matching Antimetal style */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          zIndex: 10,
          py: 3,
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
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
            <GitHub sx={{ color: "white", fontSize: 18 }} />
            <Typography
              variant="body1"
              sx={{
                color: "white",
                fontWeight: 500,
                fontSize: "15px",
                letterSpacing: "-0.01em"
              }}
            >
              RepoTorpedo
            </Typography>
          </Box>

          <Box sx={{ display: "flex", gap: 6 }}>
            <Typography
              component="a"
              href="#"
              sx={{
                color: "rgba(255,255,255,0.7)",
                textDecoration: "none",
                fontSize: "15px",
                fontWeight: 400,
                letterSpacing: "-0.01em",
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
                fontSize: "15px",
                fontWeight: 400,
                letterSpacing: "-0.01em",
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
                fontSize: "15px",
                fontWeight: 400,
                letterSpacing: "-0.01em",
                "&:hover": { color: "white" }
              }}
            >
              Get access
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Centered Content - Antimetal inspired */}
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
          {/* Main Headline - Antimetal style */}
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: "2.75rem", sm: "4rem", md: "5rem" },
              fontWeight: 500,
              color: "white",
              lineHeight: 1.1,
              letterSpacing: "-0.025em",
              mb: 8,
              maxWidth: "900px",
              fontFamily:
                "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
            }}
          >
            It has never been easier{" "}
            <Box
              component="span"
              sx={{
                color: "rgba(255,255,255,0.5)"
              }}
            >
              to deploy your code.
            </Box>
          </Typography>

          {/* Simple CTA - Heyorbi inspired */}
          <Box
            component="form"
            onSubmit={handleEmailSubmit}
            sx={{
              display: "flex",
              gap: 2,
              maxWidth: "420px",
              width: "100%",
              flexDirection: { xs: "column", sm: "row" },
              mb: 3
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
                  background: "rgba(255,255,255,0.04)",
                  borderRadius: "8px",
                  color: "white",
                  fontSize: "15px",
                  py: 0.5,
                  "& fieldset": {
                    borderColor: "rgba(255,255,255,0.15)"
                  },
                  "&:hover fieldset": {
                    borderColor: "rgba(255,255,255,0.25)"
                  },
                  "&.Mui-focused fieldset": {
                    borderColor: "rgba(255,255,255,0.4)"
                  }
                },
                "& .MuiInputBase-input": {
                  py: 1.5,
                  "&::placeholder": {
                    color: "rgba(255,255,255,0.5)",
                    opacity: 1
                  }
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
                px: 4,
                py: 1.75,
                borderRadius: "8px",
                textTransform: "none",
                fontSize: "15px",
                letterSpacing: "-0.01em",
                minWidth: "140px",
                "&:hover": {
                  background: "rgba(255,255,255,0.92)"
                },
                "&:disabled": {
                  background: "rgba(255,255,255,0.15)",
                  color: "rgba(255,255,255,0.4)"
                }
              }}
            >
              {isLoading ? "Starting..." : "Get started"}
            </Button>
          </Box>

          <Typography
            variant="body2"
            sx={{
              color: "rgba(255,255,255,0.4)",
              fontSize: "13px",
              fontWeight: 400,
              letterSpacing: "-0.01em"
            }}
          >
            Free forever · No credit card required
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
