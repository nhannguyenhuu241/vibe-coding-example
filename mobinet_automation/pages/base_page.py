"""
Base page object model for Mobinet NextGen automation.
Provides common functionality shared across all page objects.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException
)
from utils.wait_helpers import WaitHelpers
from utils.screenshot_helper import ScreenshotHelper


class BasePage:
    """
    Base page class containing common functionality for all page objects.
    Implements the Page Object Model pattern with enhanced error handling.
    """
    
    def __init__(self, driver, config_data=None, logger=None):
        """
        Initialize base page.
        
        Args:
            driver: WebDriver instance
            config_data (dict): Configuration data from YAML
            logger: Logger instance
        """
        self.driver = driver
        self.config_data = config_data or {}
        self.logger = logger
        self.wait_helpers = WaitHelpers(driver, logger=logger)
        self.screenshot_helper = ScreenshotHelper(driver, logger) if logger else None
        
        # Default timeout values
        self.default_timeout = config_data.get('browser', {}).get('explicit_wait', 20) if config_data else 20
        self.short_timeout = 5
        self.long_timeout = 30
        
    def find_element(self, locator, timeout=None, description=""):
        """
        Enhanced element finding with wait and error handling.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            description (str): Description for logging
            
        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.default_timeout
        
        try:
            if self.logger:
                self.logger.debug(f"Finding element: {locator} - {description}")
                
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            
            return element
            
        except TimeoutException:
            if self.logger:
                self.logger.error(f"Element not found: {locator} - {description}")
            if self.screenshot_helper:
                self.screenshot_helper.take_screenshot(
                    description=f"Element not found: {description}"
                )
            raise NoSuchElementException(f"Element not found: {locator}")
            
    def find_elements(self, locator, timeout=None):
        """
        Find multiple elements with wait.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            
        Returns:
            list: List of WebElements
        """
        timeout = timeout or self.default_timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
            
    def click_element(self, locator, timeout=None, description=""):
        """
        Click element with enhanced error handling and retry logic.
        
        Args:
            locator (tuple): (By strategy, locator string)
            timeout (int): Custom timeout (optional)
            description (str): Description for logging
        """
        timeout = timeout or self.default_timeout
        
        def click_action():
            element = self.wait_helpers.wait_for_element_clickable(
                locator, timeout, description
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll completion
            
            # Try regular click first
            try:
                element.click()
                if self.logger:
                    self.logger.debug(f"Clicked element: {locator} - {description}")
            except ElementNotInteractableException:
                # Fallback to JavaScript click
                if self.logger:
                    self.logger.warning(f"Regular click failed, using JavaScript: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
                
        # Retry on stale element
        self.wait_helpers.retry_on_stale_element(click_action)
        
    def enter_text(self, locator, text, clear_first=True, timeout=None, description=""):
        """
        Enter text in element with validation.
        
        Args:
            locator (tuple): (By strategy, locator string)
            text (str): Text to enter
            clear_first (bool): Clear field before entering text
            timeout (int): Custom timeout (optional)
            description (str): Description for logging
        """
        timeout = timeout or self.default_timeout
        
        def enter_text_action():
            element = self.wait_helpers.wait_for_element_visible(
                locator, timeout, description
            )
            
            if clear_first:
                element.clear()
                
            element.send_keys(text)
            
            # Verify text was entered
            entered_text = element.get_attribute("value")
            if entered_text != text:
                if self.logger:
                    self.logger.warning(f"Text verification failed. Expected: '{text}', Got: '{entered_text}'")
                    
            if self.logger:
                self.logger.debug(f"Entered text '{text}' in element: {locator} - {description}")
                
        self.wait_helpers.retry_on_stale_element(enter_text_action)
        
    def select_dropdown_option(self, dropdown_locator, option_value=None, option_text=None, timeout=None):
        """
        Select option from dropdown by value or visible text.
        
        Args:
            dropdown_locator (tuple): Dropdown element locator
            option_value (str): Option value to select (optional)
            option_text (str): Option text to select (optional)
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if selection was successful
        """
        timeout = timeout or self.default_timeout
        
        try:
            dropdown_element = self.wait_helpers.wait_for_element_visible(
                dropdown_locator, timeout
            )
            
            select = Select(dropdown_element)
            
            if option_value:
                select.select_by_value(option_value)
                if self.logger:
                    self.logger.debug(f"Selected dropdown option by value: {option_value}")
            elif option_text:
                select.select_by_visible_text(option_text)
                if self.logger:
                    self.logger.debug(f"Selected dropdown option by text: {option_text}")
            else:
                raise ValueError("Either option_value or option_text must be provided")
                
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select dropdown option: {str(e)}")
            return False
            
    def get_element_text(self, locator, timeout=None):
        """
        Get text content from element.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
            
        Returns:
            str: Element text content
        """
        timeout = timeout or self.default_timeout
        
        try:
            element = self.wait_helpers.wait_for_element_visible(locator, timeout)
            return element.text.strip()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get element text: {str(e)}")
            return ""
            
    def is_element_visible(self, locator, timeout=None):
        """
        Check if element is visible on the page.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if element is visible
        """
        timeout = timeout or self.short_timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except:
            return False
            
    def is_element_present(self, locator, timeout=None):
        """
        Check if element is present in DOM.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if element is present
        """
        timeout = timeout or self.short_timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False
            
    def wait_for_page_title(self, expected_title, timeout=None):
        """
        Wait for page title to match expected value.
        
        Args:
            expected_title (str): Expected page title
            timeout (int): Custom timeout (optional)
            
        Returns:
            bool: True if title matches
        """
        timeout = timeout or self.default_timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_contains(expected_title)
            )
            if self.logger:
                self.logger.debug(f"Page title contains: {expected_title}")
            return True
        except TimeoutException:
            if self.logger:
                current_title = self.driver.title
                self.logger.error(f"Page title mismatch. Expected: '{expected_title}', Got: '{current_title}'")
            return False
            
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll element into view.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
        """
        timeout = timeout or self.default_timeout
        
        try:
            element = self.wait_helpers.wait_for_element_visible(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll completion
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to scroll to element: {str(e)}")
                
    def hover_over_element(self, locator, timeout=None):
        """
        Hover over element to trigger hover effects.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout (optional)
        """
        timeout = timeout or self.default_timeout
        
        try:
            element = self.wait_helpers.wait_for_element_visible(locator, timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(0.5)  # Brief pause for hover effects
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to hover over element: {str(e)}")
                
    def get_current_url(self):
        """Get current page URL."""
        return self.driver.current_url
        
    def get_page_title(self):
        """Get current page title."""
        return self.driver.title
        
    def refresh_page(self):
        """Refresh current page."""
        self.driver.refresh()
        if self.logger:
            self.logger.debug("Page refreshed")
            
    def navigate_back(self):
        """Navigate back in browser history."""
        self.driver.back()
        if self.logger:
            self.logger.debug("Navigated back")
            
    def switch_to_frame(self, frame_locator):
        """Switch to iframe or frame."""
        try:
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
            if self.logger:
                self.logger.debug(f"Switched to frame: {frame_locator}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to switch to frame: {str(e)}")
                
    def switch_to_default_content(self):
        """Switch back to main page content from frame."""
        self.driver.switch_to.default_content()
        if self.logger:
            self.logger.debug("Switched to default content")
            
    def take_screenshot(self, description=""):
        """Take screenshot for test evidence."""
        if self.screenshot_helper:
            return self.screenshot_helper.take_screenshot(description=description)
        return None
        
    def wait_for_loading_to_complete(self, loading_locator=None, timeout=None):
        """
        Wait for loading indicators to disappear.
        
        Args:
            loading_locator (tuple): Loading indicator locator (optional)
            timeout (int): Custom timeout (optional)
        """
        timeout = timeout or self.default_timeout
        
        # Wait for page load completion
        self.wait_helpers.wait_for_page_load_complete(timeout)
        
        # Wait for AJAX completion
        self.wait_helpers.wait_for_ajax_complete(timeout)
        
        # Wait for custom loading indicator to disappear
        if loading_locator:
            self.wait_helpers.wait_for_element_to_disappear(loading_locator, timeout)
            
    def get_all_dropdown_options(self, dropdown_locator, timeout=None):
        """
        Get all options from a dropdown.
        
        Args:
            dropdown_locator (tuple): Dropdown element locator
            timeout (int): Custom timeout (optional)
            
        Returns:
            list: List of option texts
        """
        timeout = timeout or self.default_timeout
        
        try:
            dropdown_element = self.wait_helpers.wait_for_element_visible(
                dropdown_locator, timeout
            )
            
            select = Select(dropdown_element)
            options = select.options
            
            return [option.text.strip() for option in options if option.text.strip()]
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get dropdown options: {str(e)}")
            return []