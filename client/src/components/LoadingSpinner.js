import React from "react"
import { Box, CircularProgress, Typography } from "@mui/material"

const LoadingSpinner = ({ message = "Loading..." }) => (
  <Box
    display="flex"
    flexDirection="column"
    alignItems="center"
    justifyContent="center"
    minHeight="40vh"
  >
    <CircularProgress size={60} sx={{ mb: 3, color: "#F28C28" }} />
    <Typography variant="h6" color="text.secondary">
      {message}
    </Typography>
  </Box>
)

export default LoadingSpinner
