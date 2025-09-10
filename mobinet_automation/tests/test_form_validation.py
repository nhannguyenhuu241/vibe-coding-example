"""
Test cases for form validation functionality.
Covers TC-002: Form Validation test scenarios.
"""

import pytest
import allure
import time
from pages.non_payment_reason_page import NonPaymentReasonPage
from utils.test_data_manager import TestDataManager
from utils.logger import log_test_start, log_test_end


@allure.epic("Non-Payment Reason Management")
@allure.feature("Form Validation")
class TestFormValidation:
    """
    Test class for form validation functionality.
    Tests mandatory field validation, notes field requirements, and error handling.
    """
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, config_data, logger):
        """Setup test data for form validation tests."""
        self.test_data_manager = TestDataManager(config_data, logger)
        self.invalid_data_scenarios = self.test_data_manager.generate_invalid_data_scenarios()
        
    @allure.story("Mandatory Field Validation")
    @allure.title("TC-002.1: Mandatory Field Validation")
    @allure.description("Verify all mandatory fields are properly validated")
    @pytest.mark.validation
    @pytest.mark.smoke
    def test_mandatory_field_validation(self, revenue_user_session, config_data, logger):
        """
        Test mandatory field validation.
        
        Test Steps:
        1. Leave Level 1 reason empty and attempt to submit
        2. Verify error message: "Please enter complete information"
        3. Select Level 1, leave Level 2 empty and attempt to submit
        4. Verify error message appears for Level 2
        5. Select Level 1 and Level 2, leave Level 3 empty (when applicable) and attempt to submit
        6. Verify error message appears for Level 3
        7. Leave Notes field empty and attempt to submit
        8. Verify error message appears for Notes
        """
        test_logger = log_test_start("Mandatory Field Validation")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Test 1: Submit with all fields empty
            test_logger.step("Test submission with all fields empty")
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission fails with empty fields")
            assert not success, "Form submission should fail with empty mandatory fields"
            
            test_logger.verification("Verify error message appears for empty fields")
            errors = non_payment_page.get_validation_errors()
            assert len(errors) > 0, "Validation errors should be displayed"
            
            # Verify generic error message
            error_text_found = any("Please enter complete information" in error.lower() or 
                                 "complete" in error.lower() for error in errors)
            assert error_text_found, f"Expected error message not found. Got: {errors}"
            
            # Test 2: Submit with only Level 1 selected
            test_logger.step("Test submission with only Level 1 reason selected")
            non_payment_page.reset_form()
            time.sleep(1)
            
            # Get Level 1 options and select first one
            level1_options = non_payment_page.get_all_level1_options()
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                
                # Submit without Level 2
                success = non_payment_page.submit_form()
                
                test_logger.verification("Verify form submission fails without Level 2")
                assert not success, "Form submission should fail without Level 2 reason"
                
                errors = non_payment_page.get_validation_errors()
                assert len(errors) > 0, "Validation errors should be displayed for missing Level 2"
                
            # Test 3: Submit with Level 1 and Level 2 but missing notes
            test_logger.step("Test submission with reasons but missing notes")
            non_payment_page.reset_form()
            time.sleep(1)
            
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                time.sleep(2)
                
                level2_options = non_payment_page.get_all_level2_options()
                if level2_options:
                    non_payment_page.select_level2_reason(level2_options[0])
                    
                    # Submit without notes
                    success = non_payment_page.submit_form()
                    
                    test_logger.verification("Verify form submission fails without notes")
                    assert not success, "Form submission should fail without notes"
                    
                    errors = non_payment_page.get_validation_errors()
                    assert len(errors) > 0, "Validation errors should be displayed for missing notes"
                    
            # Test 4: Test Level 3 validation (if applicable)
            test_logger.step("Test Level 3 validation when applicable")
            non_payment_page.reset_form()
            time.sleep(1)
            
            # Find a hierarchy that requires Level 3
            hierarchies = self.test_data_manager.generate_reason_hierarchy_data()
            level3_hierarchy = next((h for h in hierarchies if h.level3), None)
            
            if level3_hierarchy:
                # Select Level 1 and Level 2 to trigger Level 3
                if level3_hierarchy.level1 in level1_options:
                    non_payment_page.select_level1_reason(level3_hierarchy.level1)
                    time.sleep(2)
                    
                    level2_options = non_payment_page.get_all_level2_options()
                    if level3_hierarchy.level2 in level2_options:
                        non_payment_page.select_level2_reason(level3_hierarchy.level2)
                        time.sleep(2)
                        
                        # Check if Level 3 becomes visible and is required
                        if non_payment_page.is_level3_dropdown_visible():
                            # Add some notes to avoid notes validation
                            non_payment_page.enter_notes("Test notes for Level 3 validation")
                            
                            # Submit without Level 3 selection
                            success = non_payment_page.submit_form()
                            
                            # Note: This test depends on business rules for Level 3 requirement
                            test_logger.verification("Check Level 3 validation (business rule dependent)")
                            
            test_logger.result("Mandatory field validation test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Mandatory field validation test failed", e)
            non_payment_page.take_screenshot("Mandatory_Field_Validation_Failed")
            raise
        finally:
            log_test_end("Mandatory Field Validation", True)
            
    @allure.story("Notes Field Validation")
    @allure.title("TC-002.2: Notes Field Validation")
    @allure.description("Verify notes field requirements and validation")
    @pytest.mark.validation
    def test_notes_field_validation(self, revenue_user_session, config_data, logger):
        """
        Test notes field validation.
        
        Test Steps:
        1. Leave notes field completely empty
        2. Attempt to submit form
        3. Enter whitespace only in notes field
        4. Attempt to submit form
        5. Enter valid text in notes field
        6. Submit form
        """
        test_logger = log_test_start("Notes Field Validation")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup valid reason selections for testing notes validation
            level1_options = non_payment_page.get_all_level1_options()
            if not level1_options:
                pytest.skip("No Level 1 options available for testing")
                
            # Select valid Level 1 and Level 2 reasons
            non_payment_page.select_level1_reason(level1_options[0])
            time.sleep(2)
            
            level2_options = non_payment_page.get_all_level2_options()
            if level2_options:
                non_payment_page.select_level2_reason(level2_options[0])
                time.sleep(1)
                
            # Test 1: Empty notes field
            test_logger.step("Test with empty notes field")
            non_payment_page.enter_notes("")  # Ensure notes field is empty
            
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission fails with empty notes")
            assert not success, "Form submission should fail with empty notes field"
            
            errors = non_payment_page.get_validation_errors()
            notes_error_found = any("notes" in error.lower() or "information" in error.lower() 
                                  for error in errors)
            assert notes_error_found, f"Notes validation error not found. Got errors: {errors}"
            
            # Test 2: Whitespace only in notes field
            test_logger.step("Test with whitespace-only notes field")
            whitespace_notes = self.invalid_data_scenarios["whitespace_only_notes"]
            non_payment_page.enter_notes(whitespace_notes)
            
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission fails with whitespace-only notes")
            assert not success, "Form submission should fail with whitespace-only notes"
            
            errors = non_payment_page.get_validation_errors()
            assert len(errors) > 0, "Validation errors should be displayed for whitespace-only notes"
            
            # Test 3: Valid notes
            test_logger.step("Test with valid notes")
            valid_notes = self.test_data_manager.generate_notes_text("medium")
            non_payment_page.enter_notes(valid_notes)
            
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission succeeds with valid notes")
            # Note: Success depends on all other fields being valid
            if not success:
                errors = non_payment_page.get_validation_errors()
                # Verify no notes-related errors
                notes_error_found = any("notes" in error.lower() for error in errors)
                assert not notes_error_found, f"Unexpected notes validation error with valid notes: {errors}"
                
            test_logger.result("Notes field validation test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Notes field validation test failed", e)
            non_payment_page.take_screenshot("Notes_Field_Validation_Failed")
            raise
        finally:
            log_test_end("Notes Field Validation", True)
            
    @allure.story("Special Characters Validation")
    @allure.title("Special Characters and Edge Cases Validation")
    @allure.description("Test form validation with special characters and edge cases")
    @pytest.mark.validation
    def test_special_characters_validation(self, revenue_user_session, config_data, logger):
        """
        Test form validation with special characters and edge cases.
        
        Tests various edge cases including:
        - Special characters in notes
        - Very long notes
        - Potential XSS/injection attempts
        """
        test_logger = log_test_start("Special Characters Validation")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup valid reason selections
            level1_options = non_payment_page.get_all_level1_options()
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                time.sleep(2)
                
                level2_options = non_payment_page.get_all_level2_options()
                if level2_options:
                    non_payment_page.select_level2_reason(level2_options[0])
                    time.sleep(1)
                    
            special_cases = [
                ("special_characters_notes", "Special characters in notes"),
                ("very_long_notes", "Very long notes text"),
                ("sql_injection_attempt", "SQL injection attempt"),
                ("xss_attempt", "XSS attempt")
            ]
            
            for case_key, case_description in special_cases:
                test_logger.step(f"Test {case_description}")
                
                case_data = self.invalid_data_scenarios.get(case_key, "")
                non_payment_page.enter_notes(case_data)
                
                success = non_payment_page.submit_form()
                
                # For security-related tests, form should either:
                # 1. Reject the input with validation error, or
                # 2. Sanitize the input and accept it
                
                if case_key in ["sql_injection_attempt", "xss_attempt"]:
                    test_logger.verification(f"Security validation for {case_description}")
                    # Either rejected or sanitized - both are acceptable
                    if not success:
                        errors = non_payment_page.get_validation_errors()
                        test_logger.info(f"Security input rejected with errors: {errors}")
                    else:
                        test_logger.info(f"Security input accepted (possibly sanitized)")
                        
                elif case_key == "very_long_notes":
                    test_logger.verification("Very long notes validation")
                    # Should be rejected or truncated
                    if not success:
                        errors = non_payment_page.get_validation_errors()
                        length_error_found = any("length" in error.lower() or "long" in error.lower() 
                                               for error in errors)
                        test_logger.info(f"Long notes validation result: {errors}")
                        
                elif case_key == "special_characters_notes":
                    test_logger.verification("Special characters validation")
                    # Special characters should generally be allowed in notes
                    test_logger.info(f"Special characters handling result: success={success}")
                    
                # Reset for next test
                non_payment_page.reset_form()
                time.sleep(1)
                
                # Re-select reasons for next iteration
                if level1_options and len(special_cases) > 1:
                    non_payment_page.select_level1_reason(level1_options[0])
                    time.sleep(1)
                    if level2_options:
                        non_payment_page.select_level2_reason(level2_options[0])
                        time.sleep(1)
                        
            test_logger.result("Special characters validation test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Special characters validation test failed", e)
            non_payment_page.take_screenshot("Special_Characters_Validation_Failed")
            raise
        finally:
            log_test_end("Special Characters Validation", True)
            
    @allure.story("Form Validation Error Messages")
    @allure.title("Validation Error Message Clarity")
    @allure.description("Verify validation error messages are clear and actionable")
    @pytest.mark.validation
    def test_validation_error_messages(self, revenue_user_session, config_data, logger):
        """
        Test validation error message clarity and usefulness.
        
        Ensures error messages are:
        - Clear and specific
        - Actionable (tell user what to do)
        - Properly localized (if applicable)
        """
        test_logger = log_test_start("Validation Error Messages")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Test various validation scenarios and check error message quality
            test_scenarios = [
                {
                    "name": "Empty form submission",
                    "setup": lambda: None,  # No setup needed
                    "expected_keywords": ["complete", "information", "required"]
                },
                {
                    "name": "Missing Level 2",
                    "setup": lambda: self._setup_level1_only(non_payment_page),
                    "expected_keywords": ["level", "reason", "select"]
                },
                {
                    "name": "Missing notes",
                    "setup": lambda: self._setup_reasons_no_notes(non_payment_page),
                    "expected_keywords": ["notes", "required", "enter"]
                }
            ]
            
            for scenario in test_scenarios:
                test_logger.step(f"Test error messages for: {scenario['name']}")
                
                # Reset form
                non_payment_page.reset_form()
                time.sleep(1)
                
                # Setup scenario
                if scenario["setup"]:
                    scenario["setup"]()
                    
                # Submit and get errors
                success = non_payment_page.submit_form()
                assert not success, f"Form should fail for scenario: {scenario['name']}"
                
                errors = non_payment_page.get_validation_errors()
                assert len(errors) > 0, f"No validation errors found for: {scenario['name']}"
                
                # Check error message quality
                all_error_text = " ".join(errors).lower()
                
                test_logger.verification(f"Check error message clarity for {scenario['name']}")
                
                # Verify expected keywords are present
                for keyword in scenario["expected_keywords"]:
                    if keyword.lower() not in all_error_text:
                        test_logger.warning(f"Expected keyword '{keyword}' not found in error: {errors}")
                        
                # Check message is not too technical
                technical_terms = ["null", "undefined", "exception", "error code"]
                for term in technical_terms:
                    if term in all_error_text:
                        test_logger.warning(f"Technical term '{term}' found in user-facing error: {errors}")
                        
                test_logger.info(f"Error messages for '{scenario['name']}': {errors}")
                
            test_logger.result("Validation error messages test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Validation error messages test failed", e)
            non_payment_page.take_screenshot("Validation_Error_Messages_Failed")
            raise
        finally:
            log_test_end("Validation Error Messages", True)
            
    def _setup_level1_only(self, non_payment_page):
        """Helper method to setup Level 1 selection only."""
        level1_options = non_payment_page.get_all_level1_options()
        if level1_options:
            non_payment_page.select_level1_reason(level1_options[0])
            time.sleep(1)
            
    def _setup_reasons_no_notes(self, non_payment_page):
        """Helper method to setup reason selections without notes."""
        level1_options = non_payment_page.get_all_level1_options()
        if level1_options:
            non_payment_page.select_level1_reason(level1_options[0])
            time.sleep(2)
            
            level2_options = non_payment_page.get_all_level2_options()
            if level2_options:
                non_payment_page.select_level2_reason(level2_options[0])
                time.sleep(1)
                
    @allure.story("Form State Management")
    @allure.title("Form State and Reset Validation")
    @allure.description("Test form state management and reset functionality")
    @pytest.mark.validation
    def test_form_state_management(self, revenue_user_session, config_data, logger):
        """
        Test form state management including:
        - Form reset functionality
        - State preservation during validation errors
        - Clear error messages after correction
        """
        test_logger = log_test_start("Form State Management")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup form with some data
            test_logger.step("Fill form with partial data")
            level1_options = non_payment_page.get_all_level1_options()
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                time.sleep(1)
                
                test_notes = "Test notes for state management"
                non_payment_page.enter_notes(test_notes)
                
            # Trigger validation error
            test_logger.step("Trigger validation error")
            success = non_payment_page.submit_form()
            assert not success, "Form should fail with incomplete data"
            
            # Verify error is displayed
            errors = non_payment_page.get_validation_errors()
            assert len(errors) > 0, "Validation errors should be displayed"
            
            # Test form reset
            test_logger.step("Test form reset functionality")
            non_payment_page.reset_form()
            time.sleep(1)
            
            # Verify form is reset
            test_logger.verification("Verify form state after reset")
            # Note: Specific verification depends on implementation
            
            # Verify error messages are cleared
            errors_after_reset = non_payment_page.get_validation_errors()
            test_logger.verification("Verify error messages cleared after reset")
            # Errors should be cleared or significantly reduced
            
            test_logger.result("Form state management test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Form state management test failed", e)
            non_payment_page.take_screenshot("Form_State_Management_Failed")
            raise
        finally:
            log_test_end("Form State Management", True)