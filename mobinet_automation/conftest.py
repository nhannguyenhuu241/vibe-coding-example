"""
Pytest configuration file for Mobinet NextGen automation tests.
Provides shared fixtures, hooks, and configuration for all test modules.
"""

import pytest
import yaml
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import setup_logger
from utils.screenshot_helper import ScreenshotHelper
from pages.login_page import LoginPage


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create reports directory
    os.makedirs("reports/html", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)


@pytest.fixture(scope="session")
def config_data():
    """Load configuration data from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="session") 
def logger():
    """Setup logger for test execution."""
    return setup_logger()


@pytest.fixture(scope="function")
def driver(config_data, logger, request):
    """
    Initialize WebDriver instance based on configuration.
    Supports Chrome and Firefox browsers with configurable options.
    """
    browser_config = config_data['browser']
    browser_name = browser_config['name'].lower()
    
    logger.info(f"Initializing {browser_name} browser")
    
    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            if browser_config['headless']:
                options.add_argument("--headless=new")
            options.add_argument(f"--window-size={browser_config['window_size']}")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = ChromeService(ChromeDriverManager().install())
            driver_instance = webdriver.Chrome(service=service, options=options)
            
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if browser_config['headless']:
                options.add_argument("--headless")
            options.add_argument(f"--width={browser_config['window_size'].split(',')[0]}")
            options.add_argument(f"--height={browser_config['window_size'].split(',')[1]}")
            
            service = FirefoxService(GeckoDriverManager().install())
            driver_instance = webdriver.Firefox(service=service, options=options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Configure timeouts
        driver_instance.implicitly_wait(browser_config['implicit_wait'])
        driver_instance.set_page_load_timeout(browser_config['page_load_timeout'])
        
        # Navigate to base URL
        driver_instance.get(config_data['environment']['base_url'])
        logger.info(f"Navigated to: {config_data['environment']['base_url']}")
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Failed to initialize driver: {str(e)}")
        raise
    
    finally:
        if 'driver_instance' in locals():
            logger.info("Closing browser")
            driver_instance.quit()


@pytest.fixture(scope="function")
def screenshot_helper(driver, logger):
    """Provides screenshot functionality for test evidence."""
    return ScreenshotHelper(driver, logger)


@pytest.fixture(scope="function") 
def login_page(driver, config_data, logger):
    """Initialize login page object."""
    return LoginPage(driver, config_data, logger)


@pytest.fixture(scope="function")
def revenue_user_session(driver, config_data, login_page, logger):
    """
    Provides authenticated session with Revenue Collection role.
    Automatically logs in with revenue collection credentials.
    """
    user_config = config_data['users']['revenue_collection']
    
    logger.info(f"Logging in as Revenue Collection user: {user_config['username']}")
    
    login_page.login(user_config['username'], user_config['password'])
    
    # Verify successful login
    assert login_page.is_login_successful(), "Revenue Collection user login failed"
    
    logger.info("Revenue Collection user login successful")
    return driver


@pytest.fixture(scope="function")
def customer_care_session(driver, config_data, login_page, logger):
    """
    Provides authenticated session with Customer Care role.
    Automatically logs in with customer care credentials.
    """
    user_config = config_data['users']['customer_care']
    
    logger.info(f"Logging in as Customer Care user: {user_config['username']}")
    
    login_page.login(user_config['username'], user_config['password'])
    
    # Verify successful login  
    assert login_page.is_login_successful(), "Customer Care user login failed"
    
    logger.info("Customer Care user login successful")
    return driver


@pytest.fixture(scope="function")
def test_contracts(config_data):
    """Provides test contract data for test scenarios."""
    return config_data['test_data']['contracts']


@pytest.fixture(scope="function")
def reason_hierarchy_data(config_data):
    """Provides hierarchical reason test data."""
    return config_data['test_data']['reasons']


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failures.
    Executed after each test to determine outcome.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Access driver from the test
        driver = None
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver')
        
        if driver:
            # Generate screenshot filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace(" ", "_").replace("::", "_")
            screenshot_path = f"screenshots/FAILED_{test_name}_{timestamp}.png"
            
            try:
                driver.save_screenshot(screenshot_path)
                # Attach screenshot to Allure report if available
                try:
                    import allure
                    allure.attach.file(screenshot_path, 
                                     name=f"Failed Test Screenshot - {test_name}",
                                     attachment_type=allure.attachment_type.PNG)
                except ImportError:
                    pass  # Allure not available, skip attachment
                    
            except Exception as e:
                logging.error(f"Failed to capture screenshot: {str(e)}")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test names.
    This helps organize tests by functionality.
    """
    for item in items:
        # Add markers based on test file/function names
        if "hierarchical" in item.name.lower():
            item.add_marker(pytest.mark.hierarchical)
        if "validation" in item.name.lower():
            item.add_marker(pytest.mark.validation)
        if "performance" in item.name.lower():
            item.add_marker(pytest.mark.performance)
        if "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        if "security" in item.name.lower():
            item.add_marker(pytest.mark.security)
        if "role" in item.name.lower():
            item.add_marker(pytest.mark.rbac)


# Custom markers for test organization
def pytest_configure(config):
    """Register custom markers for test organization."""
    config.addinivalue_line("markers", "hierarchical: Tests for hierarchical reason selection")
    config.addinivalue_line("markers", "validation: Tests for form validation")
    config.addinivalue_line("markers", "performance: Tests for performance requirements") 
    config.addinivalue_line("markers", "integration: Tests for external system integration")
    config.addinivalue_line("markers", "security: Tests for security and access control")
    config.addinivalue_line("markers", "rbac: Tests for role-based access control")
    config.addinivalue_line("markers", "smoke: Smoke tests for critical functionality")
    config.addinivalue_line("markers", "regression: Regression tests for existing functionality")


# Performance monitoring fixture
@pytest.fixture(scope="function")
def performance_monitor():
    """Monitor performance metrics during test execution."""
    import psutil
    import time
    
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    yield
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    execution_time = end_time - start_time
    memory_usage = end_memory - start_memory
    
    # Log performance metrics
    logging.info(f"Test execution time: {execution_time:.2f} seconds")
    logging.info(f"Memory usage change: {memory_usage / 1024 / 1024:.2f} MB")


# Test data cleanup fixture
@pytest.fixture(scope="function", autouse=True)
def test_data_cleanup(logger):
    """Cleanup test data before and after each test."""
    logger.info("Starting test data cleanup")
    
    yield
    
    logger.info("Finalizing test data cleanup")