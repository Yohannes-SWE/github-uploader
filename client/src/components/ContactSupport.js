import React, { useState } from "react"
import { Paper, Typography, TextField, Button, Box, Alert } from "@mui/material"

const ContactSupport = () => {
  const [form, setForm] = useState({ name: "", email: "", message: "" })
  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setSubmitted(true)
  }

  if (submitted) {
    return (
      <Alert severity="success" sx={{ mt: 4 }}>
        Thank you for contacting support! We'll get back to you soon.
      </Alert>
    )
  }

  return (
    <Paper sx={{ p: 4, mt: 6, maxWidth: 500, mx: "auto" }}>
      <Typography variant="h5" gutterBottom>
        Contact Support
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Name"
          name="name"
          value={form.name}
          onChange={handleChange}
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
          label="Email"
          name="email"
          value={form.email}
          onChange={handleChange}
          type="email"
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
          label="Message"
          name="message"
          value={form.message}
          onChange={handleChange}
          multiline
          rows={4}
          fullWidth
          sx={{ mb: 2 }}
        />
        <Button variant="contained" type="submit">
          Send
        </Button>
      </form>
    </Paper>
  )
}

export default ContactSupport
