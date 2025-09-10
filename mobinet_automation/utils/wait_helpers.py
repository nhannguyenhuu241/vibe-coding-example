"""
Enhanced wait utilities for robust element interactions.
Provides custom wait conditions and retry mechanisms for Mobinet automation.
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    StaleElementReferenceException, 
    NoSuchElementException,
    ElementNotInteractableException
)


class WaitHelpers:
    """
    Advanced wait utilities for reliable test automation.
    Includes custom conditions specific to Mobinet NextGen functionality.
    """
    
    def __init__(self, driver, default_timeout=20, logger=None):
        """
        Initialize wait helpers.
        
        Args:
            driver: WebDriver instance
            default_timeout (int): Default timeout in seconds
            logger: Logger instance
        """
        self.driver = driver
        self.default_timeout = default_timeout
        self.logger = logger
        
    def wait_for_element_visible(self, locator, timeout=None, description=""):
        """
        Wait for element to be visible.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            description (str): Description for logging
            
        Returns:
            WebElement: The visible element
        """
        timeout = timeout or self.default_timeout
        
        try:
            if self.logger:
                self.logger.debug(f"Waiting for element visible: {locator} - {description}")
                
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            
            if self.logger:
                self.logger.debug(f"Element found and visible: {locator}")
                
            return element
            
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for visible element: {locator} - {description}")
            raise TimeoutException(f"Element not visible within {timeout} seconds: {locator}")
            
    def wait_for_element_clickable(self, locator, timeout=None, description=""):
        """
        Wait for element to be clickable.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            description (str): Description for logging
            
        Returns:
            WebElement: The clickable element
        """
        timeout = timeout or self.default_timeout
        
        try:
            if self.logger:
                self.logger.debug(f"Waiting for element clickable: {locator} - {description}")
                
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            
            if self.logger:
                self.logger.debug(f"Element found and clickable: {locator}")
                
            return element
            
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for clickable element: {locator} - {description}")
            raise TimeoutException(f"Element not clickable within {timeout} seconds: {locator}")
            
    def wait_for_dropdown_options_loaded(self, dropdown_locator, minimum_options=1, timeout=None):
        """
        Wait for dropdown options to be loaded.
        
        Args:
            dropdown_locator (tuple): Locator for the dropdown container
            minimum_options (int): Minimum number of options expected
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if options are loaded
        """
        timeout = timeout or self.default_timeout
        
        def dropdown_options_loaded(driver):
            try:
                dropdown = driver.find_element(*dropdown_locator)
                options = dropdown.find_elements(By.TAG_NAME, "option")
                return len(options) >= minimum_options
            except:
                return False
                
        try:
            WebDriverWait(self.driver, timeout).until(dropdown_options_loaded)
            if self.logger:
                self.logger.debug(f"Dropdown options loaded: {dropdown_locator}")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for dropdown options: {dropdown_locator}")
            return False
            
    def wait_for_text_in_element(self, locator, expected_text, timeout=None):
        """
        Wait for specific text to appear in an element.
        
        Args:
            locator (tuple): (By strategy, locator string)
            expected_text (str): Text to wait for
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if text is found
        """
        timeout = timeout or self.default_timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, expected_text)
            )
            if self.logger:
                self.logger.debug(f"Text '{expected_text}' found in element: {locator}")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for text '{expected_text}' in element: {locator}")
            return False
            
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        Wait for element to disappear from DOM or become invisible.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if element disappeared
        """
        timeout = timeout or self.default_timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            if self.logger:
                self.logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for element to disappear: {locator}")
            return False
            
    def wait_for_page_load_complete(self, timeout=None):
        """
        Wait for page to fully load (document.readyState === 'complete').
        
        Args:
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if page is loaded
        """
        timeout = timeout or self.default_timeout
        
        def page_loaded(driver):
            return driver.execute_script("return document.readyState") == "complete"
            
        try:
            WebDriverWait(self.driver, timeout).until(page_loaded)
            if self.logger:
                self.logger.debug("Page load completed")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error("Timeout waiting for page load completion")
            return False
            
    def wait_for_ajax_complete(self, timeout=None):
        """
        Wait for AJAX requests to complete (jQuery.active === 0).
        
        Args:
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if AJAX is complete
        """
        timeout = timeout or self.default_timeout
        
        def ajax_complete(driver):
            try:
                return driver.execute_script("return jQuery.active == 0")
            except:
                # jQuery not available, assume AJAX is complete
                return True
                
        try:
            WebDriverWait(self.driver, timeout).until(ajax_complete)
            if self.logger:
                self.logger.debug("AJAX requests completed")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error("Timeout waiting for AJAX completion")
            return False
            
    def retry_on_stale_element(self, func, max_attempts=3, delay=1):
        """
        Retry function execution on stale element reference exceptions.
        
        Args:
            func: Function to execute
            max_attempts (int): Maximum retry attempts
            delay (int): Delay between retries in seconds
            
        Returns:
            Any: Function return value
        """
        for attempt in range(max_attempts):
            try:
                return func()
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    if self.logger:
                        self.logger.warning(f"Stale element reference, retrying ({attempt + 1}/{max_attempts})")
                    time.sleep(delay)
                else:
                    if self.logger:
                        self.logger.error("Max retry attempts reached for stale element")
                    raise
                    
    def wait_for_hierarchical_dropdown_enabled(self, level1_locator, level2_locator, level3_locator=None, timeout=None):
        """
        Wait for hierarchical dropdown structure to be properly enabled.
        Specific to Mobinet's reason hierarchy functionality.
        
        Args:
            level1_locator (tuple): Level 1 dropdown locator
            level2_locator (tuple): Level 2 dropdown locator  
            level3_locator (tuple): Level 3 dropdown locator (optional)
            timeout (int): Custom timeout (optional)
            
        Returns:
            dict: Status of each dropdown level
        """
        timeout = timeout or self.default_timeout
        
        def hierarchical_dropdowns_ready(driver):
            try:
                result = {
                    'level1_enabled': False,
                    'level2_enabled': False,
                    'level3_enabled': False
                }
                
                # Check Level 1
                level1 = driver.find_element(*level1_locator)
                result['level1_enabled'] = level1.is_enabled()
                
                # Check Level 2 - should be enabled after Level 1 selection
                try:
                    level2 = driver.find_element(*level2_locator)
                    result['level2_enabled'] = level2.is_enabled()
                except NoSuchElementException:
                    result['level2_enabled'] = False
                    
                # Check Level 3 if provided - should be enabled after Level 2 selection
                if level3_locator:
                    try:
                        level3 = driver.find_element(*level3_locator)
                        result['level3_enabled'] = level3.is_enabled()
                    except NoSuchElementException:
                        result['level3_enabled'] = False
                        
                return result
            except:
                return None
                
        try:
            result = WebDriverWait(self.driver, timeout).until(
                lambda driver: hierarchical_dropdowns_ready(driver) is not None
            )
            
            if self.logger:
                self.logger.debug(f"Hierarchical dropdowns status: {result}")
                
            return result
            
        except TimeoutException:
            if self.logger:
                self.logger.error("Timeout waiting for hierarchical dropdowns")
            return None
            
    def wait_for_date_picker_loaded(self, date_picker_locator, timeout=None):
        """
        Wait for date picker component to be fully loaded and interactive.
        
        Args:
            date_picker_locator (tuple): Date picker container locator
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if date picker is loaded
        """
        timeout = timeout or self.default_timeout
        
        def date_picker_loaded(driver):
            try:
                picker = driver.find_element(*date_picker_locator)
                # Check if picker is visible and has clickable elements
                if not picker.is_displayed():
                    return False
                    
                # Look for common date picker elements
                date_elements = picker.find_elements(By.CSS_SELECTOR, 
                    "[class*='date'], [class*='day'], [class*='calendar']")
                return len(date_elements) > 0
            except:
                return False
                
        try:
            WebDriverWait(self.driver, timeout).until(date_picker_loaded)
            if self.logger:
                self.logger.debug(f"Date picker loaded: {date_picker_locator}")
            return True
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Timeout waiting for date picker: {date_picker_locator}")
            return False