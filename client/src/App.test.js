import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import "@testing-library/jest-dom"
import App from "./App"

// Mock axios
jest.mock("axios", () => ({
  post: jest.fn()
}))

// Mock fetch for auth status checks
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () =>
      Promise.resolve({
        authenticated: false,
        username: ""
      })
  })
)

test("renders RepoTorpedo landing page", async () => {
  render(<App />)
  // Wait for loading to complete
  await waitFor(() => {
    expect(
      screen.queryByText(/Loading your workspace/i)
    ).not.toBeInTheDocument()
  })
  // Use getAllByText to handle multiple instances and just check the first one
  const titleElements = screen.getAllByText(/RepoTorpedo/i)
  expect(titleElements[0]).toBeInTheDocument()
})

test("renders hero section with deployment leads text", async () => {
  render(<App />)
  // Wait for loading to complete
  await waitFor(() => {
    expect(
      screen.queryByText(/Loading your workspace/i)
    ).not.toBeInTheDocument()
  })
  const heroText = screen.getByText(/fresh deployment leads/i)
  expect(heroText).toBeInTheDocument()
})

test("renders navigation links", async () => {
  render(<App />)
  // Wait for loading to complete
  await waitFor(() => {
    expect(
      screen.queryByText(/Loading your workspace/i)
    ).not.toBeInTheDocument()
  })
  const blogLink = screen.getByText(/Blog/i)
  const careersLink = screen.getByText(/Careers/i)
  expect(blogLink).toBeInTheDocument()
  expect(careersLink).toBeInTheDocument()
})

test("renders landing page description", async () => {
  render(<App />)
  // Wait for loading to complete
  await waitFor(() => {
    expect(
      screen.queryByText(/Loading your workspace/i)
    ).not.toBeInTheDocument()
  })
  const description = screen.getByText(
    /finds deployment opportunities for you/i
  )
  expect(description).toBeInTheDocument()
})
