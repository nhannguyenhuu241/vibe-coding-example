# Mobinet NextGen - Non-Payment Reason Management Test Automation

This repository contains comprehensive Selenium WebDriver automation scripts for the Mobinet NextGen Non-Payment Reason Management module. The automation framework follows the Page Object Model pattern and includes extensive test coverage for all functional requirements.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Coverage](#test-coverage)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Contributing](#contributing)

## 🔍 Overview

This automation framework provides end-to-end testing for the Mobinet NextGen Non-Payment Reason Management module, covering:

- **Hierarchical Reason Selection**: Level 1, 2, and 3 reason management
- **Form Validation**: Comprehensive field validation and error handling
- **Appointment Scheduling**: Date/time picker functionality and business rules
- **Role-Based Access Control**: Revenue Collection vs Customer Care permissions
- **Service Disconnection**: Revenue Collection specific disconnection scheduling
- **External System Integration**: Customer Debt Management, Customer Management, and Customer Care Platform synchronization
- **Performance Testing**: Response time validation and load testing
- **Security Testing**: Input validation and access control verification

## 📊 Test Coverage

### Functional Tests
- ✅ **TC-001**: Hierarchical Reason Management (Level 1, 2, 3 selection logic)
- ✅ **TC-002**: Form Validation (mandatory fields, notes validation, special characters)
- ✅ **TC-003**: Payment Appointment Scheduling (date restrictions, time selection)
- ✅ **TC-004**: Service Disconnection Scheduling (Revenue Collection only)
- ✅ **TC-005**: Role-Based Access Control (feature visibility by role)

### Integration Tests
- ✅ **TC-006**: External System Synchronization (3 external systems)
- ✅ **TC-007**: Data Mapping and Field Population (automatic field mapping)

### Performance Tests
- ✅ **TC-008**: Response Time Requirements (< 2s for reason loading, < 3s for submission)

### Security Tests
- ✅ **TC-009**: Access Control and Authorization
- ✅ **TC-010**: Audit Trail and Change Tracking

### Error Handling Tests
- ✅ **TC-011**: Validation Error Handling
- ✅ **TC-012**: Data Consistency and Recovery

## 🏗️ Architecture

### Page Object Model Structure
```
pages/
├── base_page.py              # Common page functionality
├── login_page.py             # Authentication page object
└── non_payment_reason_page.py # Main functionality page object
```

### Test Organization
```
tests/
├── test_hierarchical_reason_management.py  # TC-001: Reason hierarchy tests
├── test_form_validation.py                 # TC-002: Form validation tests
├── test_appointment_scheduling.py          # TC-003: Appointment tests
├── test_role_based_access.py              # TC-004, TC-005: RBAC and disconnect tests
└── test_integration.py                     # TC-006, TC-007: Integration tests
```

### Utilities
```
utils/
├── logger.py              # Advanced logging with test steps
├── screenshot_helper.py   # Screenshot and test evidence capture
├── wait_helpers.py        # Enhanced wait conditions
└── test_data_manager.py   # Test data generation and management
```

### Configuration
```
config/
└── config.yaml            # Environment, browser, and test data configuration
```

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **Browser**: Chrome 90+, Firefox 80+, or Edge 90+
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space

### External Dependencies
- **Selenium WebDriver**: Automated via webdriver-manager
- **Java**: JDK 8+ (for Allure reporting)
- **Internet Connection**: Required for WebDriver downloads and external system testing

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd mobinet_automation
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Allure (Optional - for enhanced reporting)
```bash
# Windows (with Scoop)
scoop install allure

# macOS
brew install allure

# Linux
sudo apt-get install allure
```

## ⚙️ Configuration

### Environment Configuration
Edit `config/config.yaml` to match your environment:

```yaml
environment:
  base_url: "https://your-mobinet-staging.example.com"
  api_base_url: "https://api.your-mobinet-staging.example.com"

users:
  revenue_collection:
    username: "your_revenue_user@company.com"
    password: "your_password"
  customer_care:
    username: "your_care_user@company.com"
    password: "your_password"
```

### Browser Configuration
```yaml
browser:
  name: "chrome"          # chrome, firefox, edge
  headless: false         # Set to true for CI/CD
  window_size: "1920,1080"
```

### Test Data Configuration
```yaml
test_data:
  contracts:
    valid_contract_id: "CON001234567"
    overdue_contract_id: "CON987654321"
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Smoke tests only
pytest -m smoke

# Hierarchical reason tests
pytest -m hierarchical

# Form validation tests
pytest -m validation

# Performance tests
pytest -m performance

# Integration tests
pytest -m integration

# Role-based access control tests
pytest -m rbac
```

### Run Specific Test Files
```bash
# Hierarchical reason management tests
pytest tests/test_hierarchical_reason_management.py

# Form validation tests
pytest tests/test_form_validation.py

# Appointment scheduling tests
pytest tests/test_appointment_scheduling.py
```

### Run with Different Browsers
```bash
# Chrome (default)
pytest

# Firefox
pytest --browser=firefox

# Headless mode
pytest --headless
```

### Parallel Execution
```bash
# Run tests in parallel (4 workers)
pytest -n 4

# Run specific tests in parallel
pytest -m smoke -n 2
```

## 📊 Test Reports

### HTML Reports
```bash
pytest --html=reports/html/report.html --self-contained-html
```

### Allure Reports
```bash
# Run tests with Allure
pytest --alluredir=reports/allure-results

# Generate and serve Allure report
allure generate reports/allure-results -o reports/allure-report
allure serve reports/allure-results
```

### JSON Reports
```bash
pytest --json-report --json-report-file=reports/json/report.json
```

## 🔍 Test Execution Examples

### Basic Smoke Test Run
```bash
pytest -m smoke -v --html=reports/smoke_test.html
```

### Comprehensive Regression Test
```bash
pytest -m "not performance" --maxfail=5 --tb=short
```

### Performance Test Suite
```bash
pytest -m performance --durations=10
```

### Integration Test with Verbose Output
```bash
pytest tests/test_integration.py -v -s --capture=no
```

## 📁 Project Structure

```
mobinet_automation/
├── config/
│   └── config.yaml                 # Test configuration
├── pages/
│   ├── __init__.py
│   ├── base_page.py               # Base page object
│   ├── login_page.py              # Login page object
│   └── non_payment_reason_page.py # Main functionality page
├── tests/
│   ├── __init__.py
│   ├── test_hierarchical_reason_management.py
│   ├── test_form_validation.py
│   ├── test_appointment_scheduling.py
│   ├── test_role_based_access.py
│   └── test_integration.py
├── utils/
│   ├── __init__.py
│   ├── logger.py                  # Logging utilities
│   ├── screenshot_helper.py       # Screenshot management
│   ├── wait_helpers.py           # Wait conditions
│   └── test_data_manager.py      # Test data management
├── reports/                       # Test reports (auto-generated)
├── screenshots/                   # Test screenshots (auto-generated)
├── logs/                         # Test logs (auto-generated)
├── conftest.py                   # PyTest configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Troubleshooting

### Common Issues

#### WebDriver Issues
```bash
# Clear WebDriver cache
rm -rf ~/.cache/selenium/

# Reinstall webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager
```

#### Test Failures
1. **Element not found**: Check if page loaded completely
2. **Timeout errors**: Increase wait times in config
3. **Authentication failures**: Verify user credentials in config
4. **Integration test failures**: Ensure external systems are accessible

#### Performance Issues
- Use headless mode for faster execution
- Reduce implicit wait times for development
- Run tests in parallel with fewer workers

### Debug Mode
```bash
# Run with maximum verbosity and no capture
pytest -vvv -s --capture=no --tb=long

# Run single test with debug
pytest tests/test_hierarchical_reason_management.py::TestHierarchicalReasonManagement::test_level1_reason_selection -vvv -s
```

## 📈 Continuous Integration

### GitHub Actions Example
```yaml
name: Mobinet Automation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest -m smoke --html=reports/ci_report.html
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: reports/
```

## 🤝 Contributing

### Code Standards
- Follow PEP 8 Python style guidelines
- Use type hints where applicable
- Add comprehensive docstrings
- Include test coverage for new features

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Create Pull Request

### Adding New Tests
1. Follow existing test structure and naming conventions
2. Use appropriate pytest markers
3. Include test documentation and expected results
4. Add test data to `test_data_manager.py` if needed

## 📞 Support

For questions, issues, or contributions:

- **Documentation**: Check this README and code comments
- **Issues**: Create GitHub issues for bugs or feature requests
- **Testing**: Run `pytest --collect-only` to verify test discovery

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: 2025-09-10  
**Version**: 1.0.0  
**Compatibility**: Mobinet NextGen v2.0+