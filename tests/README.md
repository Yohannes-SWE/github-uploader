# User Flow Testing Suite

## Overview

This comprehensive testing suite covers all possible user interactions with the RepoTorpedo application. It tests every user journey, from initial registration to complex multi-provider deployments, ensuring the application works correctly in all scenarios.

## 🚀 Quick Start

### 1. Setup Testing Environment

```bash
# Navigate to the tests directory
cd tests

# Run the setup script
python3 setup_tests.py

# Start the mock server
./start_mock_server.sh

# Run quick tests
./run_tests.sh
```

### 2. Run Different Test Types

```bash
# Quick tests (critical paths only)
./run_tests.sh --quick

# Full test suite (all tests)
./run_tests.sh --full

# With coverage analysis
./run_tests.sh --coverage

# Generate HTML report
./run_tests.sh --report

# Verbose output
./run_tests.sh --verbose
```

## 📋 Test Categories

### 1. Authentication Flow Tests

Tests user registration, login, logout, and session management.

**Coverage:**

- ✅ User registration with valid/invalid data
- ✅ User login with correct/incorrect credentials
- ✅ Session management and persistence
- ✅ Logout functionality
- ✅ Password validation and confirmation

### 2. Provider Configuration Flow Tests

Tests hosting provider setup and management.

**Coverage:**

- ✅ Get list of supported providers
- ✅ Configure Render, Vercel, Netlify, Railway providers
- ✅ Test provider connections
- ✅ Remove provider configurations
- ✅ Handle invalid API keys and configuration errors

### 3. Deployment Flow Tests

Tests application deployment to various providers.

**Coverage:**

- ✅ Single provider deployments
- ✅ Multi-provider deployments
- ✅ Deployments with custom domains
- ✅ Different environment types (Node.js, Python, Static)
- ✅ Environment variables and build commands
- ✅ Error handling and validation

### 4. Deployment Status Flow Tests

Tests deployment monitoring and status tracking.

**Coverage:**

- ✅ Get deployment history
- ✅ Monitor deployment status
- ✅ Real-time status updates
- ✅ Handle non-existent deployments

### 5. Custom Domain Flow Tests

Tests custom domain management.

**Coverage:**

- ✅ Add custom domains to services
- ✅ Domain validation
- ✅ Error handling for invalid domains

### 6. Error Handling Flow Tests

Tests application error handling and edge cases.

**Coverage:**

- ✅ Unauthenticated access attempts
- ✅ Invalid JSON requests
- ✅ Missing required fields
- ✅ Input validation errors
- ✅ Network and server errors

### 7. Performance Flow Tests

Tests application performance under load.

**Coverage:**

- ✅ Concurrent deployments
- ✅ Large payload handling
- ✅ Memory usage under load
- ✅ Response time testing

### 8. Security Flow Tests

Tests application security measures.

**Coverage:**

- ✅ Session security
- ✅ Input sanitization
- ✅ SQL injection prevention
- ✅ XSS prevention
- ✅ Authentication bypass attempts

### 9. Integration Flow Tests

Tests complete end-to-end user journeys.

**Coverage:**

- ✅ Complete user registration → deployment flow
- ✅ Multi-provider setup and deployment
- ✅ Error recovery scenarios
- ✅ Provider management workflows

## 🛠️ Test Infrastructure

### Mock Server

The `mock_server.py` provides a realistic simulation of the application API without requiring external dependencies.

**Features:**

- ✅ Complete API endpoint simulation
- ✅ Realistic response patterns
- ✅ Error simulation capabilities
- ✅ Session management
- ✅ Data persistence during test runs

### Test Configuration

The `test_config.json` contains all test settings and data.

**Configuration:**

- Test environment settings
- Provider configurations
- Test user data
- Repository examples
- Deployment configurations

### Test Data

Sample applications for testing different deployment scenarios:

- **React App**: `test_repositories/simple-react-app/`
- **Node.js API**: `test_repositories/node-api/`
- **Python Flask App**: `test_repositories/python-flask-app/`

## 📊 Test Results

### HTML Reports

Generate detailed HTML reports with test results:

```bash
./run_tests.sh --report
```

The report includes:

- ✅ Test execution summary
- ✅ Pass/fail statistics
- ✅ Error details and stack traces
- ✅ Performance metrics
- ✅ Coverage information

### Coverage Reports

Generate code coverage reports:

```bash
./run_tests.sh --coverage
```

Coverage includes:

- ✅ Line coverage
- ✅ Branch coverage
- ✅ Function coverage
- ✅ HTML coverage report

### Console Output

Real-time test progress and results:

```
🚀 Starting User Flow Tests
📍 Base URL: http://localhost:5000
⏰ Start Time: 2024-01-15T10:30:00

📋 AuthenticationFlowTests: ✅ PASS
📋 ProviderConfigurationFlowTests: ✅ PASS
📋 DeploymentFlowTests: ✅ PASS
📋 IntegrationFlowTests: ✅ PASS

📊 Test Summary
===============
✅ Tests PASSED
⏰ Duration: 45.2s
📈 Coverage: 89.5%
```

## 🔧 Advanced Usage

### Running Specific Test Categories

```bash
# Run only authentication tests
python3 -m pytest user_flows.py::AuthenticationFlowTests -v

# Run only deployment tests
python3 -m pytest user_flows.py::DeploymentFlowTests -v

# Run specific test method
python3 -m pytest user_flows.py::AuthenticationFlowTests::test_01_user_registration_flow -v
```

### Parallel Test Execution

```bash
# Run tests in parallel (experimental)
python3 run_tests.py --parallel
```

### Custom Test Configuration

Edit `test_config.json` to customize:

- Test environment settings
- Provider configurations
- Test data
- Timeout values

### Environment Variables

Set custom environment variables:

```bash
export TEST_BASE_URL="http://localhost:5000"
export TEST_VERBOSE="true"
export TEST_COVERAGE="true"
```

## 🐛 Debugging Tests

### Verbose Output

Enable detailed logging:

```bash
./run_tests.sh --verbose
```

### Debug Mode

Run tests with debug information:

```bash
python3 run_tests.py --base-url http://localhost:5000 --verbose
```

### Mock Server Debug

Start mock server in debug mode:

```bash
python3 mock_server.py --debug
```

### Test Isolation

Each test runs in isolation with cleanup:

- ✅ Fresh user sessions
- ✅ Clean provider configurations
- ✅ Isolated deployment data
- ✅ Automatic cleanup after tests

## 📈 Continuous Integration

### GitHub Actions

Automated testing on every commit:

```yaml
name: User Flow Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd tests
          python setup_tests.py
          python mock_server.py &
          python run_tests.py --full --coverage
```

### Local CI

Run the same tests locally:

```bash
# Setup and run full test suite
python3 setup_tests.py
./start_mock_server.sh &
./run_tests.sh --full --coverage --report
```

## 📚 Documentation

### Test Scenarios

Detailed documentation of all test scenarios:

- [Test Scenarios Documentation](test_scenarios.md)

### API Documentation

Mock server API endpoints:

- [Mock Server API](mock_server.py)

### User Journeys

Complete user journey maps:

- [User Journey Documentation](test_scenarios.md#user-journey-maps)

## 🚨 Troubleshooting

### Common Issues

**Server not responding:**

```bash
# Check if mock server is running
curl http://localhost:5000/health

# Restart mock server
./start_mock_server.sh
```

**Test failures:**

```bash
# Check test logs
./run_tests.sh --verbose

# Validate test setup
python3 setup_tests.py --validate-only
```

**Dependency issues:**

```bash
# Reinstall dependencies
python3 setup_tests.py --no-deps
```

### Performance Issues

**Slow test execution:**

- Use `--quick` flag for faster tests
- Run tests in parallel with `--parallel`
- Optimize test data size

**Memory issues:**

- Reduce concurrent test count
- Clean up test data regularly
- Monitor system resources

## 🤝 Contributing

### Adding New Tests

1. **Create test class:**

```python
class NewFeatureTests(UserFlowTestBase):
    def test_new_feature(self):
        # Test implementation
        pass
```

2. **Add to test runner:**

```python
# In run_tests.py
test_classes.append(NewFeatureTests)
```

3. **Update documentation:**

- Add to test scenarios
- Update user journey maps
- Document new test data requirements

### Test Best Practices

- ✅ Use descriptive test names
- ✅ Test both success and failure scenarios
- ✅ Clean up after each test
- ✅ Use realistic test data
- ✅ Document test assumptions
- ✅ Keep tests independent

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to test methods
- Use meaningful variable names
- Keep tests focused and simple

## 📞 Support

### Getting Help

1. **Check documentation:**

   - [Test Scenarios](test_scenarios.md)
   - [Mock Server API](mock_server.py)

2. **Run validation:**

   ```bash
   python3 setup_tests.py --validate-only
   ```

3. **Check logs:**
   ```bash
   ./run_tests.sh --verbose
   ```

### Reporting Issues

When reporting test issues, include:

- Test environment details
- Error messages and stack traces
- Steps to reproduce
- Expected vs actual behavior
- Test configuration

## 📄 License

This testing suite is part of the RepoTorpedo project and follows the same license terms.

---

**Happy Testing! 🧪✨**
