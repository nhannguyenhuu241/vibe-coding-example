"""
Login page object for Mobinet NextGen authentication.
Handles user authentication with different roles and error scenarios.
"""

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for login functionality.
    Supports different user roles and authentication scenarios.
    """
    
    # Login page locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginButton")
    LOGOUT_BUTTON = (By.ID, "logoutButton")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    LOADING_INDICATOR = (By.CLASS_NAME, "loading-spinner")
    
    # Post-login elements
    USER_MENU = (By.ID, "userMenu")
    USER_NAME_DISPLAY = (By.CLASS_NAME, "user-name")
    ROLE_DISPLAY = (By.CLASS_NAME, "user-role")
    DASHBOARD_CONTAINER = (By.ID, "dashboardContainer")
    
    def __init__(self, driver, config_data, logger):
        """
        Initialize login page.
        
        Args:
            driver: WebDriver instance
            config_data (dict): Configuration data
            logger: Logger instance
        """
        super().__init__(driver, config_data, logger)
        self.base_url = config_data.get('environment', {}).get('base_url', '')
        
    def navigate_to_login_page(self):
        """Navigate to the login page."""
        login_url = f"{self.base_url}/login"
        
        if self.logger:
            self.logger.info(f"Navigating to login page: {login_url}")
            
        self.driver.get(login_url)
        
        # Wait for page to load
        self.wait_for_loading_to_complete()
        
        # Verify we're on the login page
        assert self.is_element_visible(self.LOGIN_BUTTON, timeout=10), \
            "Login page did not load properly - login button not visible"
            
        if self.logger:
            self.logger.info("Successfully navigated to login page")
            
    def enter_username(self, username):
        """
        Enter username in the username field.
        
        Args:
            username (str): Username to enter
        """
        if self.logger:
            self.logger.debug(f"Entering username: {username}")
            
        self.enter_text(
            self.USERNAME_INPUT, 
            username, 
            description="Username field"
        )
        
    def enter_password(self, password):
        """
        Enter password in the password field.
        
        Args:
            password (str): Password to enter
        """
        if self.logger:
            self.logger.debug("Entering password (masked)")
            
        self.enter_text(
            self.PASSWORD_INPUT, 
            password, 
            description="Password field"
        )
        
    def click_login_button(self):
        """Click the login button."""
        if self.logger:
            self.logger.debug("Clicking login button")
            
        self.click_element(
            self.LOGIN_BUTTON, 
            description="Login button"
        )
        
        # Wait for login processing
        self.wait_for_login_processing()
        
    def wait_for_login_processing(self):
        """Wait for login processing to complete."""
        # Wait for loading indicator to appear and disappear
        if self.is_element_visible(self.LOADING_INDICATOR, timeout=2):
            self.wait_helpers.wait_for_element_to_disappear(
                self.LOADING_INDICATOR, 
                timeout=30
            )
            
        # Additional wait for page transition
        time.sleep(2)
        
    def login(self, username, password):
        """
        Perform complete login process.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if login was successful
        """
        if self.logger:
            self.logger.info(f"Attempting login with username: {username}")
            
        try:
            # Navigate to login page if not already there
            if not self.is_element_visible(self.LOGIN_BUTTON, timeout=3):
                self.navigate_to_login_page()
                
            # Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Click login
            self.click_login_button()
            
            # Check for success
            if self.is_login_successful():
                if self.logger:
                    self.logger.info(f"Login successful for user: {username}")
                return True
            else:
                error_message = self.get_error_message()
                if self.logger:
                    self.logger.error(f"Login failed for user: {username}. Error: {error_message}")
                return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Login process failed: {str(e)}")
            if self.screenshot_helper:
                self.screenshot_helper.take_screenshot(
                    description=f"Login failure - {username}"
                )
            return False
            
    def login_with_role(self, role_name):
        """
        Login with specific role using configured credentials.
        
        Args:
            role_name (str): Role name (e.g., 'revenue_collection', 'customer_care')
            
        Returns:
            bool: True if login was successful
        """
        users_config = self.config_data.get('users', {})
        user_config = users_config.get(role_name)
        
        if not user_config:
            if self.logger:
                self.logger.error(f"No configuration found for role: {role_name}")
            return False
            
        return self.login(
            user_config.get('username'),
            user_config.get('password')
        )
        
    def is_login_successful(self):
        """
        Check if login was successful by looking for post-login elements.
        
        Returns:
            bool: True if login was successful
        """
        # Check for dashboard or user menu
        dashboard_visible = self.is_element_visible(self.DASHBOARD_CONTAINER, timeout=10)
        user_menu_visible = self.is_element_visible(self.USER_MENU, timeout=5)
        
        # Check that we're not still on login page
        login_button_hidden = not self.is_element_visible(self.LOGIN_BUTTON, timeout=3)
        
        success = (dashboard_visible or user_menu_visible) and login_button_hidden
        
        if self.logger:
            self.logger.debug(f"Login success check - Dashboard: {dashboard_visible}, "
                            f"User Menu: {user_menu_visible}, Login Hidden: {login_button_hidden}")
            
        return success
        
    def get_error_message(self):
        """
        Get error message displayed on login failure.
        
        Returns:
            str: Error message text or empty string if no error
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
                return self.get_element_text(self.ERROR_MESSAGE)
            return ""
        except:
            return ""
            
    def get_logged_in_user_info(self):
        """
        Get information about the currently logged-in user.
        
        Returns:
            dict: User information including name and role
        """
        user_info = {
            'username': '',
            'role': '',
            'is_logged_in': False
        }
        
        try:
            if self.is_element_visible(self.USER_NAME_DISPLAY, timeout=5):
                user_info['username'] = self.get_element_text(self.USER_NAME_DISPLAY)
                user_info['is_logged_in'] = True
                
            if self.is_element_visible(self.ROLE_DISPLAY, timeout=3):
                user_info['role'] = self.get_element_text(self.ROLE_DISPLAY)
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not retrieve user info: {str(e)}")
                
        return user_info
        
    def logout(self):
        """
        Log out the current user.
        
        Returns:
            bool: True if logout was successful
        """
        if self.logger:
            self.logger.info("Attempting to logout")
            
        try:
            # Look for logout button
            if self.is_element_visible(self.LOGOUT_BUTTON, timeout=5):
                self.click_element(self.LOGOUT_BUTTON, description="Logout button")
                
                # Wait for redirect to login page
                login_visible = self.is_element_visible(self.LOGIN_BUTTON, timeout=10)
                
                if login_visible:
                    if self.logger:
                        self.logger.info("Logout successful")
                    return True
                    
            # Alternative logout through user menu
            if self.is_element_visible(self.USER_MENU, timeout=5):
                self.click_element(self.USER_MENU, description="User menu")
                
                # Look for logout option in dropdown
                logout_option = (By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
                if self.is_element_visible(logout_option, timeout=3):
                    self.click_element(logout_option, description="Logout option")
                    
                    # Wait for redirect to login page
                    login_visible = self.is_element_visible(self.LOGIN_BUTTON, timeout=10)
                    
                    if login_visible:
                        if self.logger:
                            self.logger.info("Logout successful via user menu")
                        return True
                        
            if self.logger:
                self.logger.warning("Logout button/option not found")
            return False
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Logout failed: {str(e)}")
            return False
            
    def verify_user_role_access(self, expected_role):
        """
        Verify that the logged-in user has the expected role.
        
        Args:
            expected_role (str): Expected role name
            
        Returns:
            bool: True if user has expected role
        """
        user_info = self.get_logged_in_user_info()
        
        if not user_info['is_logged_in']:
            if self.logger:
                self.logger.error("User is not logged in")
            return False
            
        actual_role = user_info['role'].lower()
        expected_role_lower = expected_role.lower()
        
        role_match = expected_role_lower in actual_role or actual_role in expected_role_lower
        
        if self.logger:
            self.logger.debug(f"Role verification - Expected: {expected_role}, "
                            f"Actual: {user_info['role']}, Match: {role_match}")
            
        return role_match
        
    def clear_login_form(self):
        """Clear username and password fields."""
        if self.logger:
            self.logger.debug("Clearing login form")
            
        try:
            if self.is_element_present(self.USERNAME_INPUT):
                username_field = self.find_element(self.USERNAME_INPUT)
                username_field.clear()
                
            if self.is_element_present(self.PASSWORD_INPUT):
                password_field = self.find_element(self.PASSWORD_INPUT)
                password_field.clear()
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not clear login form: {str(e)}")
                
    def is_on_login_page(self):
        """
        Check if currently on the login page.
        
        Returns:
            bool: True if on login page
        """
        return (self.is_element_visible(self.LOGIN_BUTTON, timeout=3) and 
                self.is_element_visible(self.USERNAME_INPUT, timeout=3) and
                self.is_element_visible(self.PASSWORD_INPUT, timeout=3))
                
    def wait_for_login_page_load(self):
        """Wait for login page to fully load."""
        self.wait_for_loading_to_complete()
        
        # Verify essential login elements are present
        assert self.is_element_visible(self.USERNAME_INPUT, timeout=10), \
            "Username input not visible"
        assert self.is_element_visible(self.PASSWORD_INPUT, timeout=10), \
            "Password input not visible"
        assert self.is_element_visible(self.LOGIN_BUTTON, timeout=10), \
            "Login button not visible"
            
        if self.logger:
            self.logger.info("Login page loaded successfully")