#!/usr/bin/env python3
"""
User Flow Test Runner
=====================

This script runs comprehensive user flow tests for the RepoTorpedo application.
It tests all possible user journeys and interactions with the application.

Usage:
    python3 run_tests.py [options]

Options:
    --base-url URL     Base URL for the application (default: http://localhost:5000)
    --parallel         Run tests in parallel (experimental)
    --verbose          Verbose output
    --report           Generate HTML report
    --coverage         Run with coverage analysis
    --quick            Run only critical tests
    --full             Run all tests including performance and security
"""

import sys
import os
import argparse
import time
import json
from datetime import datetime
from typing import List, Dict, Any
import subprocess
import tempfile

# Add parent directory to path to import user_flows
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_flows import run_user_flow_tests, UserFlowTestBase
import unittest


class TestRunner:
    """Test runner with reporting and configuration"""
    
    def __init__(self, base_url: str = "http://localhost:5000", verbose: bool = False):
        self.base_url = base_url
        self.verbose = verbose
        self.results = {
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'test_results': [],
            'summary': {}
        }
    
    def run_tests(self, test_categories: List[str] = None) -> bool:
        """Run user flow tests"""
        print(f"🚀 Starting User Flow Tests")
        print(f"📍 Base URL: {self.base_url}")
        print(f"⏰ Start Time: {self.results['start_time']}")
        print("=" * 60)
        
        # Set environment variable for base URL
        os.environ['TEST_BASE_URL'] = self.base_url
        
        # Run tests
        success = run_user_flow_tests()
        
        # Record end time
        self.results['end_time'] = datetime.now().isoformat()
        
        return success
    
    def run_quick_tests(self) -> bool:
        """Run only critical tests"""
        print("🏃 Running Quick Tests (Critical Paths Only)")
        
        # Define critical test categories
        critical_tests = [
            'AuthenticationFlowTests',
            'ProviderConfigurationFlowTests',
            'DeploymentFlowTests',
            'IntegrationFlowTests'
        ]
        
        return self.run_tests(critical_tests)
    
    def run_full_tests(self) -> bool:
        """Run all tests including performance and security"""
        print("🔬 Running Full Test Suite (All Tests)")
        
        # Run all test categories
        all_tests = [
            'AuthenticationFlowTests',
            'ProviderConfigurationFlowTests',
            'DeploymentFlowTests',
            'DeploymentStatusFlowTests',
            'CustomDomainFlowTests',
            'ErrorHandlingFlowTests',
            'PerformanceFlowTests',
            'SecurityFlowTests',
            'IntegrationFlowTests'
        ]
        
        return self.run_tests(all_tests)
    
    def run_with_coverage(self) -> bool:
        """Run tests with coverage analysis"""
        print("📊 Running Tests with Coverage Analysis")
        
        try:
            # Check if coverage is installed
            import coverage
        except ImportError:
            print("❌ Coverage not installed. Install with: pip install coverage")
            return False
        
        # Initialize coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        success = self.run_full_tests()
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        print("\n📈 Coverage Report:")
        cov.report()
        
        # Generate HTML report
        cov.html_report(directory='htmlcov')
        print("📁 HTML coverage report generated in 'htmlcov' directory")
        
        return success
    
    def generate_html_report(self, output_file: str = "test_report.html"):
        """Generate HTML test report"""
        print(f"📄 Generating HTML report: {output_file}")
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Flow Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
                .summary { display: flex; gap: 20px; margin: 20px 0; }
                .summary-item { background: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }
                .test-result { margin: 10px 0; padding: 10px; border-radius: 3px; }
                .passed { background: #d4edda; border-left: 4px solid #28a745; }
                .failed { background: #f8d7da; border-left: 4px solid #dc3545; }
                .error { background: #fff3cd; border-left: 4px solid #ffc107; }
                .timestamp { color: #666; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 User Flow Test Report</h1>
                <p class="timestamp">Generated: {timestamp}</p>
                <p>Base URL: {base_url}</p>
            </div>
            
            <div class="summary">
                <div class="summary-item">
                    <h3>Total Tests</h3>
                    <p>{total_tests}</p>
                </div>
                <div class="summary-item">
                    <h3>Passed</h3>
                    <p style="color: #28a745;">{passed}</p>
                </div>
                <div class="summary-item">
                    <h3>Failed</h3>
                    <p style="color: #dc3545;">{failed}</p>
                </div>
                <div class="summary-item">
                    <h3>Errors</h3>
                    <p style="color: #ffc107;">{errors}</p>
                </div>
            </div>
            
            <h2>Test Results</h2>
            {test_results}
        </body>
        </html>
        """
        
        # Generate test results HTML
        test_results_html = ""
        for result in self.results.get('test_results', []):
            status_class = result.get('status', 'unknown')
            test_results_html += f"""
            <div class="test-result {status_class}">
                <h4>{result.get('test_name', 'Unknown Test')}</h4>
                <p><strong>Status:</strong> {result.get('status', 'Unknown')}</p>
                <p><strong>Duration:</strong> {result.get('duration', 'Unknown')}s</p>
                {f'<p><strong>Error:</strong> {result.get("error", "")}</p>' if result.get('error') else ''}
            </div>
            """
        
        # Fill template
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            base_url=self.base_url,
            total_tests=self.results.get('total_tests', 0),
            passed=self.results.get('passed', 0),
            failed=self.results.get('failed', 0),
            errors=self.results.get('errors', 0),
            test_results=test_results_html
        )
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"✅ HTML report generated: {output_file}")
    
    def run_parallel_tests(self) -> bool:
        """Run tests in parallel (experimental)"""
        print("⚡ Running Tests in Parallel (Experimental)")
        
        # This is a simplified parallel implementation
        # In production, you might want to use multiprocessing or threading
        
        import threading
        import queue
        
        # Define test categories
        test_categories = [
            'AuthenticationFlowTests',
            'ProviderConfigurationFlowTests',
            'DeploymentFlowTests',
            'DeploymentStatusFlowTests',
            'CustomDomainFlowTests',
            'ErrorHandlingFlowTests',
            'PerformanceFlowTests',
            'SecurityFlowTests',
            'IntegrationFlowTests'
        ]
        
        results_queue = queue.Queue()
        
        def run_test_category(category):
            """Run a single test category"""
            try:
                # Create test suite for category
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromName(f'user_flows.{category}')
                
                # Run tests
                runner = unittest.TextTestRunner(verbosity=1, stream=open(os.devnull, 'w'))
                result = runner.run(suite)
                
                results_queue.put({
                    'category': category,
                    'success': result.wasSuccessful(),
                    'tests_run': result.testsRun,
                    'failures': len(result.failures),
                    'errors': len(result.errors)
                })
            except Exception as e:
                results_queue.put({
                    'category': category,
                    'success': False,
                    'error': str(e)
                })
        
        # Start threads
        threads = []
        for category in test_categories:
            thread = threading.Thread(target=run_test_category, args=(category,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        all_success = True
        while not results_queue.empty():
            result = results_queue.get()
            print(f"📋 {result['category']}: {'✅ PASS' if result['success'] else '❌ FAIL'}")
            if not result['success']:
                all_success = False
        
        return all_success


def check_server_health(base_url: str) -> bool:
    """Check if the server is running and healthy"""
    try:
        import requests
        response = requests.get(f"{base_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run User Flow Tests")
    parser.add_argument("--base-url", default="http://localhost:5000", 
                       help="Base URL for the application")
    parser.add_argument("--parallel", action="store_true", 
                       help="Run tests in parallel (experimental)")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--report", action="store_true", 
                       help="Generate HTML report")
    parser.add_argument("--coverage", action="store_true", 
                       help="Run with coverage analysis")
    parser.add_argument("--quick", action="store_true", 
                       help="Run only critical tests")
    parser.add_argument("--full", action="store_true", 
                       help="Run all tests including performance and security")
    
    args = parser.parse_args()
    
    # Check server health
    print("🔍 Checking server health...")
    if not check_server_health(args.base_url):
        print(f"❌ Server not responding at {args.base_url}")
        print("💡 Make sure the server is running: python3 server/main.py")
        return 1
    
    print("✅ Server is healthy")
    
    # Initialize test runner
    runner = TestRunner(base_url=args.base_url, verbose=args.verbose)
    
    # Run tests based on options
    success = False
    
    if args.parallel:
        success = runner.run_parallel_tests()
    elif args.coverage:
        success = runner.run_with_coverage()
    elif args.quick:
        success = runner.run_quick_tests()
    elif args.full:
        success = runner.run_full_tests()
    else:
        # Default: run quick tests
        success = runner.run_quick_tests()
    
    # Generate report if requested
    if args.report:
        runner.generate_html_report()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"✅ Tests {'PASSED' if success else 'FAILED'}")
    print(f"⏰ Duration: {runner.results.get('end_time', 'Unknown')}")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 