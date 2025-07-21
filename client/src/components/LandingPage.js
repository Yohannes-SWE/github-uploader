import React, { useState, useCallback, memo } from "react"
import PropTypes from "prop-types"
import {
  Box,
  Container,
  Typography,
  Button,
  TextField,
  Paper
} from "@mui/material"
import {
  GitHub,
  Launch,
  Code,
  CloudUpload,
  ArrowForward
} from "@mui/icons-material"
import "./LandingPage.css"

// Simplified components for tech vibe
const CodeTerminal = memo(() => (
  <Paper
    className="code-terminal"
    elevation={0}
    sx={{
      background: "rgba(0, 0, 0, 0.8)",
      border: "1px solid rgba(255, 255, 255, 0.1)",
      borderRadius: "12px",
      p: 3,
      fontFamily: "'Monaco', monospace",
      fontSize: "14px",
      color: "#00ff88",
      maxWidth: "500px",
      margin: "0 auto"
    }}
  >
    <Box sx={{ display: "flex", alignItems: "center", mb: 2, gap: 1 }}>
      <Box
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#ff5f57"
        }}
      />
      <Box
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#ffbd2e"
        }}
      />
      <Box
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#28ca42"
        }}
      />
      <Typography sx={{ ml: 2, color: "#666", fontSize: "12px" }}>
        terminal
      </Typography>
    </Box>

    <Box component="pre" sx={{ color: "#00ff88", lineHeight: 1.6 }}>
      {`$ git push origin main
Counting objects: 15, done.
Compressing objects: 100% (12/12), done.
Writing objects: 100% (15/15), 2.1 KiB
Total 15 (delta 8), reused 0 (delta 0)

`}
      <Box component="span" sx={{ color: "#ff6b6b" }}>
        🚀 RepoTorpedo detected new deployment
      </Box>
      {`
✅ Project analyzed successfully
✅ Render service connected
✅ Domain configured: `}
      <Box component="span" sx={{ color: "#4ecdc4" }}>
        your-app.onrender.com
      </Box>
      {`

Deployment complete in 47s
`}
    </Box>
  </Paper>
))

CodeTerminal.displayName = "CodeTerminal"

const TechFeature = memo(({ icon: Icon, title, description }) => (
  <Box sx={{ textAlign: "center", p: 2 }}>
    <Box
      sx={{
        width: 48,
        height: 48,
        borderRadius: "12px",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        margin: "0 auto 16px auto",
        color: "white"
      }}
    >
      <Icon sx={{ fontSize: 24 }} />
    </Box>
    <Typography
      variant="h6"
      gutterBottom
      sx={{ color: "white", fontWeight: 600 }}
    >
      {title}
    </Typography>
    <Typography variant="body2" sx={{ color: "rgba(255,255,255,0.7)" }}>
      {description}
    </Typography>
  </Box>
))

TechFeature.displayName = "TechFeature"

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
      {/* Gradient Background */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)",
          zIndex: -2
        }}
      />

      {/* Subtle Grid Pattern */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: `radial-gradient(circle at 25px 25px, rgba(255,255,255,0.1) 2px, transparent 0)`,
          backgroundSize: "50px 50px",
          zIndex: -1
        }}
      />

      {/* Simple Header */}
      <Container maxWidth="lg" sx={{ pt: 4, pb: 2 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <Code sx={{ color: "#00ff88", fontSize: 32 }} />
            <Typography
              variant="h5"
              sx={{
                color: "white",
                fontWeight: 700,
                background: "linear-gradient(135deg, #00ff88 0%, #00d4ff 100%)",
                backgroundClip: "text",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent"
              }}
            >
              RepoTorpedo
            </Typography>
          </Box>

          <Box sx={{ display: "flex", gap: 3 }}>
            <Typography
              component="a"
              href="#features"
              sx={{
                color: "rgba(255,255,255,0.8)",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 500,
                "&:hover": { color: "white" }
              }}
            >
              Features
            </Typography>
            <Typography
              component="a"
              href="#github"
              sx={{
                color: "rgba(255,255,255,0.8)",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 500,
                "&:hover": { color: "white" }
              }}
            >
              GitHub
            </Typography>
          </Box>
        </Box>
      </Container>

      {/* Hero Section */}
      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 12 } }}>
        <Box sx={{ textAlign: "center", mb: 8 }}>
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: "2.5rem", md: "4rem", lg: "5rem" },
              fontWeight: 800,
              color: "white",
              mb: 3,
              lineHeight: 1.1,
              letterSpacing: "-0.02em"
            }}
          >
            Deploy your code
            <br />
            <Box
              component="span"
              sx={{
                background:
                  "linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%)",
                backgroundClip: "text",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent"
              }}
            >
              in seconds
            </Box>
          </Typography>

          <Typography
            variant="h5"
            sx={{
              color: "rgba(255,255,255,0.7)",
              mb: 6,
              maxWidth: "600px",
              margin: "0 auto 48px auto",
              fontWeight: 400,
              lineHeight: 1.5
            }}
          >
            The fastest way to deploy your GitHub repositories to production.
            Zero configuration, maximum speed.
          </Typography>

          {/* Call to Action */}
          <Box
            component="form"
            onSubmit={handleEmailSubmit}
            sx={{
              display: "flex",
              gap: 2,
              maxWidth: "400px",
              margin: "0 auto 48px auto",
              flexDirection: { xs: "column", sm: "row" }
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
                  background: "rgba(255,255,255,0.1)",
                  borderRadius: "12px",
                  color: "white",
                  "& fieldset": {
                    borderColor: "rgba(255,255,255,0.2)"
                  },
                  "&:hover fieldset": {
                    borderColor: "rgba(255,255,255,0.3)"
                  },
                  "&.Mui-focused fieldset": {
                    borderColor: "#00ff88"
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
              endIcon={<ArrowForward />}
              sx={{
                background: "linear-gradient(135deg, #00ff88 0%, #00d4ff 100%)",
                color: "black",
                fontWeight: 600,
                px: 4,
                py: 1.5,
                borderRadius: "12px",
                textTransform: "none",
                fontSize: "16px",
                "&:hover": {
                  background:
                    "linear-gradient(135deg, #00e67a 0%, #00c4e6 100%)",
                  transform: "translateY(-1px)"
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
              color: "rgba(255,255,255,0.5)",
              mb: 6
            }}
          >
            Free forever • No credit card required
          </Typography>
        </Box>

        {/* Code Terminal Demo */}
        <Box sx={{ mb: 12 }}>
          <CodeTerminal />
        </Box>

        {/* Simple Features */}
        <Box id="features" sx={{ py: 8 }}>
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: "2rem", md: "2.5rem" },
              fontWeight: 700,
              color: "white",
              textAlign: "center",
              mb: 6
            }}
          >
            Everything you need
          </Typography>

          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" },
              gap: 4,
              mt: 6
            }}
          >
            <TechFeature
              icon={GitHub}
              title="GitHub Integration"
              description="Connect your repositories with one click. Automatic deployments on every push."
            />
            <TechFeature
              icon={CloudUpload}
              title="Zero Configuration"
              description="Smart detection of your tech stack. No config files or setup required."
            />
            <TechFeature
              icon={Launch}
              title="Instant Deployment"
              description="From git push to live URL in under 60 seconds. Lightning fast builds."
            />
          </Box>
        </Box>

        {/* Simple CTA */}
        <Box sx={{ textAlign: "center", py: 8 }}>
          <Typography
            variant="h3"
            sx={{
              fontSize: { xs: "1.8rem", md: "2.2rem" },
              fontWeight: 700,
              color: "white",
              mb: 4
            }}
          >
            Ready to deploy?
          </Typography>

          <Button
            onClick={handleGetStarted}
            variant="contained"
            size="large"
            endIcon={<ArrowForward />}
            sx={{
              background: "linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)",
              color: "white",
              fontWeight: 600,
              px: 6,
              py: 2,
              borderRadius: "16px",
              textTransform: "none",
              fontSize: "18px",
              "&:hover": {
                background: "linear-gradient(135deg, #ff5252 0%, #26a69a 100%)",
                transform: "translateY(-2px)",
                boxShadow: "0 8px 30px rgba(255, 107, 107, 0.3)"
              }
            }}
          >
            Start Building Now
          </Button>
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
