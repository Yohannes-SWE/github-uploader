import React, { useState, useRef } from "react"
import {
  Box,
  Typography,
  Button,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Chip,
  Alert,
  LinearProgress
} from "@mui/material"
import {
  CloudUpload,
  FolderOpen,
  InsertDriveFile,
  Image,
  Code,
  Delete,
  CheckCircle,
  Error
} from "@mui/icons-material"

const FileUpload = ({ onFilesSelected }) => {
  const [files, setFiles] = useState([])
  const [isDragOver, setIsDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const fileInputRef = useRef()

  const handleFileSelect = (selectedFiles) => {
    const newFiles = Array.from(selectedFiles).map((file) => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      status: "ready"
    }))

    setFiles((prev) => [...prev, ...newFiles])
    if (onFilesSelected) {
      onFilesSelected([...files, ...newFiles])
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    const droppedFiles = e.dataTransfer.files
    handleFileSelect(droppedFiles)
  }

  const handleFileInput = (e) => {
    const selectedFiles = e.target.files
    handleFileSelect(selectedFiles)
  }

  const removeFile = (fileId) => {
    setFiles((prev) => prev.filter((f) => f.id !== fileId))
  }

  const getFileIcon = (fileType) => {
    if (fileType.startsWith("image/")) return <Image />
    if (
      fileType.includes("html") ||
      fileType.includes("css") ||
      fileType.includes("javascript")
    )
      return <Code />
    return <InsertDriveFile />
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const getFileType = (fileName) => {
    const extension = fileName.split(".").pop().toLowerCase()
    const typeMap = {
      "html": "HTML File",
      "css": "CSS File",
      "js": "JavaScript File",
      "jpg": "Image",
      "jpeg": "Image",
      "png": "Image",
      "gif": "Image",
      "svg": "Image",
      "ico": "Icon",
      "txt": "Text File",
      "json": "JSON File",
      "xml": "XML File"
    }
    return typeMap[extension] || "File"
  }

  const supportedFileTypes = [
    "text/html",
    "text/css",
    "text/javascript",
    "application/javascript",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/svg+xml",
    "text/plain",
    "application/json"
  ]

  const isFileSupported = (file) => {
    return (
      supportedFileTypes.includes(file.type) ||
      file.name.endsWith(".html") ||
      file.name.endsWith(".css") ||
      file.name.endsWith(".js")
    )
  }

  const uploadFiles = async () => {
    setUploading(true)
    setUploadProgress(0)

    try {
      // Simulate upload progress
      for (let i = 0; i <= 100; i += 10) {
        setUploadProgress(i)
        await new Promise((resolve) => setTimeout(resolve, 200))
      }

      // Update file statuses
      setFiles((prev) => prev.map((f) => ({ ...f, status: "uploaded" })))

      // Here you would actually upload to your backend
      console.log("Files ready for upload:", files)
    } catch (error) {
      console.error("Upload failed:", error)
      setFiles((prev) => prev.map((f) => ({ ...f, status: "error" })))
    } finally {
      setUploading(false)
    }
  }

  const hasUnsupportedFiles = files.some((f) => !isFileSupported(f.file))

  return (
    <Box>
      {/* Upload Area */}
      <Paper
        sx={{
          p: 4,
          textAlign: "center",
          border: "2px dashed",
          borderColor: isDragOver ? "#1976d2" : "#e0e0e0",
          backgroundColor: isDragOver ? "#f3f8ff" : "#fafafa",
          transition: "all 0.3s ease",
          cursor: "pointer",
          mb: 3
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <CloudUpload sx={{ fontSize: 60, color: "#1976d2", mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          {isDragOver
            ? "Drop your files here"
            : "Drag & Drop Your Website Files"}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          or click to browse your computer
        </Typography>
        <Button variant="outlined" startIcon={<FolderOpen />}>
          Choose Files
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileInput}
          style={{ display: "none" }}
          accept=".html,.css,.js,.jpg,.jpeg,.png,.gif,.svg,.ico,.txt,.json,.xml"
        />
      </Paper>

      {/* Supported Files Info */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>Supported files:</strong> HTML, CSS, JavaScript, images (JPG,
          PNG, GIF, SVG), and other web files. We'll automatically detect your
          website structure.
        </Typography>
      </Alert>

      {/* File List */}
      {files.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2
            }}
          >
            <Typography variant="h6">
              Your Website Files ({files.length})
            </Typography>
            <Button
              variant="contained"
              onClick={uploadFiles}
              disabled={uploading || hasUnsupportedFiles}
              startIcon={<CloudUpload />}
            >
              {uploading ? "Uploading..." : "Upload Files"}
            </Button>
          </Box>

          {uploading && (
            <Box sx={{ mb: 2 }}>
              <LinearProgress variant="determinate" value={uploadProgress} />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Uploading files... {uploadProgress}%
              </Typography>
            </Box>
          )}

          <List>
            {files.map((file) => (
              <ListItem
                key={file.id}
                sx={{
                  border: "1px solid #e0e0e0",
                  borderRadius: 1,
                  mb: 1,
                  backgroundColor:
                    file.status === "error"
                      ? "#ffebee"
                      : file.status === "uploaded"
                      ? "#e8f5e8"
                      : "#fafafa"
                }}
                secondaryAction={
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    {file.status === "uploaded" && (
                      <CheckCircle color="success" />
                    )}
                    {file.status === "error" && <Error color="error" />}
                    {!isFileSupported(file.file) && (
                      <Chip label="Unsupported" size="small" color="warning" />
                    )}
                    <IconButton
                      edge="end"
                      onClick={() => removeFile(file.id)}
                      disabled={uploading}
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                }
              >
                <ListItemIcon>{getFileIcon(file.file.type)}</ListItemIcon>
                <ListItemText
                  primary={file.name}
                  secondary={
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        {getFileType(file.name)} • {formatFileSize(file.size)}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>

          {hasUnsupportedFiles && (
            <Alert severity="warning" sx={{ mt: 2 }}>
              Some files may not be supported for web deployment. We recommend
              using HTML, CSS, JavaScript, and image files.
            </Alert>
          )}
        </Paper>
      )}

      {/* Quick Tips */}
      <Paper sx={{ p: 3, backgroundColor: "#f8f9fa" }}>
        <Typography variant="h6" gutterBottom>
          💡 Quick Tips
        </Typography>
        <Box component="ul" sx={{ pl: 2, m: 0 }}>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Main page:</strong> Include an <code>index.html</code> file
            for your homepage
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>Images:</strong> Put all images in a folder (like "images"
            or "img")
          </Typography>
          <Typography component="li" variant="body2" sx={{ mb: 1 }}>
            <strong>CSS:</strong> Include your stylesheet to make your site look
            great
          </Typography>
          <Typography component="li" variant="body2">
            <strong>JavaScript:</strong> Add interactive features to your
            website
          </Typography>
        </Box>
      </Paper>
    </Box>
  )
}

export default FileUpload
