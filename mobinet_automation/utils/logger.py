"""
Logging utility for Mobinet NextGen automation framework.
Provides centralized logging configuration with color coding and file output.
"""

import logging
import colorlog
import os
from datetime import datetime


def setup_logger(name="mobinet_automation", level=logging.INFO):
    """
    Setup logger with color formatting for console and file output.
    
    Args:
        name (str): Logger name
        level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = colorlog.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Console handler with color formatting
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)
    
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler for persistent logging
    timestamp = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(f"logs/automation_{timestamp}.log", encoding='utf-8')
    file_handler.setLevel(level)
    
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


class TestLogger:
    """
    Test-specific logger wrapper with additional functionality for automation.
    """
    
    def __init__(self, test_name, logger=None):
        """
        Initialize test logger.
        
        Args:
            test_name (str): Name of the test
            logger: Parent logger instance
        """
        self.test_name = test_name
        self.logger = logger or setup_logger()
        
    def step(self, message):
        """Log a test step with special formatting."""
        self.logger.info(f"[STEP] {self.test_name}: {message}")
        
    def verification(self, message):
        """Log a verification point."""
        self.logger.info(f"[VERIFY] {self.test_name}: {message}")
        
    def data(self, message):
        """Log test data information."""
        self.logger.debug(f"[DATA] {self.test_name}: {message}")
        
    def action(self, message):
        """Log user actions."""
        self.logger.info(f"[ACTION] {self.test_name}: {message}")
        
    def result(self, message, passed=True):
        """Log test result."""
        status = "PASS" if passed else "FAIL"
        log_method = self.logger.info if passed else self.logger.error
        log_method(f"[{status}] {self.test_name}: {message}")
        
    def performance(self, action, duration):
        """Log performance metrics."""
        self.logger.info(f"[PERFORMANCE] {self.test_name}: {action} completed in {duration:.2f} seconds")
        
    def error(self, message, exception=None):
        """Log errors with optional exception details."""
        error_msg = f"[ERROR] {self.test_name}: {message}"
        if exception:
            error_msg += f" - Exception: {str(exception)}"
        self.logger.error(error_msg)
        
    def warning(self, message):
        """Log warnings."""
        self.logger.warning(f"[WARNING] {self.test_name}: {message}")
        
    def debug(self, message):
        """Log debug information."""
        self.logger.debug(f"[DEBUG] {self.test_name}: {message}")


def log_test_start(test_name):
    """Log test start with separator for clarity."""
    logger = setup_logger()
    logger.info("=" * 80)
    logger.info(f"STARTING TEST: {test_name}")
    logger.info("=" * 80)
    return TestLogger(test_name, logger)


def log_test_end(test_name, passed=True):
    """Log test end with result."""
    logger = setup_logger()
    status = "PASSED" if passed else "FAILED"
    logger.info("=" * 80)
    logger.info(f"TEST {status}: {test_name}")
    logger.info("=" * 80)