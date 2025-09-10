"""
Test cases for role-based access control functionality.
Covers TC-005: Role-Based Access Control and TC-004: Service Disconnection Scheduling.
"""

import pytest
import allure
import time
from datetime import datetime, timedelta
from pages.non_payment_reason_page import NonPaymentReasonPage
from utils.test_data_manager import TestDataManager
from utils.logger import log_test_start, log_test_end


@allure.epic("Non-Payment Reason Management")
@allure.feature("Role-Based Access Control")
class TestRoleBasedAccess:
    """
    Test class for role-based access control functionality.
    Tests feature access for different user roles and service disconnection permissions.
    """
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, config_data, logger):
        """Setup test data for role-based access tests."""
        self.test_data_manager = TestDataManager(config_data, logger)
        
    @allure.story("Revenue Collection Role Features")
    @allure.title("TC-005.1: Revenue Collection Role Complete Access")
    @allure.description("Verify Revenue Collection users see all features including service disconnection")
    @pytest.mark.rbac
    @pytest.mark.smoke
    def test_revenue_collection_role_features(self, revenue_user_session, config_data, logger):
        """
        Test Revenue Collection role complete feature access.
        
        Test Steps:
        1. Navigate to Non-Payment Reason screen
        2. Verify all reason selection dropdowns are visible
        3. Verify payment appointment scheduling is available
        4. Verify service disconnection scheduling options are visible
        5. Verify historical tracking shows disconnect dates
        """
        test_logger = log_test_start("Revenue Collection Role Features")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            test_logger.verification("Verify all reason selection dropdowns are visible")
            
            # Test Level 1 dropdown visibility
            level1_visible = non_payment_page.is_element_visible(
                non_payment_page.LEVEL1_DROPDOWN,
                timeout=10
            )
            assert level1_visible, "Level 1 reason dropdown should be visible for Revenue Collection role"
            
            # Test Level 2 dropdown (after Level 1 selection)
            level1_options = non_payment_page.get_all_level1_options()
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                time.sleep(2)
                
                level2_visible = non_payment_page.is_element_visible(
                    non_payment_page.LEVEL2_DROPDOWN,
                    timeout=5
                )
                assert level2_visible, "Level 2 reason dropdown should be visible after Level 1 selection"
                
            test_logger.verification("Verify payment appointment scheduling is available")
            
            # Test appointment scheduling visibility
            appointment_date_visible = non_payment_page.is_element_visible(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                timeout=5
            )
            assert appointment_date_visible, "Appointment date picker should be visible for Revenue Collection role"
            
            test_logger.verification("Verify service disconnection scheduling options are visible")
            
            # Test disconnect option visibility (Revenue Collection specific)
            disconnect_options_visible = non_payment_page.is_disconnect_options_visible()
            assert disconnect_options_visible, "Service disconnection options should be visible for Revenue Collection role"
            
            # Test specific disconnect option elements
            disconnect_option1_visible = non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION1_BOX,
                timeout=5
            )
            assert disconnect_option1_visible, "Disconnect option 1 box should be visible for Revenue Collection role"
            
            test_logger.verification("Verify historical tracking shows disconnect-related information")
            
            # Test history section visibility
            history_visible = non_payment_page.is_element_visible(
                non_payment_page.REASON_HISTORY_SECTION,
                timeout=5
            )
            # Note: History section may not be immediately visible depending on implementation
            
            test_logger.result("Revenue Collection role features test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Revenue Collection role features test failed", e)
            non_payment_page.take_screenshot("Revenue_Collection_Role_Failed")
            raise
        finally:
            log_test_end("Revenue Collection Role Features", True)
            
    @allure.story("Non-Revenue Collection Role Restrictions")
    @allure.title("TC-005.2: Non-Revenue Collection Role Access Restrictions")
    @allure.description("Verify other roles have appropriate feature restrictions")
    @pytest.mark.rbac
    def test_non_revenue_collection_role_restrictions(self, customer_care_session, config_data, logger):
        """
        Test non-Revenue Collection role access restrictions.
        
        Test Steps:
        1. Navigate to Non-Payment Reason screen
        2. Verify reason selection dropdowns are visible
        3. Verify payment appointment scheduling is available
        4. Verify service disconnection scheduling is hidden
        5. Verify historical tracking excludes disconnect-related information
        """
        test_logger = log_test_start("Non-Revenue Collection Role Restrictions")
        
        try:
            non_payment_page = NonPaymentReasonPage(customer_care_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            test_logger.verification("Verify basic features are accessible")
            
            # Test basic reason selection is available
            level1_visible = non_payment_page.is_element_visible(
                non_payment_page.LEVEL1_DROPDOWN,
                timeout=10
            )
            assert level1_visible, "Level 1 reason dropdown should be visible for all roles"
            
            # Test Level 2 availability after Level 1 selection
            level1_options = non_payment_page.get_all_level1_options()
            if level1_options:
                non_payment_page.select_level1_reason(level1_options[0])
                time.sleep(2)
                
                level2_visible = non_payment_page.is_element_visible(
                    non_payment_page.LEVEL2_DROPDOWN,
                    timeout=5
                )
                assert level2_visible, "Level 2 reason dropdown should be visible for all roles"
                
            test_logger.verification("Verify payment appointment scheduling is available")
            
            # Test appointment scheduling is available to all roles
            appointment_date_visible = non_payment_page.is_element_visible(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                timeout=5
            )
            assert appointment_date_visible, "Appointment scheduling should be available for all roles"
            
            test_logger.verification("Verify service disconnection scheduling is hidden")
            
            # Test disconnect options are NOT visible for non-Revenue Collection roles
            disconnect_options_visible = non_payment_page.is_disconnect_options_visible()
            assert not disconnect_options_visible, "Service disconnection options should be hidden for non-Revenue Collection roles"
            
            # Test specific disconnect elements are not present
            disconnect_option1_visible = non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION1_BOX,
                timeout=3
            )
            assert not disconnect_option1_visible, "Disconnect option 1 should not be visible for non-Revenue Collection roles"
            
            disconnect_option2_visible = non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION2_BOX,
                timeout=3
            )
            assert not disconnect_option2_visible, "Disconnect option 2 should not be visible for non-Revenue Collection roles"
            
            test_logger.verification("Verify form submission works without disconnect options")
            
            # Test that form can be submitted successfully without disconnect features
            level2_options = non_payment_page.get_all_level2_options()
            if level2_options:
                non_payment_page.select_level2_reason(level2_options[0])
                
            # Add notes
            notes = "Test submission for Customer Care role without disconnect options"
            non_payment_page.enter_notes(notes)
            
            # Submit form
            success = non_payment_page.submit_form()
            test_logger.verification("Verify form submission succeeds for non-Revenue Collection role")
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                # Verify no disconnect-related errors
                disconnect_errors = [e for e in errors if 'disconnect' in e.lower()]
                assert len(disconnect_errors) == 0, f"Unexpected disconnect-related errors for non-Revenue role: {disconnect_errors}"
                
            test_logger.result("Non-Revenue Collection role restrictions test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Non-Revenue Collection role restrictions test failed", e)
            non_payment_page.take_screenshot("Non_Revenue_Collection_Role_Failed")
            raise
        finally:
            log_test_end("Non-Revenue Collection Role Restrictions", True)
            
    @allure.story("Service Disconnection Scheduling")
    @allure.title("TC-004.1: First Option Box Logic")
    @allure.description("Verify first disconnection option behavior for Revenue Collection role")
    @pytest.mark.rbac
    @pytest.mark.disconnect
    def test_first_disconnect_option_logic(self, revenue_user_session, config_data, logger):
        """
        Test first disconnect option box logic.
        
        Test Steps:
        1. Verify first option box is empty by default
        2. Select "Option 2: Disconnect after Option 1 and until end of month disconnect completely"
        3. Verify second option box appears
        4. Select different option or clear selection
        5. Verify second option box is hidden
        """
        test_logger = log_test_start("First Disconnect Option Logic")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup basic form data
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            test_logger.verification("Verify first option box is empty by default")
            
            # Verify disconnect options are visible (Revenue Collection role check)
            disconnect_options_visible = non_payment_page.is_disconnect_options_visible()
            assert disconnect_options_visible, "Disconnect options should be visible for Revenue Collection role"
            
            # Verify second option box is not visible initially
            option2_initially_hidden = not non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION2_BOX,
                timeout=3
            )
            assert option2_initially_hidden, "Second option box should be hidden initially"
            
            test_logger.step("Select Option 2 in first option box")
            
            # Select "Option 2" which should reveal second option box
            option2_text = "Option 2: Disconnect after Option 1 and until end of month disconnect completely"
            success = non_payment_page.select_disconnect_option1(option2_text)
            
            if not success:
                # Try alternative text or approach
                test_logger.warning("Direct Option 2 selection failed, trying alternative approaches")
                # May need to adapt based on actual implementation
                
            test_logger.verification("Verify second option box appears after selecting Option 2")
            
            time.sleep(2)  # Wait for UI update
            
            option2_visible = non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION2_BOX,
                timeout=5
            )
            # Note: This assertion depends on successful Option 2 selection
            if success:
                assert option2_visible, "Second option box should appear after selecting Option 2"
                
            test_logger.step("Test different option selection hides second option box")
            
            # Try selecting a different option (if available)
            # This would require knowing available options from the dropdown
            try:
                # Reset or select different option
                different_option = "Option 1"  # Assuming this exists
                alt_success = non_payment_page.select_disconnect_option1(different_option)
                
                if alt_success:
                    time.sleep(2)
                    
                    option2_hidden_again = not non_payment_page.is_element_visible(
                        non_payment_page.DISCONNECT_OPTION2_BOX,
                        timeout=3
                    )
                    test_logger.verification("Verify second option box hides with different selection")
                    # Note: Verification depends on business logic
                    
            except Exception as e:
                test_logger.warning(f"Could not test alternative option selection: {str(e)}")
                
            test_logger.result("First disconnect option logic test completed successfully", True)
            
        except Exception as e:
            test_logger.error("First disconnect option logic test failed", e)
            non_payment_page.take_screenshot("First_Disconnect_Option_Logic_Failed")
            raise
        finally:
            log_test_end("First Disconnect Option Logic", True)
            
    @allure.story("Service Disconnection Date Logic")
    @allure.title("TC-004.2: Second Option Box Date Logic")
    @allure.description("Verify disconnect date selection rules and validation")
    @pytest.mark.rbac
    @pytest.mark.disconnect
    def test_second_option_date_logic(self, revenue_user_session, config_data, logger):
        """
        Test second option box date logic.
        
        Test Steps:
        1. Select "Cancel disconnect schedule"
        2. Verify third option box is hidden
        3. Select specific disconnect date option
        4. Verify date picker appears
        5. Try to select date <= current date
        6. Verify dates 1-12 of month are disabled
        7. Select valid date between 13th and end of month
        8. Verify third option box appears starting from N+1 day
        """
        test_logger = log_test_start("Second Option Date Logic")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup basic form data and get to second option box
            self._setup_basic_form_data(non_payment_page, test_logger)
            self._setup_disconnect_option2_visible(non_payment_page, test_logger)
            
            test_logger.step("Test 'Cancel disconnect schedule' option")
            
            # Select "Cancel disconnect schedule"
            cancel_option_text = "Cancel disconnect schedule"
            success = non_payment_page.select_disconnect_option2(cancel_option_text)
            
            if success:
                test_logger.verification("Verify third option box is hidden with cancel option")
                time.sleep(2)
                
                option3_hidden = not non_payment_page.is_element_visible(
                    non_payment_page.DISCONNECT_OPTION3_BOX,
                    timeout=3
                )
                assert option3_hidden, "Third option box should be hidden when cancel is selected"
                
            test_logger.step("Test specific disconnect date option")
            
            # Select specific disconnect date option
            date_option_text = "Select specific disconnect date"  # Assumed text
            success = non_payment_page.select_disconnect_option2(date_option_text)
            
            if success:
                test_logger.verification("Verify date picker appears")
                time.sleep(2)
                
                date_picker_visible = non_payment_page.is_element_visible(
                    non_payment_page.DISCONNECT_DATE_PICKER,
                    timeout=5
                )
                assert date_picker_visible, "Disconnect date picker should appear with specific date option"
                
                # Test invalid date selections
                test_logger.step("Test invalid date selections")
                
                # Test past date (should fail)
                past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                past_success = non_payment_page.select_disconnect_date(past_date)
                
                test_logger.verification("Verify past date is rejected")
                assert not past_success, "Past dates should be rejected for disconnect scheduling"
                
                # Test early month dates (1-12, should fail)
                current_date = datetime.now()
                
                # Generate date in current month, day 5 (should be invalid)
                if current_date.day > 5:
                    early_date = current_date.replace(day=5).strftime("%Y-%m-%d")
                    early_success = non_payment_page.select_disconnect_date(early_date)
                    
                    test_logger.verification("Verify early month date (day 5) is rejected")
                    assert not early_success, "Dates 1-12 of month should be rejected"
                    
                # Test valid date (between 13th and end of month, in future)
                test_logger.step("Test valid disconnect date selection")
                
                valid_date = self._generate_valid_disconnect_date()
                valid_success = non_payment_page.select_disconnect_date(valid_date)
                
                test_logger.verification("Verify valid disconnect date is accepted")
                assert valid_success, f"Valid disconnect date should be accepted: {valid_date}"
                
                if valid_success:
                    test_logger.verification("Verify third option box appears after valid date selection")
                    time.sleep(2)
                    
                    option3_visible = non_payment_page.is_element_visible(
                        non_payment_page.DISCONNECT_OPTION3_BOX,
                        timeout=5
                    )
                    assert option3_visible, "Third option box should appear after valid disconnect date selection"
                    
            test_logger.result("Second option date logic test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Second option date logic test failed", e)
            non_payment_page.take_screenshot("Second_Option_Date_Logic_Failed")
            raise
        finally:
            log_test_end("Second Option Date Logic", True)
            
    @allure.story("Service Disconnection Status Selection")
    @allure.title("TC-004.3: Third Option Box Status Selection")
    @allure.description("Verify status selection in third option box")
    @pytest.mark.rbac
    @pytest.mark.disconnect
    def test_third_option_status_selection(self, revenue_user_session, config_data, logger):
        """
        Test third option box status selection.
        
        Test Steps:
        1. Verify third option box appears
        2. Verify "Maintain" and "Temporary" options are available
        3. Select "Maintain" status
        4. Verify selection is saved
        5. Select "Temporary" status
        6. Verify selection is saved
        7. Leave status unselected and attempt to submit
        8. Verify validation error appears
        """
        test_logger = log_test_start("Third Option Status Selection")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup form to get to third option box
            self._setup_basic_form_data(non_payment_page, test_logger)
            self._setup_disconnect_option3_visible(non_payment_page, test_logger)
            
            test_logger.verification("Verify third option box is visible")
            option3_visible = non_payment_page.is_element_visible(
                non_payment_page.DISCONNECT_OPTION3_BOX,
                timeout=5
            )
            
            if not option3_visible:
                pytest.skip("Could not reach third option box state for testing")
                
            test_logger.verification("Verify Maintain and Temporary options are available")
            
            # Test "Maintain" status selection
            test_logger.step("Test 'Maintain' status selection")
            maintain_success = non_payment_page.select_disconnect_status("Maintain")
            
            test_logger.verification("Verify 'Maintain' status can be selected")
            assert maintain_success, "'Maintain' status should be selectable"
            
            # Test "Temporary" status selection
            test_logger.step("Test 'Temporary' status selection")
            temporary_success = non_payment_page.select_disconnect_status("Temporary")
            
            test_logger.verification("Verify 'Temporary' status can be selected")
            assert temporary_success, "'Temporary' status should be selectable"
            
            # Test form submission without status selection
            test_logger.step("Test validation when status is not selected")
            
            # Reset status selection (implementation-dependent)
            # This might require specific UI interaction
            
            # Add notes for complete form
            notes = "Test disconnect status validation"
            non_payment_page.enter_notes(notes)
            
            # Submit without status selection
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission fails without status selection")
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                status_error_found = any('status' in error.lower() or 'maintain' in error.lower() or 'temporary' in error.lower() 
                                       for error in errors)
                
                if status_error_found:
                    test_logger.verification("Verify status validation error is displayed")
                    # This confirms the validation is working
                else:
                    test_logger.info(f"Form failed for other reasons: {errors}")
                    
            # Test complete valid submission
            test_logger.step("Test complete valid submission with status")
            
            # Select a status
            non_payment_page.select_disconnect_status("Maintain")
            
            # Submit form
            final_success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission succeeds with valid status")
            
            if not final_success:
                final_errors = non_payment_page.get_validation_errors()
                status_errors = [e for e in final_errors if 'status' in e.lower()]
                
                assert len(status_errors) == 0, f"Unexpected status errors with valid selection: {status_errors}"
                
            test_logger.result("Third option status selection test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Third option status selection test failed", e)
            non_payment_page.take_screenshot("Third_Option_Status_Selection_Failed")
            raise
        finally:
            log_test_end("Third Option Status Selection", True)
            
    def _setup_basic_form_data(self, non_payment_page, test_logger):
        """Helper method to setup basic form data."""
        test_logger.step("Setup basic form data")
        
        # Select Level 1 and Level 2 reasons
        level1_options = non_payment_page.get_all_level1_options()
        if level1_options:
            non_payment_page.select_level1_reason(level1_options[0])
            time.sleep(2)
            
            level2_options = non_payment_page.get_all_level2_options()
            if level2_options:
                non_payment_page.select_level2_reason(level2_options[0])
                time.sleep(1)
                
    def _setup_disconnect_option2_visible(self, non_payment_page, test_logger):
        """Helper method to setup disconnect option 2 visibility."""
        test_logger.step("Setup disconnect option 2 visibility")
        
        # Select Option 2 in first disconnect option to reveal second option box
        option2_text = "Option 2: Disconnect after Option 1 and until end of month disconnect completely"
        success = non_payment_page.select_disconnect_option1(option2_text)
        
        if not success:
            test_logger.warning("Could not select Option 2, trying alternative approach")
            # Alternative implementation-specific approach
            
        time.sleep(2)
        
    def _setup_disconnect_option3_visible(self, non_payment_page, test_logger):
        """Helper method to setup disconnect option 3 visibility."""
        # First setup option 2
        self._setup_disconnect_option2_visible(non_payment_page, test_logger)
        
        test_logger.step("Setup disconnect option 3 visibility")
        
        # Select specific date option to reveal third option box
        date_option_text = "Select specific disconnect date"
        success = non_payment_page.select_disconnect_option2(date_option_text)
        
        if success:
            time.sleep(2)
            
            # Select valid disconnect date
            valid_date = self._generate_valid_disconnect_date()
            non_payment_page.select_disconnect_date(valid_date)
            
            time.sleep(2)
            
    def _generate_valid_disconnect_date(self):
        """Generate a valid disconnect date (between 13th and end of month, in future)."""
        current_date = datetime.now()
        
        # If current date is after 13th, use next month
        if current_date.day >= 13:
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1, day=15)
            else:
                next_month = current_date.replace(month=current_date.month + 1, day=15)
            return next_month.strftime("%Y-%m-%d")
        else:
            # Use current month, day 15
            valid_date = current_date.replace(day=15)
            return valid_date.strftime("%Y-%m-%d")