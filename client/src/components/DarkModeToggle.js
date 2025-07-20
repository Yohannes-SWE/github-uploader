import React, { useEffect, useState } from "react"
import { IconButton, Tooltip } from "@mui/material"
import { Brightness4, Brightness7 } from "@mui/icons-material"

const DarkModeToggle = ({ onToggle, darkMode }) => (
  <Tooltip title={darkMode ? "Switch to light mode" : "Switch to dark mode"}>
    <IconButton onClick={onToggle} color="inherit">
      {darkMode ? <Brightness7 /> : <Brightness4 />}
    </IconButton>
  </Tooltip>
)

export default DarkModeToggle
