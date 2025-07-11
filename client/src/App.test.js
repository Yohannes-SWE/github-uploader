import { render, screen, fireEvent } from "@testing-library/react"
import App from "./App"

// Mock axios
jest.mock("axios", () => ({
  post: jest.fn()
}))

test("renders GitHub Uploader title", () => {
  render(<App />)
  const titleElement = screen.getByText(/GitHub Uploader/i)
  expect(titleElement).toBeInTheDocument()
})

test("renders login button", () => {
  render(<App />)
  const loginButton = screen.getByText(/Login with GitHub/i)
  expect(loginButton).toBeInTheDocument()
})

test("renders drag and drop area", () => {
  render(<App />)
  const dropZone = screen.getByText(/Drag & drop a zipped project folder here/i)
  expect(dropZone).toBeInTheDocument()
})

test("analyze button is disabled when no file selected", () => {
  render(<App />)
  const analyzeButton = screen.getByText(/Analyze Project/i)
  expect(analyzeButton).toBeDisabled()
})
