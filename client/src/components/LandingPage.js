import React, { useState, useCallback, useMemo } from "react"
import PropTypes from "prop-types"
import {
  Box,
  Container,
  Typography,
  Button,
  TextField,
  Card,
  CardContent,
  Chip,
  Grid,
  Paper,
  Divider,
  useTheme,
  useMediaQuery
} from "@mui/material"
import {
  Cloud,
  TrendingUp,
  GitHub,
  Launch,
  CheckCircle,
  ArrowForward,
  Code,
  Deploy,
  Domain,
  KeyboardArrowDown,
  Settings,
  Visibility
} from "@mui/icons-material"
import "./LandingPage.css"

// Constants for better maintainability
const FEATURES_DATA = [
  {
    id: "github-integration",
    icon: GitHub,
    title: "GitHub Integration",
    description: "Connect your repositories seamlessly",
    color: "#24292e"
  },
  {
    id: "one-click-deploy",
    icon: Deploy,
    title: "One-Click Deploy",
    description: "Deploy to Render with zero configuration",
    color: "#00d4aa"
  },
  {
    id: "custom-domains",
    icon: Domain,
    title: "Custom Domains",
    description: "Automatically configure DNS records",
    color: "#6366f1"
  }
]

const STATS_DATA = [
  {
    id: "deployments",
    label: "Deployments",
    value: "1,234+",
    icon: TrendingUp
  },
  { id: "users", label: "Users", value: "567+", icon: CheckCircle },
  {
    id: "success-rate",
    label: "Success Rate",
    value: "99.8%",
    icon: CheckCircle
  }
]

// Reusable components for better maintainability
const WindowControls = () => (
  <Box display="flex" alignItems="center" gap={1}>
    <Box className="window-button red" aria-label="Close window" />
    <Box className="window-button yellow" aria-label="Minimize window" />
    <Box className="window-button green" aria-label="Maximize window" />
  </Box>
)

const LineNumbers = ({ count = 20 }) => (
  <Box className="line-numbers" role="presentation">
    {Array.from({ length: count }, (_, i) => (
      <Box key={i} className="line-number" aria-hidden="true">
        {i + 1}
      </Box>
    ))}
  </Box>
)

LineNumbers.propTypes = {
  count: PropTypes.number
}

const CodeLine = ({ children, indentLevel = 0, className = "" }) => (
  <Box
    className={`code-line ${
      indentLevel > 0 ? `indent-${indentLevel}` : ""
    } ${className}`}
    component="pre"
  >
    {children}
  </Box>
)

CodeLine.propTypes = {
  children: PropTypes.node.isRequired,
  indentLevel: PropTypes.number,
  className: PropTypes.string
}

const DeploymentSection = ({ title, children }) => (
  <Box className="deployment-section">
    <Typography variant="body2" className="section-title">
      {title}
    </Typography>
    {children}
  </Box>
)

DeploymentSection.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired
}

const StatusBar = () => {
  const currentTime = useMemo(() => new Date(), [])

  return (
    <Box className="status-bar" role="status">
      <Box display="flex" alignItems="center" gap={2}>
        <Typography variant="body2" className="status-item">
          Cursor Tab
        </Typography>
        <Typography variant="body2" className="status-item">
          Ln 17, Col 3
        </Typography>
        <Typography variant="body2" className="status-item">
          Spaces: 2
        </Typography>
        <Typography variant="body2" className="status-item">
          UTF-8
        </Typography>
        <Typography variant="body2" className="status-item">
          LF
        </Typography>
        <Typography variant="body2" className="status-item">
          TypeScript
        </Typography>
      </Box>
      <Box display="flex" alignItems="center" gap={1}>
        <Settings className="status-icon" aria-label="Settings" />
        <Visibility className="status-icon" aria-label="Toggle visibility" />
      </Box>
    </Box>
  )
}

const LandingPage = ({ onGetStarted, className = "" }) => {
  const [email, setEmail] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [emailError, setEmailError] = useState("")

  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down("md"))

  // Memoized values for performance
  const currentTime = useMemo(() => {
    return (
      new Date().toLocaleDateString("en-US", {
        month: "short",
        day: "numeric"
      }) +
      " " +
      new Date().toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true
      })
    )
  }, [])

  // Email validation
  const validateEmail = useCallback((email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }, [])

  const handleEmailChange = useCallback(
    (e) => {
      const value = e.target.value
      setEmail(value)

      if (value && !validateEmail(value)) {
        setEmailError("Please enter a valid email address")
      } else {
        setEmailError("")
      }
    },
    [validateEmail]
  )

  const handleEmailSubmit = useCallback(
    async (e) => {
      e.preventDefault()

      if (!email.trim()) {
        setEmailError("Email is required")
        return
      }

      if (!validateEmail(email)) {
        setEmailError("Please enter a valid email address")
        return
      }

      setIsLoading(true)
      setEmailError("")

      try {
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1000))

        if (onGetStarted) {
          onGetStarted(email)
        }
      } catch (error) {
        console.error("Email submission failed:", error)
        setEmailError("Failed to submit email. Please try again.")
      } finally {
        setIsLoading(false)
      }
    },
    [email, validateEmail, onGetStarted]
  )

  const handleDeployClick = useCallback(() => {
    if (onGetStarted) {
      onGetStarted()
    }
  }, [onGetStarted])

  return (
    <Box className={`landing-page ${className}`} component="main">
      {/* Grid Background */}
      <Box className="grid-background" aria-hidden="true" />

      {/* Gradient Background */}
      <Box className="gradient-background" aria-hidden="true" />

      {/* Header */}
      <Box className="header" component="header">
        <Container maxWidth="lg">
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            py={2}
          >
            <Box display="flex" alignItems="center" gap={3}>
              <Box display="flex" alignItems="center">
                <Cloud className="logo-icon" aria-hidden="true" />
                <Typography variant="h6" className="logo-text" component="h1">
                  RepoTorpedo
                </Typography>
              </Box>
              <Box display="flex" gap={3} className="nav-links" component="nav">
                <Typography
                  variant="body2"
                  className="nav-link"
                  component="a"
                  href="#blog"
                >
                  Blog
                </Typography>
                <Typography
                  variant="body2"
                  className="nav-link"
                  component="a"
                  href="#careers"
                >
                  Careers
                </Typography>
                <Typography
                  variant="body2"
                  className="nav-link"
                  component="a"
                  href="#access"
                >
                  Get access
                </Typography>
              </Box>
            </Box>
            <Typography
              variant="body2"
              className="time-display"
              aria-label="Current time"
            >
              {currentTime}
            </Typography>
          </Box>
        </Container>
      </Box>

      {/* Hero Section with Code Editor */}
      <Container maxWidth="lg" className="hero-section">
        <Box textAlign="center" py={8}>
          <Typography variant="h1" className="hero-title" component="h2">
            It has never been easier to build software.
          </Typography>

          {/* Code Editor Window */}
          <Box className="code-editor-container">
            <Paper
              className="code-editor-window"
              elevation={0}
              role="application"
              aria-label="Code editor"
            >
              {/* Window Title Bar */}
              <Box className="window-title-bar">
                <WindowControls />
                <Box
                  display="flex"
                  alignItems="center"
                  gap={1}
                  className="window-title"
                >
                  <Code className="window-icon" aria-hidden="true" />
                  <Typography variant="body2">frontend</Typography>
                </Box>
                <Box />
              </Box>

              {/* Code Editor Content */}
              <Box className="code-editor-content">
                <Box className="code-pane">
                  <LineNumbers count={20} />
                  <Box className="code-content">
                    <CodeLine>
                      <span className="keyword">import</span>{" "}
                      <span className="string">React</span>{" "}
                      <span className="keyword">from</span>{" "}
                      <span className="string">'react'</span>;
                    </CodeLine>
                    <CodeLine>
                      <span className="keyword">import</span>{" "}
                      <span className="string">'./App.css'</span>;
                    </CodeLine>
                    <CodeLine />
                    <CodeLine>
                      <span className="keyword">function</span>{" "}
                      <span className="function">App</span>() {"{"}
                    </CodeLine>
                    <CodeLine indentLevel={1}>
                      <span className="keyword">return</span> (
                    </CodeLine>
                    <CodeLine indentLevel={2}>
                      &lt;<span className="tag">div</span>{" "}
                      <span className="attribute">className</span>=
                      <span className="string">"App"</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={3}>
                      &lt;<span className="tag">header</span>{" "}
                      <span className="attribute">className</span>=
                      <span className="string">"App-header"</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={4}>
                      &lt;<span className="tag">h1</span>&gt;Welcome to
                      RepoTorpedo&lt;/<span className="tag">h1</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={4}>
                      &lt;<span className="tag">p</span>&gt;Deploy your app in
                      seconds&lt;/<span className="tag">p</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={3}>
                      &lt;/<span className="tag">header</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={2}>
                      &lt;/<span className="tag">div</span>&gt;
                    </CodeLine>
                    <CodeLine indentLevel={1}>);</CodeLine>
                    <CodeLine>{"}"}</CodeLine>
                    <CodeLine />
                    <CodeLine>
                      <span className="keyword">export</span>{" "}
                      <span className="keyword">default</span> App;
                    </CodeLine>
                  </Box>
                </Box>

                {/* Right Pane - Deployment Panel */}
                <Box className="deployment-pane">
                  <DeploymentSection title="Ready to deploy">
                    <Box className="deployment-item">
                      <Box className="deployment-info">
                        <Typography variant="body2" className="file-path">
                          src/App.js
                        </Typography>
                        <Typography variant="body2" className="file-stats">
                          L1-L25
                        </Typography>
                      </Box>
                      <Chip
                        label="+25"
                        size="small"
                        className="stats-chip positive"
                      />
                    </Box>
                  </DeploymentSection>

                  <Divider className="pane-divider" />

                  <DeploymentSection title="Build Status">
                    <Box className="build-status">
                      <Box
                        className="status-indicator success"
                        aria-label="Build successful"
                      />
                      <Typography variant="body2">Build successful</Typography>
                    </Box>
                  </DeploymentSection>

                  <DeploymentSection title="Deploy to Render">
                    <TextField
                      fullWidth
                      variant="outlined"
                      placeholder="Plan, search, build anything"
                      className="deploy-input"
                      size="small"
                      aria-label="Deployment description"
                    />
                    <Button
                      variant="contained"
                      className="deploy-button"
                      fullWidth
                      startIcon={<Launch />}
                      onClick={handleDeployClick}
                      aria-label="Deploy application"
                    >
                      Deploy
                    </Button>
                  </DeploymentSection>
                </Box>
              </Box>

              {/* Status Bar */}
              <StatusBar />
            </Paper>
          </Box>

          {/* Email Signup Form */}
          <Paper className="email-form" elevation={0} component="section">
            <form onSubmit={handleEmailSubmit} noValidate>
              <Box
                display="flex"
                gap={2}
                flexDirection={isMobile ? "column" : "row"}
              >
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Enter your email"
                  value={email}
                  onChange={handleEmailChange}
                  className="email-input"
                  error={!!emailError}
                  helperText={emailError}
                  disabled={isLoading}
                  type="email"
                  required
                  aria-label="Email address"
                  InputProps={{
                    className: "email-input-field"
                  }}
                />
                <Button
                  type="submit"
                  variant="contained"
                  className="cta-button"
                  disabled={isLoading || !email.trim()}
                  size="large"
                  aria-label={isLoading ? "Submitting email" : "Join the beta"}
                >
                  {isLoading ? "Joining..." : "Join the beta"}
                </Button>
              </Box>
            </form>
          </Paper>

          <Typography variant="body2" className="beta-note">
            First 100 sign-ups get a lifetime discount.
          </Typography>
        </Box>
      </Container>

      {/* Scroll to Deploy */}
      <Box
        className="scroll-cta"
        role="button"
        tabIndex={0}
        onClick={() =>
          window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
          })
        }
      >
        <Typography variant="body1" className="scroll-text">
          Scroll to deploy
        </Typography>
        <KeyboardArrowDown className="scroll-arrow" aria-hidden="true" />
      </Box>

      {/* Features Grid */}
      <Container maxWidth="lg" className="features-section">
        <Typography
          variant="h3"
          className="section-title"
          textAlign="center"
          mb={6}
          component="h3"
        >
          Why choose RepoTorpedo?
        </Typography>

        <Grid container spacing={4}>
          {FEATURES_DATA.map((feature) => {
            const IconComponent = feature.icon
            return (
              <Grid item xs={12} md={4} key={feature.id}>
                <Card className="feature-card">
                  <CardContent textAlign="center">
                    <Box
                      className="feature-icon"
                      style={{ backgroundColor: feature.color }}
                      aria-hidden="true"
                    >
                      <IconComponent />
                    </Box>
                    <Typography
                      variant="h6"
                      className="feature-title"
                      mt={2}
                      component="h4"
                    >
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" className="feature-description">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            )
          })}
        </Grid>
      </Container>

      {/* Stats Section */}
      <Container maxWidth="lg" className="stats-section">
        <Grid container spacing={4} justifyContent="center">
          {STATS_DATA.map((stat) => {
            const IconComponent = stat.icon
            return (
              <Grid item xs={12} sm={4} key={stat.id}>
                <Box textAlign="center">
                  <Box className="stat-icon" aria-hidden="true">
                    <IconComponent />
                  </Box>
                  <Typography
                    variant="h3"
                    className="stat-value"
                    component="div"
                  >
                    {stat.value}
                  </Typography>
                  <Typography variant="body1" className="stat-label">
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            )
          })}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Container maxWidth="md" className="cta-section">
        <Box textAlign="center" py={8}>
          <Typography variant="h3" className="cta-title" component="h3">
            Ready to deploy faster?
          </Typography>
          <Typography variant="h6" className="cta-subtitle" mb={4}>
            Join thousands of developers who've simplified their deployment
            workflow
          </Typography>
          <Button
            variant="contained"
            size="large"
            className="cta-button-large"
            onClick={handleDeployClick}
            endIcon={<ArrowForward />}
            aria-label="Get started with RepoTorpedo"
          >
            Get Started Now
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
  onGetStarted: () => {},
  className: ""
}

export default LandingPage
