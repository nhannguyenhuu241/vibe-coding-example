#!/usr/bin/env python3
"""
Test execution script for Mobinet NextGen automation framework.
Provides convenient test execution with various options and configurations.
"""

import argparse
import os
import sys
import subprocess
import yaml
from pathlib import Path


def load_config():
    """Load test configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    
    if not config_path.exists():
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_directories():
    """Create necessary directories for test execution."""
    directories = [
        "reports/html",
        "reports/allure-results", 
        "reports/json",
        "logs",
        "screenshots"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def build_pytest_command(args, config):
    """Build pytest command based on arguments and configuration."""
    cmd = ["python", "-m", "pytest"]
    
    # Test selection
    if args.test_file:
        cmd.append(args.test_file)
    elif args.test_class:
        cmd.append(f"-k {args.test_class}")
    elif args.test_method:
        cmd.append(f"-k {args.test_method}")
        
    # Markers
    if args.markers:
        cmd.extend(["-m", args.markers])
        
    # Verbosity
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
        
    # Parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
        
    # Browser configuration
    if args.browser:
        os.environ["SELENIUM_BROWSER"] = args.browser
        
    if args.headless:
        os.environ["HEADLESS"] = "true"
        
    # Reporting
    if args.html_report:
        cmd.extend(["--html", f"reports/html/{args.html_report}"])
        cmd.append("--self-contained-html")
        
    if args.allure:
        cmd.extend(["--alluredir", "reports/allure-results"])
        
    if args.json_report:
        cmd.extend(["--json-report", "--json-report-file", f"reports/json/{args.json_report}"])
        
    # Failure handling
    if args.maxfail:
        cmd.extend(["--maxfail", str(args.maxfail)])
        
    if args.fail_fast:
        cmd.append("-x")
        
    # Additional options
    if args.capture:
        cmd.append("--capture=no")
        
    if args.durations:
        cmd.extend(["--durations", str(args.durations)])
        
    return cmd


def run_smoke_tests(config):
    """Run smoke test suite."""
    print("🚀 Running Smoke Tests...")
    
    cmd = [
        "python", "-m", "pytest",
        "-m", "smoke",
        "--html", "reports/html/smoke_test_report.html",
        "--self-contained-html",
        "-v"
    ]
    
    return subprocess.run(cmd)


def run_regression_tests(config):
    """Run regression test suite."""
    print("🔄 Running Regression Tests...")
    
    cmd = [
        "python", "-m", "pytest", 
        "-m", "not performance",
        "--html", "reports/html/regression_test_report.html",
        "--self-contained-html",
        "--maxfail", "5",
        "-v"
    ]
    
    return subprocess.run(cmd)


def run_performance_tests(config):
    """Run performance test suite."""
    print("⚡ Running Performance Tests...")
    
    cmd = [
        "python", "-m", "pytest",
        "-m", "performance", 
        "--html", "reports/html/performance_test_report.html",
        "--self-contained-html",
        "--durations", "10",
        "-v"
    ]
    
    return subprocess.run(cmd)


def run_integration_tests(config):
    """Run integration test suite."""
    print("🔗 Running Integration Tests...")
    
    cmd = [
        "python", "-m", "pytest",
        "tests/test_integration.py",
        "--html", "reports/html/integration_test_report.html", 
        "--self-contained-html",
        "-v", "-s"
    ]
    
    return subprocess.run(cmd)


def generate_allure_report():
    """Generate and serve Allure report."""
    print("📊 Generating Allure Report...")
    
    # Generate report
    subprocess.run([
        "allure", "generate", 
        "reports/allure-results", 
        "-o", "reports/allure-report",
        "--clean"
    ])
    
    # Serve report
    print("🌐 Serving Allure Report at http://localhost:8080")
    subprocess.run(["allure", "serve", "reports/allure-results"])


def main():
    """Main test execution function."""
    parser = argparse.ArgumentParser(
        description="Mobinet NextGen Test Automation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --smoke                           # Run smoke tests
  %(prog)s --regression                      # Run regression suite
  %(prog)s --performance                     # Run performance tests
  %(prog)s --integration                     # Run integration tests
  
  %(prog)s -m hierarchical                   # Run hierarchical reason tests
  %(prog)s -m "smoke and not slow"           # Run smoke tests excluding slow ones
  
  %(prog)s --file tests/test_validation.py   # Run specific test file
  %(prog)s --class TestFormValidation        # Run specific test class
  %(prog)s --method test_mandatory_fields    # Run specific test method
  
  %(prog)s --browser firefox --headless      # Run with Firefox headless
  %(prog)s --parallel 4                      # Run with 4 parallel workers
  
  %(prog)s --html report.html --allure       # Generate HTML and Allure reports
        """
    )
    
    # Test suites
    suite_group = parser.add_argument_group('Test Suites')
    suite_group.add_argument('--smoke', action='store_true', 
                            help='Run smoke test suite')
    suite_group.add_argument('--regression', action='store_true',
                            help='Run regression test suite')  
    suite_group.add_argument('--performance', action='store_true',
                            help='Run performance test suite')
    suite_group.add_argument('--integration', action='store_true',
                            help='Run integration test suite')
    
    # Test selection
    selection_group = parser.add_argument_group('Test Selection')
    selection_group.add_argument('--file', dest='test_file',
                                help='Run specific test file')
    selection_group.add_argument('--class', dest='test_class',
                                help='Run specific test class')
    selection_group.add_argument('--method', dest='test_method', 
                                help='Run specific test method')
    selection_group.add_argument('-m', '--markers', dest='markers',
                                help='Run tests with specific markers')
    
    # Browser configuration
    browser_group = parser.add_argument_group('Browser Configuration')
    browser_group.add_argument('--browser', choices=['chrome', 'firefox', 'edge'],
                              default='chrome', help='Browser to use for testing')
    browser_group.add_argument('--headless', action='store_true',
                              help='Run browser in headless mode')
    
    # Execution options
    execution_group = parser.add_argument_group('Execution Options')
    execution_group.add_argument('--parallel', type=int,
                                help='Number of parallel workers')
    execution_group.add_argument('--maxfail', type=int, default=10,
                                help='Stop after N failures')
    execution_group.add_argument('--fail-fast', action='store_true',
                                help='Stop on first failure')
    execution_group.add_argument('--durations', type=int, default=10,
                                help='Show N slowest test durations')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('-v', '--verbose', action='store_true',
                             help='Verbose output')
    output_group.add_argument('-q', '--quiet', action='store_true', 
                             help='Quiet output')
    output_group.add_argument('--capture', action='store_true',
                             help='Don\'t capture stdout/stderr')
    
    # Reporting
    reporting_group = parser.add_argument_group('Reporting Options')
    reporting_group.add_argument('--html', dest='html_report',
                                help='Generate HTML report with filename')
    reporting_group.add_argument('--allure', action='store_true',
                                help='Generate Allure report data')
    reporting_group.add_argument('--json', dest='json_report', 
                                help='Generate JSON report with filename')
    reporting_group.add_argument('--serve-allure', action='store_true',
                                help='Generate and serve Allure report')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Create necessary directories
    create_directories()
    
    # Handle special cases
    if args.serve_allure:
        generate_allure_report()
        return
    
    # Execute test suites
    if args.smoke:
        result = run_smoke_tests(config)
    elif args.regression:
        result = run_regression_tests(config)
    elif args.performance:
        result = run_performance_tests(config) 
    elif args.integration:
        result = run_integration_tests(config)
    else:
        # Build and execute custom pytest command
        cmd = build_pytest_command(args, config)
        print(f"🧪 Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd)
    
    # Generate Allure report if requested
    if args.allure and not args.serve_allure:
        print("📊 Allure results generated in: reports/allure-results")
        print("To view report, run: allure serve reports/allure-results")
    
    # Exit with test result code
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()