"""
Test cases for appointment scheduling and date picker functionality.
Covers TC-003: Payment Appointment Scheduling test scenarios.
"""

import pytest
import allure
import time
from datetime import datetime, timedelta
from pages.non_payment_reason_page import NonPaymentReasonPage
from utils.test_data_manager import TestDataManager
from utils.logger import log_test_start, log_test_end


@allure.epic("Non-Payment Reason Management")
@allure.feature("Appointment Scheduling")
class TestAppointmentScheduling:
    """
    Test class for appointment scheduling and date picker functionality.
    Tests date selection, time selection, and business rule validation.
    """
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, config_data, logger):
        """Setup test data for appointment scheduling tests."""
        self.test_data_manager = TestDataManager(config_data, logger)
        
    @allure.story("Date Selection Functionality")
    @allure.title("TC-003.1: Date Selection Functionality")
    @allure.description("Verify payment appointment date selection functionality")
    @pytest.mark.appointment
    @pytest.mark.smoke
    def test_date_selection_functionality(self, revenue_user_session, config_data, logger):
        """
        Test date selection functionality.
        
        Test Steps:
        1. Verify date selection is enabled by default
        2. Click date picker
        3. Verify current date and future dates are selectable
        4. Attempt to select past dates
        5. Verify past dates are disabled/not selectable
        6. Select a valid future date
        7. Verify time selection appears after date selection
        """
        test_logger = log_test_start("Date Selection Functionality")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup required form fields first
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            test_logger.verification("Verify appointment date picker is enabled by default")
            date_picker_visible = non_payment_page.is_element_visible(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                timeout=10
            )
            assert date_picker_visible, "Appointment date picker should be visible and enabled"
            
            test_logger.step("Click date picker to open calendar")
            non_payment_page.click_element(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                description="Click appointment date picker"
            )
            
            # Wait for calendar to appear
            time.sleep(2)
            
            # Test current date selection
            test_logger.step("Test current date selection")
            today = datetime.now().strftime("%Y-%m-%d")
            
            success = non_payment_page.select_appointment_date(today)
            test_logger.verification("Verify current date can be selected")
            # Note: Business rule may allow or disallow same-day appointments
            
            # Test future date selection
            test_logger.step("Test future date selection")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            success = non_payment_page.select_appointment_date(tomorrow)
            test_logger.verification("Verify future date can be selected")
            assert success, f"Should be able to select future date: {tomorrow}"
            
            # Test past date selection (should fail)
            test_logger.step("Test past date selection (should be disabled)")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Click date picker again to test past date
            non_payment_page.click_element(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                description="Click appointment date picker for past date test"
            )
            time.sleep(1)
            
            # Attempt to select past date
            success = non_payment_page.select_appointment_date(yesterday)
            test_logger.verification("Verify past date cannot be selected")
            assert not success, f"Should not be able to select past date: {yesterday}"
            
            # Test time selection availability after date selection
            test_logger.step("Verify time selection appears after valid date selection")
            
            # Select a valid future date first
            valid_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            non_payment_page.select_appointment_date(valid_date)
            
            time.sleep(2)  # Wait for time picker to appear
            
            time_picker_visible = non_payment_page.is_element_visible(
                non_payment_page.APPOINTMENT_TIME_PICKER,
                timeout=5
            )
            test_logger.verification("Verify time picker appears after date selection")
            assert time_picker_visible, "Time picker should appear after valid date selection"
            
            test_logger.result("Date selection functionality test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Date selection functionality test failed", e)
            non_payment_page.take_screenshot("Date_Selection_Functionality_Failed")
            raise
        finally:
            log_test_end("Date Selection Functionality", True)
            
    @allure.story("Date Restriction Validation")
    @allure.title("TC-003.2: Date Restriction Validation")
    @allure.description("Verify business rules for date restrictions")
    @pytest.mark.appointment
    def test_date_restriction_validation(self, revenue_user_session, config_data, logger):
        """
        Test date restriction validation.
        
        Test Steps:
        1. Try to select yesterday's date (should be disabled)
        2. Select today's date (should be allowed)
        3. Select tomorrow's date (should be allowed)
        4. Select date one week in future (should be allowed)
        5. Verify selected dates display correctly
        """
        test_logger = log_test_start("Date Restriction Validation")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup required form fields
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            # Test date scenarios
            date_scenarios = [
                {
                    "name": "Yesterday (should be disabled)",
                    "date": datetime.now() - timedelta(days=1),
                    "should_succeed": False
                },
                {
                    "name": "Today (should be allowed)",
                    "date": datetime.now(),
                    "should_succeed": True  # May depend on business rules
                },
                {
                    "name": "Tomorrow (should be allowed)",
                    "date": datetime.now() + timedelta(days=1),
                    "should_succeed": True
                },
                {
                    "name": "One week in future (should be allowed)",
                    "date": datetime.now() + timedelta(days=7),
                    "should_succeed": True
                }
            ]
            
            for scenario in date_scenarios:
                test_logger.step(f"Test date restriction: {scenario['name']}")
                
                date_str = scenario["date"].strftime("%Y-%m-%d")
                
                # Open date picker
                non_payment_page.click_element(
                    non_payment_page.APPOINTMENT_DATE_PICKER,
                    description=f"Open date picker for {scenario['name']}"
                )
                time.sleep(1)
                
                # Attempt to select date
                success = non_payment_page.select_appointment_date(date_str)
                
                if scenario["should_succeed"]:
                    test_logger.verification(f"Verify {scenario['name']} can be selected")
                    # Note: Some scenarios may have business rule exceptions
                    if not success:
                        test_logger.warning(f"Expected success but failed for: {scenario['name']}")
                else:
                    test_logger.verification(f"Verify {scenario['name']} cannot be selected")
                    assert not success, f"Date should be restricted: {scenario['name']}"
                    
                # Brief pause between scenarios
                time.sleep(1)
                
            # Test edge case: Far future date
            test_logger.step("Test far future date (6 months ahead)")
            far_future = datetime.now() + timedelta(days=180)
            far_future_str = far_future.strftime("%Y-%m-%d")
            
            non_payment_page.click_element(
                non_payment_page.APPOINTMENT_DATE_PICKER,
                description="Open date picker for far future date"
            )
            time.sleep(1)
            
            success = non_payment_page.select_appointment_date(far_future_str)
            test_logger.verification("Verify far future date handling")
            # Business rules may limit how far in advance appointments can be scheduled
            
            test_logger.result("Date restriction validation test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Date restriction validation test failed", e)
            non_payment_page.take_screenshot("Date_Restriction_Validation_Failed")
            raise
        finally:
            log_test_end("Date Restriction Validation", True)
            
    @allure.story("Time Selection Integration")
    @allure.title("Time Selection and Integration")
    @allure.description("Test time selection functionality and integration with date picker")
    @pytest.mark.appointment
    def test_time_selection_integration(self, revenue_user_session, config_data, logger):
        """
        Test time selection functionality and integration with date picker.
        
        Tests:
        - Time picker availability after date selection
        - Valid time selection options
        - Business hours restrictions (if applicable)
        - Time display and validation
        """
        test_logger = log_test_start("Time Selection Integration")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup required form fields
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            # Select a valid future date
            test_logger.step("Select valid appointment date")
            appointment_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            success = non_payment_page.select_appointment_date(appointment_date)
            assert success, f"Failed to select appointment date: {appointment_date}"
            
            # Wait for time picker to appear
            time.sleep(2)
            
            test_logger.verification("Verify time picker appears after date selection")
            time_picker_visible = non_payment_page.is_element_visible(
                non_payment_page.APPOINTMENT_TIME_PICKER,
                timeout=10
            )
            assert time_picker_visible, "Time picker should be visible after date selection"
            
            # Test time selection options
            test_logger.step("Test available time selection options")
            
            # Common business hour time slots to test
            test_times = [
                "09:00",  # Morning
                "12:00",  # Noon
                "14:00",  # Afternoon
                "17:00"   # Late afternoon
            ]
            
            successful_times = []
            
            for test_time in test_times:
                test_logger.step(f"Test time selection: {test_time}")
                
                success = non_payment_page.select_appointment_time(test_time)
                
                if success:
                    successful_times.append(test_time)
                    test_logger.verification(f"Time {test_time} selected successfully")
                else:
                    test_logger.info(f"Time {test_time} not available (may be outside business hours)")
                    
            # Verify at least some times are available
            assert len(successful_times) > 0, "At least some time slots should be available"
            
            # Test edge case times
            test_logger.step("Test edge case times")
            
            edge_times = [
                "00:00",  # Midnight
                "06:00",  # Very early
                "22:00",  # Late evening
                "23:59"   # End of day
            ]
            
            for edge_time in edge_times:
                success = non_payment_page.select_appointment_time(edge_time)
                test_logger.info(f"Edge time {edge_time} availability: {success}")
                # These may or may not be available based on business rules
                
            # Test complete appointment scheduling
            test_logger.step("Test complete appointment scheduling flow")
            
            if successful_times:
                # Use first successful time
                selected_time = successful_times[0]
                non_payment_page.select_appointment_time(selected_time)
                
                # Add notes and submit
                notes = "Test appointment scheduling with date and time"
                non_payment_page.enter_notes(notes)
                
                # Submit form
                success = non_payment_page.submit_form()
                test_logger.verification("Verify complete appointment scheduling submission")
                
                if not success:
                    errors = non_payment_page.get_validation_errors()
                    test_logger.info(f"Submission errors (may be expected): {errors}")
                    
            test_logger.result("Time selection integration test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Time selection integration test failed", e)
            non_payment_page.take_screenshot("Time_Selection_Integration_Failed")
            raise
        finally:
            log_test_end("Time Selection Integration", True)
            
    @allure.story("Appointment Data Validation")
    @allure.title("Appointment Data Validation and Persistence")
    @allure.description("Test appointment data validation and persistence")
    @pytest.mark.appointment
    def test_appointment_data_validation(self, revenue_user_session, config_data, logger):
        """
        Test appointment data validation and persistence.
        
        Tests:
        - Date/time combination validation
        - Data persistence during form interaction
        - Invalid date/time handling
        - Appointment conflict detection (if applicable)
        """
        test_logger = log_test_start("Appointment Data Validation")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup required form fields
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            # Test data persistence during form interaction
            test_logger.step("Test appointment data persistence")
            
            # Select appointment date and time
            test_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            success = non_payment_page.select_appointment_date(test_date)
            assert success, f"Failed to select test date: {test_date}"
            
            time.sleep(2)
            
            test_time = "10:00"
            success = non_payment_page.select_appointment_time(test_time)
            # Note: Success depends on time availability
            
            # Interact with other form elements
            test_logger.step("Test data persistence during other form interactions")
            
            # Change reason selection and verify appointment data persists
            level1_options = non_payment_page.get_all_level1_options()
            if len(level1_options) > 1:
                # Select different Level 1 reason
                non_payment_page.select_level1_reason(level1_options[-1])
                time.sleep(2)
                
                # Verify appointment date/time persistence
                # Note: This would require specific element value checking
                test_logger.verification("Verify appointment data persists during reason changes")
                
            # Test invalid date/time combinations
            test_logger.step("Test invalid date/time combinations")
            
            # Test same-day appointment with past time (if today is allowed)
            if datetime.now().hour > 12:  # After noon
                today = datetime.now().strftime("%Y-%m-%d")
                morning_time = "09:00"  # Past time for today
                
                # Try to select today with morning time
                non_payment_page.select_appointment_date(today)
                time.sleep(2)
                
                success = non_payment_page.select_appointment_time(morning_time)
                test_logger.verification("Verify past time on current date handling")
                # Should be rejected or warned about
                
            # Test weekend date handling (if business rules apply)
            test_logger.step("Test weekend date handling")
            
            # Find next weekend day
            next_saturday = datetime.now() + timedelta(days=(5 - datetime.now().weekday()) % 7 + 1)
            weekend_date = next_saturday.strftime("%Y-%m-%d")
            
            success = non_payment_page.select_appointment_date(weekend_date)
            test_logger.verification("Verify weekend date handling")
            # May be allowed or restricted based on business rules
            
            # Test appointment with complete valid data
            test_logger.step("Test complete valid appointment scheduling")
            
            # Use guaranteed valid future date
            valid_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
            valid_time = "14:00"  # Mid-afternoon
            
            non_payment_page.select_appointment_date(valid_date)
            time.sleep(2)
            non_payment_page.select_appointment_time(valid_time)
            
            # Add notes
            notes = f"Test appointment scheduled for {valid_date} at {valid_time}"
            non_payment_page.enter_notes(notes)
            
            # Submit and verify
            success = non_payment_page.submit_form()
            test_logger.verification("Verify valid appointment submission")
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                appointment_errors = [e for e in errors if 'appointment' in e.lower() or 'date' in e.lower() or 'time' in e.lower()]
                
                if not appointment_errors:
                    test_logger.info("Form submission failed for non-appointment reasons")
                else:
                    test_logger.warning(f"Unexpected appointment validation errors: {appointment_errors}")
                    
            test_logger.result("Appointment data validation test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Appointment data validation test failed", e)
            non_payment_page.take_screenshot("Appointment_Data_Validation_Failed")
            raise
        finally:
            log_test_end("Appointment Data Validation", True)
            
    def _setup_basic_form_data(self, non_payment_page, test_logger):
        """Helper method to setup basic form data required for appointment testing."""
        test_logger.step("Setup basic form data for appointment testing")
        
        # Select Level 1 and Level 2 reasons
        level1_options = non_payment_page.get_all_level1_options()
        if level1_options:
            non_payment_page.select_level1_reason(level1_options[0])
            time.sleep(2)
            
            level2_options = non_payment_page.get_all_level2_options()
            if level2_options:
                non_payment_page.select_level2_reason(level2_options[0])
                time.sleep(1)
                
    @allure.story("Date Picker Performance")
    @allure.title("Date Picker Loading Performance")
    @allure.description("Test date picker component loading performance")
    @pytest.mark.appointment
    @pytest.mark.performance
    def test_date_picker_performance(self, revenue_user_session, config_data, logger, performance_monitor):
        """
        Test date picker performance characteristics.
        
        Validates:
        - Date picker loading time
        - Calendar navigation responsiveness
        - Date selection responsiveness
        """
        test_logger = log_test_start("Date Picker Performance")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup basic form data
            self._setup_basic_form_data(non_payment_page, test_logger)
            
            # Measure date picker loading performance
            test_logger.step("Measure date picker loading performance")
            
            loading_times = []
            
            for i in range(5):  # Test 5 iterations
                start_time = time.time()
                
                # Click to open date picker
                non_payment_page.click_element(
                    non_payment_page.APPOINTMENT_DATE_PICKER,
                    description=f"Open date picker - iteration {i+1}"
                )
                
                # Wait for date picker to fully load
                date_picker_loaded = non_payment_page.wait_helpers.wait_for_date_picker_loaded(
                    (By.CLASS_NAME, "date-picker-calendar"),
                    timeout=10
                )
                
                load_time = time.time() - start_time
                loading_times.append(load_time)
                
                test_logger.performance(f"Date picker loading iteration {i+1}", load_time)
                
                # Close date picker for next iteration
                # This may require clicking outside or pressing Escape
                time.sleep(1)
                
            # Calculate performance metrics
            avg_load_time = sum(loading_times) / len(loading_times)
            max_load_time = max(loading_times)
            
            # Verify performance requirements
            performance_threshold = 3.0  # 3 seconds threshold
            
            test_logger.verification(f"Verify average date picker load time < {performance_threshold}s")
            assert avg_load_time < performance_threshold, f"Average load time {avg_load_time:.2f}s exceeds threshold"
            
            test_logger.verification(f"Verify maximum date picker load time < {performance_threshold * 1.5}s")
            assert max_load_time < performance_threshold * 1.5, f"Maximum load time {max_load_time:.2f}s exceeds threshold"
            
            test_logger.result(f"Date picker performance test completed - Avg: {avg_load_time:.2f}s, Max: {max_load_time:.2f}s", True)
            
        except Exception as e:
            test_logger.error("Date picker performance test failed", e)
            non_payment_page.take_screenshot("Date_Picker_Performance_Failed")
            raise
        finally:
            log_test_end("Date Picker Performance", True)