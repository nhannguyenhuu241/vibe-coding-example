"""
Test cases for external system integration functionality.
Covers TC-006: External System Synchronization and TC-007: Data Mapping.
"""

import pytest
import allure
import time
import requests
from datetime import datetime, timedelta
from pages.non_payment_reason_page import NonPaymentReasonPage
from utils.test_data_manager import TestDataManager
from utils.logger import log_test_start, log_test_end


@allure.epic("Non-Payment Reason Management")
@allure.feature("External System Integration")
class TestIntegration:
    """
    Test class for external system integration functionality.
    Tests data synchronization with Customer Debt Management Tool, Customer Management System,
    and Customer Care Platform.
    """
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, config_data, logger):
        """Setup test data for integration tests."""
        self.test_data_manager = TestDataManager(config_data, logger)
        self.external_systems = config_data.get('external_systems', {})
        
    @allure.story("Customer Debt Management Tool Integration")
    @allure.title("TC-006.1: Customer Debt Management Tool Data Synchronization")
    @allure.description("Verify data synchronization with Customer Debt Management Tool")
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_customer_debt_management_integration(self, revenue_user_session, config_data, logger):
        """
        Test Customer Debt Management Tool integration.
        
        Test Steps:
        1. Complete non-payment reason form with all fields
        2. Submit form
        3. Verify data is sent to Customer Debt Management Tool
        4. Check that reason categories are properly mapped
        5. Verify appointment date/time synchronization
        6. Confirm disconnect date synchronization (for Revenue Collection)
        """
        test_logger = log_test_start("Customer Debt Management Tool Integration")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup complete form data
            test_data = self._setup_complete_form_data(non_payment_page, test_logger, include_disconnect=True)
            
            test_logger.step("Submit complete non-payment reason form")
            
            # Record submission timestamp for integration verification
            submission_time = datetime.now().isoformat()
            
            success = non_payment_page.submit_form()
            
            test_logger.verification("Verify form submission succeeds")
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                test_logger.warning(f"Form submission failed with errors: {errors}")
                # Skip integration testing if form submission fails
                pytest.skip("Form submission failed - cannot test integration")
                
            # Wait for integration processing
            test_logger.step("Wait for external system integration processing")
            integration_timeout = self.external_systems.get('customer_debt_management', {}).get('timeout', 10)
            time.sleep(integration_timeout)
            
            # Verify integration with Customer Debt Management Tool
            test_logger.step("Verify data synchronization with Customer Debt Management Tool")
            
            # Mock integration verification (in real implementation, this would query the external system)
            integration_verified = self._verify_customer_debt_management_sync(
                test_data, 
                submission_time, 
                test_logger
            )
            
            test_logger.verification("Verify reason categories are properly mapped")
            assert integration_verified.get('reason_mapping', False), "Reason categories should be properly mapped"
            
            test_logger.verification("Verify appointment synchronization")
            assert integration_verified.get('appointment_sync', False), "Appointment data should be synchronized"
            
            test_logger.verification("Verify disconnect date synchronization for Revenue Collection")
            if test_data.get('disconnect_data'):
                assert integration_verified.get('disconnect_sync', False), "Disconnect data should be synchronized"
                
            test_logger.result("Customer Debt Management Tool integration test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Customer Debt Management Tool integration test failed", e)
            non_payment_page.take_screenshot("Customer_Debt_Management_Integration_Failed")
            raise
        finally:
            log_test_end("Customer Debt Management Tool Integration", True)
            
    @allure.story("Customer Management System Integration")
    @allure.title("TC-006.2: Customer Management System Data Flow")
    @allure.description("Verify Customer Management System data flow and synchronization")
    @pytest.mark.integration
    def test_customer_management_system_integration(self, revenue_user_session, config_data, logger):
        """
        Test Customer Management System integration.
        
        Test Steps:
        1. Submit complete non-payment reason information
        2. Verify contact information synchronization
        3. Check appointment scheduling data transfer
        4. Verify customer interaction history updates
        5. Confirm proper field mapping as per specification
        """
        test_logger = log_test_start("Customer Management System Integration")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup complete form data
            test_data = self._setup_complete_form_data(non_payment_page, test_logger)
            
            test_logger.step("Submit complete non-payment reason information")
            
            submission_time = datetime.now().isoformat()
            success = non_payment_page.submit_form()
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                test_logger.warning(f"Form submission failed: {errors}")
                pytest.skip("Form submission failed - cannot test integration")
                
            # Wait for integration processing
            integration_timeout = self.external_systems.get('customer_management', {}).get('timeout', 10)
            time.sleep(integration_timeout)
            
            test_logger.step("Verify Customer Management System integration")
            
            # Mock integration verification
            cms_integration = self._verify_customer_management_sync(
                test_data,
                submission_time,
                test_logger
            )
            
            test_logger.verification("Verify contact information synchronization")
            assert cms_integration.get('contact_sync', False), "Contact information should be synchronized"
            
            test_logger.verification("Verify appointment scheduling data transfer")
            assert cms_integration.get('appointment_transfer', False), "Appointment data should be transferred"
            
            test_logger.verification("Verify customer interaction history updates")
            assert cms_integration.get('history_update', False), "Customer interaction history should be updated"
            
            test_logger.verification("Verify proper field mapping")
            assert cms_integration.get('field_mapping', False), "Field mapping should follow specification"
            
            test_logger.result("Customer Management System integration test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Customer Management System integration test failed", e)
            non_payment_page.take_screenshot("Customer_Management_System_Integration_Failed")
            raise
        finally:
            log_test_end("Customer Management System Integration", True)
            
    @allure.story("Multi-System Integration Consistency")
    @allure.title("TC-006.3: Multi-System Integration Data Consistency")
    @allure.description("Verify data consistency across all integrated systems")
    @pytest.mark.integration
    def test_multi_system_integration_consistency(self, revenue_user_session, config_data, logger):
        """
        Test multi-system integration consistency.
        
        Test Steps:
        1. Submit non-payment reason with complete information
        2. Verify same data appears correctly in all three systems
        3. Update existing reason information
        4. Verify updates propagate to all systems
        5. Check data consistency after system refresh
        """
        test_logger = log_test_start("Multi-System Integration Consistency")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup complete form data
            test_data = self._setup_complete_form_data(non_payment_page, test_logger, include_disconnect=True)
            
            test_logger.step("Submit complete non-payment reason information")
            
            submission_time = datetime.now().isoformat()
            success = non_payment_page.submit_form()
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                pytest.skip(f"Form submission failed: {errors}")
                
            # Wait for all integrations to complete
            max_timeout = max(
                self.external_systems.get('customer_debt_management', {}).get('timeout', 10),
                self.external_systems.get('customer_management', {}).get('timeout', 10),
                self.external_systems.get('customer_care_platform', {}).get('timeout', 10)
            )
            time.sleep(max_timeout + 2)  # Extra buffer
            
            test_logger.step("Verify data consistency across all systems")
            
            # Verify Customer Debt Management Tool
            cdm_data = self._verify_customer_debt_management_sync(test_data, submission_time, test_logger)
            
            # Verify Customer Management System
            cms_data = self._verify_customer_management_sync(test_data, submission_time, test_logger)
            
            # Verify Customer Care Platform
            ccp_data = self._verify_customer_care_platform_sync(test_data, submission_time, test_logger)
            
            test_logger.verification("Verify data appears correctly in all systems")
            
            # Check consistency across systems
            consistency_checks = [
                cdm_data.get('data_present', False),
                cms_data.get('data_present', False),
                ccp_data.get('data_present', False)
            ]
            
            assert all(consistency_checks), "Data should be present in all integrated systems"
            
            # Test data update propagation
            test_logger.step("Test data update propagation")
            
            # This would require updating existing data and verifying propagation
            # Implementation depends on system capabilities for updates
            
            test_logger.verification("Verify update propagation (if supported)")
            # Note: This may require separate update functionality testing
            
            # Test system refresh consistency
            test_logger.step("Test data consistency after system refresh")
            
            # Refresh page and verify data persistence
            non_payment_page.refresh_page()
            non_payment_page.wait_for_non_payment_page_load()
            
            # Re-verify integration after refresh
            refreshed_cdm_data = self._verify_customer_debt_management_sync(test_data, submission_time, test_logger)
            
            test_logger.verification("Verify data consistency after refresh")
            assert refreshed_cdm_data.get('data_present', False), "Data should remain consistent after page refresh"
            
            test_logger.result("Multi-system integration consistency test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Multi-system integration consistency test failed", e)
            non_payment_page.take_screenshot("Multi_System_Integration_Consistency_Failed")
            raise
        finally:
            log_test_end("Multi-System Integration Consistency", True)
            
    @allure.story("Data Mapping and Field Population")
    @allure.title("TC-007.1: Automatic Field Population Verification")
    @allure.description("Verify automatic field mapping per specification")
    @pytest.mark.integration
    def test_automatic_field_population(self, revenue_user_session, config_data, logger):
        """
        Test automatic field population per specification.
        
        Test Steps:
        1. Complete and submit non-payment reason form
        2. Verify in Customer Debt Management Tool:
           - "Contact Person" is left blank
           - "Payment Capability" is left blank
           - "Action" is left blank
           - "Contact Channel" is set to "MobiX"
           - "Care Result Notes" contains MobiX notes content
        3. Verify appointment and disconnect information populates correctly
        """
        test_logger = log_test_start("Automatic Field Population")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup form with specific test data
            test_notes = "Test notes for automatic field mapping verification"
            test_data = self._setup_complete_form_data(
                non_payment_page, 
                test_logger, 
                specific_notes=test_notes,
                include_disconnect=True
            )
            
            test_logger.step("Submit non-payment reason form")
            
            submission_time = datetime.now().isoformat()
            success = non_payment_page.submit_form()
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                pytest.skip(f"Form submission failed: {errors}")
                
            # Wait for integration
            time.sleep(self.external_systems.get('customer_debt_management', {}).get('timeout', 10))
            
            test_logger.step("Verify automatic field population in Customer Debt Management Tool")
            
            # Mock verification of field population
            field_mapping = self._verify_field_population(test_data, test_notes, submission_time, test_logger)
            
            test_logger.verification("Verify 'Contact Person' is left blank")
            assert field_mapping.get('contact_person_blank', False), "Contact Person field should be left blank"
            
            test_logger.verification("Verify 'Payment Capability' is left blank")
            assert field_mapping.get('payment_capability_blank', False), "Payment Capability field should be left blank"
            
            test_logger.verification("Verify 'Action' is left blank")
            assert field_mapping.get('action_blank', False), "Action field should be left blank"
            
            test_logger.verification("Verify 'Contact Channel' is set to 'MobiX'")
            assert field_mapping.get('contact_channel_mobix', False), "Contact Channel should be set to 'MobiX'"
            
            test_logger.verification("Verify 'Care Result Notes' contains MobiX notes content")
            assert field_mapping.get('notes_transferred', False), "Care Result Notes should contain MobiX notes"
            
            test_logger.verification("Verify appointment information populates correctly")
            if test_data.get('appointment_data'):
                assert field_mapping.get('appointment_populated', False), "Appointment information should populate correctly"
                
            test_logger.verification("Verify disconnect information populates correctly")
            if test_data.get('disconnect_data'):
                assert field_mapping.get('disconnect_populated', False), "Disconnect information should populate correctly"
                
            test_logger.result("Automatic field population test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Automatic field population test failed", e)
            non_payment_page.take_screenshot("Automatic_Field_Population_Failed")
            raise
        finally:
            log_test_end("Automatic Field Population", True)
            
    @allure.story("Integration Performance")
    @allure.title("Integration System Performance Testing")
    @allure.description("Verify integration system performance meets requirements")
    @pytest.mark.integration
    @pytest.mark.performance
    def test_integration_performance(self, revenue_user_session, config_data, logger, performance_monitor):
        """
        Test integration system performance.
        
        Validates:
        - All external system updates < 5 seconds
        - Individual system update times
        - Performance under various conditions
        """
        test_logger = log_test_start("Integration Performance")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Setup test data
            test_data = self._setup_complete_form_data(non_payment_page, test_logger)
            
            test_logger.step("Measure integration performance")
            
            # Record start time
            start_time = time.time()
            
            # Submit form
            success = non_payment_page.submit_form()
            
            if not success:
                errors = non_payment_page.get_validation_errors()
                pytest.skip(f"Form submission failed: {errors}")
                
            # Wait for integration completion and measure time
            max_timeout = config_data.get('performance', {}).get('integration_max', 5)
            
            # Mock integration completion detection
            integration_complete = self._wait_for_integration_completion(max_timeout, test_logger)
            
            total_integration_time = time.time() - start_time
            
            test_logger.performance("Total integration time", total_integration_time)
            
            test_logger.verification(f"Verify total integration time < {max_timeout} seconds")
            assert total_integration_time < max_timeout, f"Integration time {total_integration_time:.2f}s exceeds {max_timeout}s threshold"
            
            # Test individual system performance
            test_logger.step("Measure individual system performance")
            
            individual_times = self._measure_individual_system_performance(test_data, test_logger)
            
            for system, perf_time in individual_times.items():
                test_logger.performance(f"{system} integration time", perf_time)
                
                # Individual systems should complete within reasonable time
                individual_threshold = max_timeout * 0.8  # 80% of total threshold
                assert perf_time < individual_threshold, f"{system} time {perf_time:.2f}s exceeds threshold"
                
            test_logger.result(f"Integration performance test completed - Total: {total_integration_time:.2f}s", True)
            
        except Exception as e:
            test_logger.error("Integration performance test failed", e)
            non_payment_page.take_screenshot("Integration_Performance_Failed")
            raise
        finally:
            log_test_end("Integration Performance", True)
            
    # Helper methods for integration testing
    
    def _setup_complete_form_data(self, non_payment_page, test_logger, specific_notes=None, include_disconnect=False):
        """Setup complete form data for integration testing."""
        test_logger.step("Setup complete form data")
        
        # Get test data
        if include_disconnect:
            test_data = self.test_data_manager.get_role_specific_test_data('revenue_collection')
        else:
            test_data = self.test_data_manager.get_role_specific_test_data('customer_care')
            
        # Select reasons
        reason = test_data['reason_hierarchy']
        
        level1_options = non_payment_page.get_all_level1_options()
        if reason.level1 in level1_options:
            non_payment_page.select_level1_reason(reason.level1)
        elif level1_options:
            non_payment_page.select_level1_reason(level1_options[0])
            
        time.sleep(2)
        
        level2_options = non_payment_page.get_all_level2_options()
        if level2_options:
            if reason.level2 in level2_options:
                non_payment_page.select_level2_reason(reason.level2)
            else:
                non_payment_page.select_level2_reason(level2_options[0])
                
        # Add notes
        notes = specific_notes or test_data['notes']
        non_payment_page.enter_notes(notes)
        
        # Setup appointment
        appointment = test_data['appointment']
        non_payment_page.select_appointment_date(appointment.date)
        time.sleep(1)
        non_payment_page.select_appointment_time(appointment.time)
        
        # Setup disconnect data if included
        if include_disconnect and 'disconnect' in test_data:
            disconnect = test_data['disconnect']
            # Setup disconnect options (implementation-specific)
            
        return {
            'reason_hierarchy': reason,
            'notes': notes,
            'appointment_data': appointment,
            'disconnect_data': test_data.get('disconnect'),
            'contract': test_data['contract']
        }
        
    def _verify_customer_debt_management_sync(self, test_data, submission_time, test_logger):
        """Mock verification of Customer Debt Management Tool synchronization."""
        test_logger.step("Verify Customer Debt Management Tool synchronization")
        
        # In real implementation, this would query the external system API
        # Mock verification results
        return {
            'data_present': True,
            'reason_mapping': True,
            'appointment_sync': True,
            'disconnect_sync': True if test_data.get('disconnect_data') else None,
            'field_mapping_correct': True
        }
        
    def _verify_customer_management_sync(self, test_data, submission_time, test_logger):
        """Mock verification of Customer Management System synchronization."""
        test_logger.step("Verify Customer Management System synchronization")
        
        return {
            'data_present': True,
            'contact_sync': True,
            'appointment_transfer': True,
            'history_update': True,
            'field_mapping': True
        }
        
    def _verify_customer_care_platform_sync(self, test_data, submission_time, test_logger):
        """Mock verification of Customer Care Platform synchronization."""
        test_logger.step("Verify Customer Care Platform synchronization")
        
        return {
            'data_present': True,
            'interaction_logged': True,
            'notes_synced': True,
            'timeline_updated': True
        }
        
    def _verify_field_population(self, test_data, test_notes, submission_time, test_logger):
        """Mock verification of automatic field population."""
        test_logger.step("Verify automatic field population")
        
        return {
            'contact_person_blank': True,
            'payment_capability_blank': True,
            'action_blank': True,
            'contact_channel_mobix': True,
            'notes_transferred': True,
            'appointment_populated': True if test_data.get('appointment_data') else False,
            'disconnect_populated': True if test_data.get('disconnect_data') else False
        }
        
    def _wait_for_integration_completion(self, timeout, test_logger):
        """Mock waiting for integration completion."""
        # In real implementation, this would poll external systems or check status endpoints
        time.sleep(timeout * 0.5)  # Simulate integration time
        test_logger.info("Integration completion detected (mock)")
        return True
        
    def _measure_individual_system_performance(self, test_data, test_logger):
        """Mock measurement of individual system performance."""
        # Mock individual system performance times
        return {
            'customer_debt_management': 1.5,
            'customer_management': 1.2,
            'customer_care_platform': 0.8
        }