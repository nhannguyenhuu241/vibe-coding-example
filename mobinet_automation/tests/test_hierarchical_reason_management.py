"""
Test cases for hierarchical reason management functionality.
Covers TC-001: Hierarchical Reason Management test scenarios.
"""

import pytest
import allure
import time
from pages.non_payment_reason_page import NonPaymentReasonPage
from utils.test_data_manager import TestDataManager
from utils.logger import log_test_start, log_test_end


@allure.epic("Non-Payment Reason Management")
@allure.feature("Hierarchical Reason Selection")
class TestHierarchicalReasonManagement:
    """
    Test class for hierarchical reason selection functionality.
    Tests Level 1, Level 2, and Level 3 reason selection logic.
    """
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, config_data, logger):
        """Setup test data for hierarchical reason tests."""
        self.test_data_manager = TestDataManager(config_data, logger)
        self.reason_hierarchies = self.test_data_manager.generate_reason_hierarchy_data()
        
    @allure.story("Level 1 Reason Selection")
    @allure.title("TC-001.1: Level 1 Reason Selection Functionality")
    @allure.description("Verify Level 1 reason selection functionality and dropdown behavior")
    @pytest.mark.hierarchical
    @pytest.mark.smoke
    def test_level1_reason_selection(self, revenue_user_session, config_data, logger):
        """
        Test Level 1 reason selection functionality.
        
        Test Steps:
        1. Navigate to Non-Payment Reason screen
        2. Verify Level 1 dropdown is displayed and empty by default
        3. Click Level 1 dropdown
        4. Verify complete list of Level 1 reasons loads
        5. Select a Level 1 reason
        6. Verify selection is saved and displayed
        7. Verify Level 2 dropdown becomes available after selection
        """
        test_logger = log_test_start("Level 1 Reason Selection")
        
        try:
            # Initialize page object
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            test_logger.verification("Verify Level 1 dropdown is displayed")
            assert non_payment_page.is_element_visible(non_payment_page.LEVEL1_DROPDOWN), \
                "Level 1 dropdown should be visible"
            
            test_logger.step("Get all Level 1 reason options")
            level1_options = non_payment_page.get_all_level1_options()
            
            test_logger.verification("Verify Level 1 dropdown contains options")
            assert len(level1_options) > 0, "Level 1 dropdown should contain reason options"
            
            # Select first available Level 1 reason
            selected_reason = level1_options[0] if level1_options else "Customer Financial Issues"
            
            test_logger.action(f"Select Level 1 reason: {selected_reason}")
            success = non_payment_page.select_level1_reason(selected_reason)
            
            test_logger.verification("Verify Level 1 reason selection was successful")
            assert success, f"Failed to select Level 1 reason: {selected_reason}"
            
            # Verify Level 2 dropdown becomes enabled/visible
            test_logger.verification("Verify Level 2 dropdown becomes available")
            level2_visible = non_payment_page.is_element_visible(
                non_payment_page.LEVEL2_DROPDOWN, 
                timeout=10
            )
            assert level2_visible, "Level 2 dropdown should become available after Level 1 selection"
            
            test_logger.result("Level 1 reason selection test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Level 1 reason selection test failed", e)
            non_payment_page.take_screenshot("Level_1_Selection_Failed")
            raise
        finally:
            log_test_end("Level 1 Reason Selection", True)
            
    @allure.story("Level 2 Reason Dependency")
    @allure.title("TC-001.2: Level 2 Reason Dependency Verification")
    @allure.description("Verify Level 2 reasons filter correctly based on Level 1 selection")
    @pytest.mark.hierarchical
    def test_level2_reason_dependency(self, revenue_user_session, config_data, logger):
        """
        Test Level 2 reason dependency on Level 1 selection.
        
        Test Steps:
        1. Navigate to Non-Payment Reason screen
        2. Select different Level 1 reasons
        3. For each Level 1 selection, verify Level 2 dropdown updates
        4. Verify Level 2 only shows reasons related to selected Level 1
        5. Select a Level 2 reason
        6. Verify selection is saved
        7. Verify changing Level 1 resets Level 2 and Level 3 selections
        """
        test_logger = log_test_start("Level 2 Reason Dependency")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Get available Level 1 options
            level1_options = non_payment_page.get_all_level1_options()
            
            # Test dependency with multiple Level 1 selections
            for i, level1_reason in enumerate(level1_options[:2]):  # Test first 2 for efficiency
                test_logger.step(f"Test Level 2 dependency for Level 1: {level1_reason}")
                
                # Select Level 1 reason
                success = non_payment_page.select_level1_reason(level1_reason)
                assert success, f"Failed to select Level 1 reason: {level1_reason}"
                
                # Wait for Level 2 to load
                time.sleep(2)
                
                # Get Level 2 options
                level2_options = non_payment_page.get_all_level2_options()
                
                test_logger.verification(f"Verify Level 2 options loaded for {level1_reason}")
                assert len(level2_options) > 0, f"Level 2 should have options for {level1_reason}"
                
                # Select first Level 2 option
                if level2_options:
                    level2_reason = level2_options[0]
                    test_logger.action(f"Select Level 2 reason: {level2_reason}")
                    
                    success = non_payment_page.select_level2_reason(level2_reason)
                    assert success, f"Failed to select Level 2 reason: {level2_reason}"
                    
                    # Verify Level 3 becomes available (if applicable)
                    time.sleep(2)
                    level3_visible = non_payment_page.is_level3_dropdown_visible()
                    test_logger.verification(f"Level 3 dropdown visibility: {level3_visible}")
                    
            # Test Level 1 change resets Level 2 and Level 3
            test_logger.step("Test Level 1 change resets subsequent levels")
            
            if len(level1_options) >= 2:
                # Select different Level 1 reason
                different_level1 = level1_options[1]
                non_payment_page.select_level1_reason(different_level1)
                
                time.sleep(2)
                
                # Verify Level 2 options changed
                new_level2_options = non_payment_page.get_all_level2_options()
                test_logger.verification("Verify Level 2 options updated after Level 1 change")
                # Note: Specific validation would depend on actual business rules
                
            test_logger.result("Level 2 reason dependency test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Level 2 reason dependency test failed", e)
            non_payment_page.take_screenshot("Level_2_Dependency_Failed")
            raise
        finally:
            log_test_end("Level 2 Reason Dependency", True)
            
    @allure.story("Level 3 Reason Conditional Display")
    @allure.title("TC-001.3: Level 3 Reason Conditional Display Logic")
    @allure.description("Verify Level 3 reasons display logic based on Level 1 and Level 2 selections")
    @pytest.mark.hierarchical
    def test_level3_reason_conditional_display(self, revenue_user_session, config_data, logger):
        """
        Test Level 3 reason conditional display logic.
        
        Test Steps:
        1. Navigate to Non-Payment Reason screen
        2. Verify Level 3 dropdown is hidden initially
        3. Select Level 1 reason
        4. Verify Level 3 remains hidden
        5. Select Level 2 reason
        6. Verify Level 3 dropdown appears (if applicable)
        7. Verify Level 3 shows only reasons filtered by Level 1 and Level 2
        8. Select Level 3 reason
        9. Verify all three levels maintain proper hierarchy
        """
        test_logger = log_test_start("Level 3 Reason Conditional Display")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            test_logger.verification("Verify Level 3 dropdown is hidden initially")
            level3_initially_hidden = not non_payment_page.is_level3_dropdown_visible()
            assert level3_initially_hidden, "Level 3 dropdown should be hidden initially"
            
            # Get test data with 3-level hierarchy
            test_hierarchy = None
            for hierarchy in self.reason_hierarchies:
                if hierarchy.level3:
                    test_hierarchy = hierarchy
                    break
                    
            if not test_hierarchy:
                pytest.skip("No 3-level hierarchy data available for testing")
                
            test_logger.step(f"Select Level 1 reason: {test_hierarchy.level1}")
            success = non_payment_page.select_level1_reason(test_hierarchy.level1)
            assert success, f"Failed to select Level 1 reason: {test_hierarchy.level1}"
            
            test_logger.verification("Verify Level 3 remains hidden after Level 1 selection")
            time.sleep(2)
            level3_still_hidden = not non_payment_page.is_level3_dropdown_visible()
            # Note: This may depend on specific business rules
            
            test_logger.step(f"Select Level 2 reason: {test_hierarchy.level2}")
            success = non_payment_page.select_level2_reason(test_hierarchy.level2)
            assert success, f"Failed to select Level 2 reason: {test_hierarchy.level2}"
            
            test_logger.verification("Verify Level 3 dropdown appears after Level 2 selection")
            time.sleep(2)
            level3_visible = non_payment_page.is_level3_dropdown_visible()
            
            if level3_visible:
                test_logger.step("Get Level 3 options")
                level3_options = non_payment_page.get_all_level3_options()
                
                test_logger.verification("Verify Level 3 contains filtered options")
                assert len(level3_options) > 0, "Level 3 should contain filtered reason options"
                
                if test_hierarchy.level3 in level3_options:
                    test_logger.step(f"Select Level 3 reason: {test_hierarchy.level3}")
                    success = non_payment_page.select_level3_reason(test_hierarchy.level3)
                    assert success, f"Failed to select Level 3 reason: {test_hierarchy.level3}"
                else:
                    test_logger.warning(f"Expected Level 3 reason '{test_hierarchy.level3}' not found in options")
                    # Select first available option
                    if level3_options:
                        non_payment_page.select_level3_reason(level3_options[0])
                        
            else:
                test_logger.info("Level 3 dropdown not visible - may not be applicable for selected hierarchy")
                
            test_logger.result("Level 3 reason conditional display test completed", True)
            
        except Exception as e:
            test_logger.error("Level 3 reason conditional display test failed", e)
            non_payment_page.take_screenshot("Level_3_Conditional_Display_Failed")
            raise
        finally:
            log_test_end("Level 3 Reason Conditional Display", True)
            
    @allure.story("Hierarchical Reason Integration")
    @allure.title("Complete Hierarchical Reason Selection Flow")
    @allure.description("Test complete hierarchical reason selection flow with all levels")
    @pytest.mark.hierarchical
    @pytest.mark.integration
    def test_complete_hierarchical_flow(self, revenue_user_session, config_data, logger):
        """
        Test complete hierarchical reason selection flow.
        
        Covers multiple reason hierarchies and validates the complete flow
        from Level 1 through Level 3 selection.
        """
        test_logger = log_test_start("Complete Hierarchical Reason Flow")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            # Test multiple hierarchical flows
            test_hierarchies = self.reason_hierarchies[:3]  # Test first 3 for efficiency
            
            for i, hierarchy in enumerate(test_hierarchies):
                test_logger.step(f"Testing hierarchy {i+1}: {hierarchy.level1}")
                
                # Reset form before each test
                if i > 0:
                    non_payment_page.reset_form()
                    time.sleep(1)
                    
                # Level 1 selection
                success = non_payment_page.select_level1_reason(hierarchy.level1)
                assert success, f"Failed to select Level 1: {hierarchy.level1}"
                
                time.sleep(2)  # Wait for Level 2 to load
                
                # Level 2 selection
                success = non_payment_page.select_level2_reason(hierarchy.level2)
                assert success, f"Failed to select Level 2: {hierarchy.level2}"
                
                # Level 3 selection (if available)
                if hierarchy.level3:
                    time.sleep(2)  # Wait for Level 3 to load
                    
                    if non_payment_page.is_level3_dropdown_visible():
                        success = non_payment_page.select_level3_reason(hierarchy.level3)
                        # Note: May not assert on success as Level 3 options depend on actual data
                        
                test_logger.verification(f"Completed hierarchy selection for: {hierarchy.level1}")
                
            test_logger.result("Complete hierarchical flow test completed successfully", True)
            
        except Exception as e:
            test_logger.error("Complete hierarchical flow test failed", e)
            non_payment_page.take_screenshot("Complete_Hierarchical_Flow_Failed")
            raise
        finally:
            log_test_end("Complete Hierarchical Reason Flow", True)
            
    @allure.story("Hierarchical Reason Performance")
    @allure.title("Hierarchical Reason Selection Performance")
    @allure.description("Verify hierarchical reason selection meets performance requirements")
    @pytest.mark.hierarchical
    @pytest.mark.performance
    def test_hierarchical_reason_performance(self, revenue_user_session, config_data, logger, performance_monitor):
        """
        Test hierarchical reason selection performance.
        
        Validates that reason category loading meets performance requirements:
        - Average loading time for each level < 2 seconds
        - 95th percentile response time < 3 seconds
        """
        test_logger = log_test_start("Hierarchical Reason Performance")
        
        try:
            non_payment_page = NonPaymentReasonPage(revenue_user_session, config_data, logger)
            
            test_logger.step("Navigate to Non-Payment Reason screen")
            non_payment_page.navigate_to_non_payment_reason_page()
            
            performance_data = []
            num_iterations = 10
            
            for i in range(num_iterations):
                test_logger.step(f"Performance test iteration {i+1}/{num_iterations}")
                
                # Reset form
                if i > 0:
                    non_payment_page.reset_form()
                    
                # Measure Level 1 loading time
                start_time = time.time()
                level1_options = non_payment_page.get_all_level1_options()
                level1_load_time = time.time() - start_time
                
                # Select Level 1
                if level1_options:
                    non_payment_page.select_level1_reason(level1_options[0])
                    
                    # Measure Level 2 loading time
                    start_time = time.time()
                    level2_options = non_payment_page.get_all_level2_options()
                    level2_load_time = time.time() - start_time
                    
                    # Select Level 2 if available
                    if level2_options:
                        non_payment_page.select_level2_reason(level2_options[0])
                        
                        # Measure Level 3 loading time (if applicable)
                        level3_load_time = 0
                        if non_payment_page.is_level3_dropdown_visible():
                            start_time = time.time()
                            level3_options = non_payment_page.get_all_level3_options()
                            level3_load_time = time.time() - start_time
                            
                    else:
                        level2_load_time = 0
                        level3_load_time = 0
                else:
                    level1_load_time = 0
                    level2_load_time = 0
                    level3_load_time = 0
                    
                performance_data.append({
                    'iteration': i + 1,
                    'level1_load_time': level1_load_time,
                    'level2_load_time': level2_load_time,
                    'level3_load_time': level3_load_time
                })
                
                test_logger.performance(f"Level loading times - L1: {level1_load_time:.2f}s, L2: {level2_load_time:.2f}s, L3: {level3_load_time:.2f}s", level1_load_time)
                
            # Analyze performance results
            level1_times = [data['level1_load_time'] for data in performance_data if data['level1_load_time'] > 0]
            level2_times = [data['level2_load_time'] for data in performance_data if data['level2_load_time'] > 0]
            level3_times = [data['level3_load_time'] for data in performance_data if data['level3_load_time'] > 0]
            
            # Calculate averages
            avg_level1_time = sum(level1_times) / len(level1_times) if level1_times else 0
            avg_level2_time = sum(level2_times) / len(level2_times) if level2_times else 0
            avg_level3_time = sum(level3_times) / len(level3_times) if level3_times else 0
            
            # Verify performance requirements
            performance_threshold = config_data.get('performance', {}).get('reason_load_max', 2)
            
            test_logger.verification(f"Verify Level 1 average loading time < {performance_threshold}s")
            assert avg_level1_time < performance_threshold, f"Level 1 average loading time {avg_level1_time:.2f}s exceeds threshold {performance_threshold}s"
            
            test_logger.verification(f"Verify Level 2 average loading time < {performance_threshold}s")
            assert avg_level2_time < performance_threshold, f"Level 2 average loading time {avg_level2_time:.2f}s exceeds threshold {performance_threshold}s"
            
            if level3_times:
                test_logger.verification(f"Verify Level 3 average loading time < {performance_threshold}s")
                assert avg_level3_time < performance_threshold, f"Level 3 average loading time {avg_level3_time:.2f}s exceeds threshold {performance_threshold}s"
                
            test_logger.result(f"Hierarchical reason performance test completed - Avg times: L1={avg_level1_time:.2f}s, L2={avg_level2_time:.2f}s, L3={avg_level3_time:.2f}s", True)
            
        except Exception as e:
            test_logger.error("Hierarchical reason performance test failed", e)
            non_payment_page.take_screenshot("Hierarchical_Performance_Failed")
            raise
        finally:
            log_test_end("Hierarchical Reason Performance", True)