"""
Non-Payment Reason Management page object for Mobinet NextGen.
Handles hierarchical reason selection, form validation, appointments, and service disconnection.
"""

import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.base_page import BasePage


class NonPaymentReasonPage(BasePage):
    """
    Page object for Non-Payment Reason Management functionality.
    Supports hierarchical reason selection, appointment scheduling, and service disconnection.
    """
    
    # Page navigation
    PAYMENT_SCREEN_MENU = (By.ID, "paymentScreenMenu")
    THREE_DOT_MENU = (By.CLASS_NAME, "three-dot-menu")
    NON_PAYMENT_REASON_LINK = (By.XPATH, "//a[contains(text(), 'Non-Payment Reason') or contains(text(), 'Trả lý do không thanh toán')]")
    
    # Main form container
    NON_PAYMENT_FORM = (By.ID, "nonPaymentReasonForm")
    
    # Hierarchical reason selection
    LEVEL1_DROPDOWN = (By.ID, "level1ReasonDropdown")
    LEVEL2_DROPDOWN = (By.ID, "level2ReasonDropdown")
    LEVEL3_DROPDOWN = (By.ID, "level3ReasonDropdown")
    
    # Form fields
    NOTES_FIELD = (By.ID, "notesTextarea")
    
    # Payment appointment scheduling
    APPOINTMENT_DATE_PICKER = (By.ID, "appointmentDatePicker")
    APPOINTMENT_TIME_PICKER = (By.ID, "appointmentTimePicker")
    APPOINTMENT_SECTION = (By.ID, "appointmentSection")
    
    # Service disconnection scheduling (Revenue Collection only)
    DISCONNECT_OPTION1_BOX = (By.ID, "disconnectOption1")
    DISCONNECT_OPTION2_BOX = (By.ID, "disconnectOption2")
    DISCONNECT_OPTION3_BOX = (By.ID, "disconnectOption3")
    
    DISCONNECT_OPTION2_SELECT = (By.ID, "disconnectOption2Select")
    DISCONNECT_DATE_PICKER = (By.ID, "disconnectDatePicker")
    DISCONNECT_STATUS_MAINTAIN = (By.ID, "disconnectStatusMaintain")
    DISCONNECT_STATUS_TEMPORARY = (By.ID, "disconnectStatusTemporary")
    
    # Form buttons
    SUBMIT_BUTTON = (By.ID, "submitReasonButton")
    CANCEL_BUTTON = (By.ID, "cancelReasonButton")
    RESET_BUTTON = (By.ID, "resetFormButton")
    
    # Validation messages
    ERROR_MESSAGES = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    VALIDATION_ERROR = (By.CLASS_NAME, "validation-error")
    
    # Loading indicators
    FORM_LOADING = (By.CLASS_NAME, "form-loading")
    DROPDOWN_LOADING = (By.CLASS_NAME, "dropdown-loading")
    
    # History section
    REASON_HISTORY_SECTION = (By.ID, "reasonHistorySection")
    HISTORY_RECORDS = (By.CLASS_NAME, "history-record")
    
    def __init__(self, driver, config_data, logger):
        """Initialize Non-Payment Reason page."""
        super().__init__(driver, config_data, logger)
        
    def navigate_to_non_payment_reason_page(self):
        """Navigate to Non-Payment Reason page from payment screen."""
        if self.logger:
            self.logger.info("Navigating to Non-Payment Reason page")
            
        try:
            # Click three-dot menu on payment screen
            self.click_element(
                self.THREE_DOT_MENU,
                description="Three-dot menu on payment screen"
            )
            
            # Click Non-Payment Reason link
            self.click_element(
                self.NON_PAYMENT_REASON_LINK,
                description="Non-Payment Reason link"
            )
            
            # Wait for page to load
            self.wait_for_non_payment_page_load()
            
            if self.logger:
                self.logger.info("Successfully navigated to Non-Payment Reason page")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to navigate to Non-Payment Reason page: {str(e)}")
            raise
            
    def wait_for_non_payment_page_load(self):
        """Wait for Non-Payment Reason page to fully load."""
        # Wait for main form container
        self.wait_helpers.wait_for_element_visible(
            self.NON_PAYMENT_FORM,
            timeout=self.long_timeout,
            description="Non-Payment Reason form container"
        )
        
        # Wait for Level 1 dropdown to be available
        self.wait_helpers.wait_for_element_visible(
            self.LEVEL1_DROPDOWN,
            timeout=self.default_timeout,
            description="Level 1 reason dropdown"
        )
        
        # Wait for any loading indicators to disappear
        self.wait_for_loading_to_complete()
        
        if self.logger:
            self.logger.info("Non-Payment Reason page loaded successfully")
            
    def select_level1_reason(self, reason_text):
        """
        Select Level 1 reason from dropdown.
        
        Args:
            reason_text (str): Text of the reason to select
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting Level 1 reason: {reason_text}")
            
        try:
            # Wait for Level 1 dropdown to be loaded with options
            self.wait_helpers.wait_for_dropdown_options_loaded(
                self.LEVEL1_DROPDOWN,
                minimum_options=1
            )
            
            success = self.select_dropdown_option(
                self.LEVEL1_DROPDOWN,
                option_text=reason_text
            )
            
            if success:
                # Wait for Level 2 dropdown to become enabled
                time.sleep(1)  # Brief pause for UI update
                
                if self.logger:
                    self.logger.info(f"Level 1 reason selected successfully: {reason_text}")
                    
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select Level 1 reason: {str(e)}")
            return False
            
    def select_level2_reason(self, reason_text):
        """
        Select Level 2 reason from dropdown.
        
        Args:
            reason_text (str): Text of the reason to select
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting Level 2 reason: {reason_text}")
            
        try:
            # Wait for Level 2 dropdown to be enabled and loaded
            self.wait_helpers.wait_for_dropdown_options_loaded(
                self.LEVEL2_DROPDOWN,
                minimum_options=1
            )
            
            success = self.select_dropdown_option(
                self.LEVEL2_DROPDOWN,
                option_text=reason_text
            )
            
            if success:
                # Wait for Level 3 dropdown to appear (if applicable)
                time.sleep(1)  # Brief pause for UI update
                
                if self.logger:
                    self.logger.info(f"Level 2 reason selected successfully: {reason_text}")
                    
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select Level 2 reason: {str(e)}")
            return False
            
    def select_level3_reason(self, reason_text):
        """
        Select Level 3 reason from dropdown.
        
        Args:
            reason_text (str): Text of the reason to select
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting Level 3 reason: {reason_text}")
            
        try:
            # Verify Level 3 dropdown is visible
            if not self.is_element_visible(self.LEVEL3_DROPDOWN, timeout=5):
                if self.logger:
                    self.logger.warning("Level 3 dropdown is not visible")
                return False
                
            # Wait for Level 3 dropdown to be loaded with options
            self.wait_helpers.wait_for_dropdown_options_loaded(
                self.LEVEL3_DROPDOWN,
                minimum_options=1
            )
            
            success = self.select_dropdown_option(
                self.LEVEL3_DROPDOWN,
                option_text=reason_text
            )
            
            if success and self.logger:
                self.logger.info(f"Level 3 reason selected successfully: {reason_text}")
                
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select Level 3 reason: {str(e)}")
            return False
            
    def enter_notes(self, notes_text):
        """
        Enter notes in the notes field.
        
        Args:
            notes_text (str): Notes text to enter
        """
        if self.logger:
            self.logger.info("Entering notes text")
            
        self.enter_text(
            self.NOTES_FIELD,
            notes_text,
            description="Notes field"
        )
        
    def select_appointment_date(self, date_str):
        """
        Select appointment date using date picker.
        
        Args:
            date_str (str): Date in YYYY-MM-DD format
            
        Returns:
            bool: True if date selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting appointment date: {date_str}")
            
        try:
            # Click date picker to open calendar
            self.click_element(
                self.APPOINTMENT_DATE_PICKER,
                description="Appointment date picker"
            )
            
            # Wait for date picker to load
            self.wait_helpers.wait_for_date_picker_loaded(
                (By.CLASS_NAME, "date-picker-calendar")
            )
            
            # Find and click the specific date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day = date_obj.day
            
            date_cell_locator = (By.XPATH, f"//td[@data-date='{date_str}' or contains(@class, 'day') and text()='{day}']")
            
            if self.is_element_visible(date_cell_locator, timeout=5):
                self.click_element(date_cell_locator, description=f"Date cell for {date_str}")
                
                if self.logger:
                    self.logger.info(f"Appointment date selected: {date_str}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"Date cell not found for: {date_str}")
                return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select appointment date: {str(e)}")
            return False
            
    def select_appointment_time(self, time_str):
        """
        Select appointment time.
        
        Args:
            time_str (str): Time in HH:MM format
            
        Returns:
            bool: True if time selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting appointment time: {time_str}")
            
        try:
            # Wait for time picker to be available
            self.wait_helpers.wait_for_element_visible(
                self.APPOINTMENT_TIME_PICKER,
                description="Appointment time picker"
            )
            
            # Enter time directly or select from picker
            success = self.select_dropdown_option(
                self.APPOINTMENT_TIME_PICKER,
                option_text=time_str
            )
            
            if success and self.logger:
                self.logger.info(f"Appointment time selected: {time_str}")
                
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select appointment time: {str(e)}")
            return False
            
    def select_disconnect_option1(self, option_text):
        """
        Select first disconnect option (Revenue Collection only).
        
        Args:
            option_text (str): Option text to select
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting disconnect option 1: {option_text}")
            
        # Verify disconnect options are visible (Revenue Collection role)
        if not self.is_element_visible(self.DISCONNECT_OPTION1_BOX, timeout=5):
            if self.logger:
                self.logger.warning("Disconnect options not visible - user may not have Revenue Collection role")
            return False
            
        try:
            success = self.select_dropdown_option(
                self.DISCONNECT_OPTION1_BOX,
                option_text=option_text
            )
            
            # If "Option 2" selected, verify second option box appears
            if success and "Option 2" in option_text:
                time.sleep(1)  # Brief pause for UI update
                option2_visible = self.is_element_visible(self.DISCONNECT_OPTION2_BOX, timeout=5)
                
                if self.logger:
                    self.logger.info(f"Second option box visible: {option2_visible}")
                    
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select disconnect option 1: {str(e)}")
            return False
            
    def select_disconnect_option2(self, option_text):
        """
        Select second disconnect option.
        
        Args:
            option_text (str): Option text to select
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting disconnect option 2: {option_text}")
            
        try:
            # Wait for second option box to be visible
            self.wait_helpers.wait_for_element_visible(
                self.DISCONNECT_OPTION2_BOX,
                description="Disconnect option 2 box"
            )
            
            success = self.select_dropdown_option(
                self.DISCONNECT_OPTION2_SELECT,
                option_text=option_text
            )
            
            # If specific date option selected, verify date picker appears
            if success and "Cancel disconnect schedule" not in option_text:
                time.sleep(1)  # Brief pause for UI update
                date_picker_visible = self.is_element_visible(self.DISCONNECT_DATE_PICKER, timeout=5)
                
                if self.logger:
                    self.logger.info(f"Disconnect date picker visible: {date_picker_visible}")
                    
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select disconnect option 2: {str(e)}")
            return False
            
    def select_disconnect_date(self, date_str):
        """
        Select disconnect date (must be between 13th and end of month, greater than current date).
        
        Args:
            date_str (str): Date in YYYY-MM-DD format
            
        Returns:
            bool: True if date selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting disconnect date: {date_str}")
            
        # Validate date meets business rules
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            current_date = datetime.now()
            
            # Check if date is in the future
            if date_obj <= current_date:
                if self.logger:
                    self.logger.error(f"Disconnect date must be greater than current date: {date_str}")
                return False
                
            # Check if date is between 13th and end of month
            if date_obj.day < 13:
                if self.logger:
                    self.logger.error(f"Disconnect date must be between 13th and end of month: {date_str}")
                return False
                
        except ValueError:
            if self.logger:
                self.logger.error(f"Invalid date format: {date_str}")
            return False
            
        try:
            # Click disconnect date picker
            self.click_element(
                self.DISCONNECT_DATE_PICKER,
                description="Disconnect date picker"
            )
            
            # Wait for date picker to load
            self.wait_helpers.wait_for_date_picker_loaded(
                (By.CLASS_NAME, "date-picker-calendar")
            )
            
            # Select the specific date
            day = date_obj.day
            date_cell_locator = (By.XPATH, f"//td[@data-date='{date_str}' or contains(@class, 'day') and text()='{day}']")
            
            if self.is_element_visible(date_cell_locator, timeout=5):
                self.click_element(date_cell_locator, description=f"Disconnect date cell for {date_str}")
                
                # Wait for third option box to appear
                time.sleep(1)
                option3_visible = self.is_element_visible(self.DISCONNECT_OPTION3_BOX, timeout=5)
                
                if self.logger:
                    self.logger.info(f"Disconnect date selected: {date_str}, Third option box visible: {option3_visible}")
                    
                return True
            else:
                if self.logger:
                    self.logger.error(f"Disconnect date cell not found for: {date_str}")
                return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select disconnect date: {str(e)}")
            return False
            
    def select_disconnect_status(self, status):
        """
        Select disconnect status (Maintain or Temporary).
        
        Args:
            status (str): "Maintain" or "Temporary"
            
        Returns:
            bool: True if selection was successful
        """
        if self.logger:
            self.logger.info(f"Selecting disconnect status: {status}")
            
        try:
            # Wait for third option box to be visible
            self.wait_helpers.wait_for_element_visible(
                self.DISCONNECT_OPTION3_BOX,
                description="Disconnect option 3 box (status selection)"
            )
            
            if status.lower() == "maintain":
                self.click_element(
                    self.DISCONNECT_STATUS_MAINTAIN,
                    description="Maintain status option"
                )
            elif status.lower() == "temporary":
                self.click_element(
                    self.DISCONNECT_STATUS_TEMPORARY,
                    description="Temporary status option"
                )
            else:
                if self.logger:
                    self.logger.error(f"Invalid disconnect status: {status}")
                return False
                
            if self.logger:
                self.logger.info(f"Disconnect status selected: {status}")
                
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to select disconnect status: {str(e)}")
            return False
            
    def submit_form(self):
        """
        Submit the non-payment reason form.
        
        Returns:
            bool: True if submission was successful
        """
        if self.logger:
            self.logger.info("Submitting non-payment reason form")
            
        try:
            # Click submit button
            self.click_element(
                self.SUBMIT_BUTTON,
                description="Submit form button"
            )
            
            # Wait for form processing
            self.wait_for_form_submission()
            
            # Check for success or error messages
            success = self.is_form_submission_successful()
            
            if success and self.logger:
                self.logger.info("Form submitted successfully")
            elif self.logger:
                error_msg = self.get_validation_errors()
                self.logger.error(f"Form submission failed: {error_msg}")
                
            return success
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to submit form: {str(e)}")
            return False
            
    def wait_for_form_submission(self):
        """Wait for form submission processing to complete."""
        # Wait for any loading indicators
        if self.is_element_visible(self.FORM_LOADING, timeout=2):
            self.wait_helpers.wait_for_element_to_disappear(
                self.FORM_LOADING,
                timeout=self.long_timeout
            )
            
        # Wait for AJAX completion
        self.wait_helpers.wait_for_ajax_complete()
        
        # Additional brief pause for UI updates
        time.sleep(2)
        
    def is_form_submission_successful(self):
        """
        Check if form submission was successful.
        
        Returns:
            bool: True if submission was successful
        """
        # Look for success message
        success_visible = self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        
        # Check if we're redirected to history page
        history_visible = self.is_element_visible(self.REASON_HISTORY_SECTION, timeout=5)
        
        # Verify no validation errors present
        no_errors = not self.has_validation_errors()
        
        return success_visible or (history_visible and no_errors)
        
    def has_validation_errors(self):
        """
        Check if form has validation errors.
        
        Returns:
            bool: True if validation errors are present
        """
        return (self.is_element_visible(self.ERROR_MESSAGES, timeout=3) or 
                self.is_element_visible(self.VALIDATION_ERROR, timeout=3))
        
    def get_validation_errors(self):
        """
        Get validation error messages.
        
        Returns:
            list: List of error messages
        """
        error_messages = []
        
        try:
            error_elements = self.find_elements(self.ERROR_MESSAGES, timeout=3)
            for element in error_elements:
                if element.is_displayed():
                    error_messages.append(element.text.strip())
                    
            validation_elements = self.find_elements(self.VALIDATION_ERROR, timeout=3)
            for element in validation_elements:
                if element.is_displayed():
                    error_messages.append(element.text.strip())
                    
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not retrieve error messages: {str(e)}")
                
        return error_messages
        
    def get_all_level1_options(self):
        """Get all available Level 1 reason options."""
        return self.get_all_dropdown_options(self.LEVEL1_DROPDOWN)
        
    def get_all_level2_options(self):
        """Get all available Level 2 reason options."""
        return self.get_all_dropdown_options(self.LEVEL2_DROPDOWN)
        
    def get_all_level3_options(self):
        """Get all available Level 3 reason options."""
        if self.is_element_visible(self.LEVEL3_DROPDOWN, timeout=3):
            return self.get_all_dropdown_options(self.LEVEL3_DROPDOWN)
        return []
        
    def is_level3_dropdown_visible(self):
        """Check if Level 3 dropdown is visible."""
        return self.is_element_visible(self.LEVEL3_DROPDOWN, timeout=3)
        
    def is_disconnect_options_visible(self):
        """Check if disconnect options are visible (Revenue Collection role check)."""
        return self.is_element_visible(self.DISCONNECT_OPTION1_BOX, timeout=3)
        
    def reset_form(self):
        """Reset the form to initial state."""
        if self.logger:
            self.logger.info("Resetting form")
            
        try:
            self.click_element(
                self.RESET_BUTTON,
                description="Reset form button"
            )
            
            # Brief pause for form reset
            time.sleep(1)
            
            if self.logger:
                self.logger.info("Form reset successfully")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to reset form: {str(e)}")
                
    def cancel_form(self):
        """Cancel form and return to previous screen."""
        if self.logger:
            self.logger.info("Cancelling form")
            
        try:
            self.click_element(
                self.CANCEL_BUTTON,
                description="Cancel form button"
            )
            
            if self.logger:
                self.logger.info("Form cancelled successfully")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to cancel form: {str(e)}")
                
    def get_reason_history_records(self):
        """
        Get historical non-payment reason records.
        
        Returns:
            list: List of history record elements
        """
        try:
            if self.is_element_visible(self.REASON_HISTORY_SECTION, timeout=5):
                return self.find_elements(self.HISTORY_RECORDS, timeout=5)
            return []
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not retrieve history records: {str(e)}")
            return []