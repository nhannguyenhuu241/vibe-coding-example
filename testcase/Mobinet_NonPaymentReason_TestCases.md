# Mobinet NextGen - Non-Payment Reason Management Module Test Cases

## Test Case Overview
**Module**: Non-Payment Reason Management (Trả lý do không thanh toán)  
**Test Type**: Comprehensive Functional, Integration, and Performance Testing  
**Target Roles**: Revenue Collection (Thu cước)  
**Version**: 1.0  
**Date**: 2025-09-10

## Test Environment Setup

### Prerequisites
- Mobinet NextGen system deployed and accessible
- Test user accounts with Revenue Collection role
- Integration with Customer Debt Management Tool active
- Integration with Customer Management System active
- Integration with Customer Care Platform active
- Test contracts with various payment statuses

### Test Data Requirements
- Valid contracts with different payment statuses
- Complete reason hierarchy data (Level 1, 2, 3)
- Historical non-payment reason records
- Test dates covering current month and future dates

---

## Functional Test Cases

### TC-001: Hierarchical Reason Management

#### TC-001.1: Level 1 Reason Selection
**Test Objective**: Verify Level 1 reason selection functionality
**Preconditions**: User has access to Non-Payment Reason screen
**Test Steps**:
1. Navigate to Non-Payment Reason screen
2. Verify Level 1 dropdown is displayed and empty by default
3. Click Level 1 dropdown
4. Verify complete list of Level 1 reasons loads
5. Select a Level 1 reason
6. Verify selection is saved and displayed

**Expected Results**:
- Level 1 dropdown displays all available reasons
- Selection updates the dropdown display
- Level 2 dropdown becomes available after selection

**Test Data**: Level 1 reasons from system database

#### TC-001.2: Level 2 Reason Dependency
**Test Objective**: Verify Level 2 reasons filter correctly based on Level 1 selection
**Preconditions**: Level 1 reason selected
**Test Steps**:
1. Select different Level 1 reasons
2. For each Level 1 selection, verify Level 2 dropdown updates
3. Verify Level 2 only shows reasons related to selected Level 1
4. Select a Level 2 reason
5. Verify selection is saved

**Expected Results**:
- Level 2 dropdown shows only filtered reasons
- Level 2 selection enables Level 3 dropdown
- Changing Level 1 resets Level 2 and Level 3 selections

#### TC-001.3: Level 3 Reason Conditional Display
**Test Objective**: Verify Level 3 reasons display logic
**Preconditions**: Level 1 and Level 2 reasons selected
**Test Steps**:
1. Verify Level 3 dropdown is hidden initially
2. Select Level 1 reason
3. Verify Level 3 remains hidden
4. Select Level 2 reason
5. Verify Level 3 dropdown appears
6. Verify Level 3 shows only reasons filtered by Level 1 and Level 2
7. Select Level 3 reason

**Expected Results**:
- Level 3 only appears after Level 1 and Level 2 selection
- Level 3 shows correctly filtered reasons
- All three levels maintain proper hierarchy

### TC-002: Form Validation

#### TC-002.1: Mandatory Field Validation
**Test Objective**: Verify all mandatory fields are properly validated
**Preconditions**: User on Non-Payment Reason screen
**Test Steps**:
1. Leave Level 1 reason empty and attempt to submit
2. Verify error message: "Please enter complete information"
3. Select Level 1, leave Level 2 empty and attempt to submit
4. Verify error message appears for Level 2
5. Select Level 1 and Level 2, leave Level 3 empty (when applicable) and attempt to submit
6. Verify error message appears for Level 3
7. Leave Notes field empty and attempt to submit
8. Verify error message appears for Notes

**Expected Results**:
- Error message "Please enter complete information" displays for each missing mandatory field
- Form submission is blocked until all mandatory fields are completed
- Error messages are clear and actionable

#### TC-002.2: Notes Field Validation
**Test Objective**: Verify notes field requirements
**Preconditions**: User on Non-Payment Reason screen
**Test Steps**:
1. Leave notes field completely empty
2. Attempt to submit form
3. Enter whitespace only in notes field
4. Attempt to submit form
5. Enter valid text in notes field
6. Submit form

**Expected Results**:
- Empty notes field triggers validation error
- Whitespace-only notes should trigger validation error
- Valid notes allow form submission

### TC-003: Payment Appointment Scheduling

#### TC-003.1: Date Selection Functionality
**Test Objective**: Verify payment appointment date selection
**Preconditions**: User on Non-Payment Reason screen
**Test Steps**:
1. Verify date selection is enabled by default
2. Click date picker
3. Verify current date and future dates are selectable
4. Attempt to select past dates
5. Verify past dates are disabled/not selectable
6. Select a valid future date
7. Verify time selection appears after date selection

**Expected Results**:
- Date picker allows current and future dates only
- Past dates are disabled
- Time selection appears after date selection
- Selected date/time is properly stored

#### TC-003.2: Date Restriction Validation
**Test Objective**: Verify business rules for date restrictions
**Preconditions**: User on Payment Appointment section
**Test Steps**:
1. Try to select yesterday's date (should be disabled)
2. Select today's date (should be allowed)
3. Select tomorrow's date (should be allowed)
4. Select date one week in future (should be allowed)
5. Verify selected dates display correctly

**Expected Results**:
- Past dates cannot be selected
- Current and future dates are selectable
- Date restrictions are enforced client-side and server-side

### TC-004: Service Disconnection Scheduling (Revenue Collection Only)

#### TC-004.1: First Option Box Logic
**Test Objective**: Verify first disconnection option behavior
**Preconditions**: User has Revenue Collection role
**Test Steps**:
1. Verify first option box is empty by default
2. Select "Option 2: Disconnect after Option 1 and until end of month disconnect completely"
3. Verify second option box appears
4. Select different option or clear selection
5. Verify second option box is hidden

**Expected Results**:
- First option box starts empty
- Selecting "Option 2" reveals second option box
- Other selections hide second option box

#### TC-004.2: Second Option Box Date Logic
**Test Objective**: Verify disconnect date selection rules
**Preconditions**: First option box set to "Option 2"
**Test Steps**:
1. Select "Cancel disconnect schedule"
2. Verify third option box is hidden
3. Select specific disconnect date option
4. Verify date picker appears
5. Try to select date <= current date
6. Verify dates 1-12 of month are disabled
7. Select valid date between 13th and end of month
8. Verify third option box appears starting from N+1 day

**Expected Results**:
- "Cancel disconnect schedule" hides third option box
- Date selection shows only valid dates (13th to month end, > current date)
- Invalid dates trigger appropriate error messages
- Third option box appears with proper date range

#### TC-004.3: Third Option Box Status Selection
**Test Objective**: Verify status selection in third option box
**Preconditions**: Valid disconnect date selected in second option box
**Test Steps**:
1. Verify third option box appears
2. Verify "Maintain" and "Temporary" options are available
3. Select "Maintain" status
4. Verify selection is saved
5. Select "Temporary" status
6. Verify selection is saved
7. Leave status unselected and attempt to submit
8. Verify validation error appears

**Expected Results**:
- Both status options are available
- Status selection is mandatory when third box is visible
- Validation prevents submission without status selection

### TC-005: Role-Based Access Control

#### TC-005.1: Revenue Collection Role Features
**Test Objective**: Verify Revenue Collection users see all features
**Preconditions**: User logged in with Revenue Collection role
**Test Steps**:
1. Navigate to Non-Payment Reason screen
2. Verify all reason selection dropdowns are visible
3. Verify payment appointment scheduling is available
4. Verify service disconnection scheduling options are visible
5. Verify historical tracking shows disconnect dates

**Expected Results**:
- All features are accessible for Revenue Collection role
- Service disconnection options are visible and functional

#### TC-005.2: Non-Revenue Collection Role Restrictions
**Test Objective**: Verify other roles have appropriate restrictions
**Preconditions**: User logged in with non-Revenue Collection role
**Test Steps**:
1. Navigate to Non-Payment Reason screen
2. Verify reason selection dropdowns are visible
3. Verify payment appointment scheduling is available
4. Verify service disconnection scheduling is hidden
5. Verify historical tracking excludes disconnect-related information

**Expected Results**:
- Basic features accessible for all roles
- Service disconnection features hidden for non-Revenue Collection roles

---

## Integration Test Cases

### TC-006: External System Synchronization

#### TC-006.1: Customer Debt Management Tool Integration
**Test Objective**: Verify data synchronization with Customer Debt Management Tool
**Preconditions**: Integration with Customer Debt Management Tool active
**Test Steps**:
1. Complete non-payment reason form with all fields
2. Submit form
3. Verify data is sent to Customer Debt Management Tool
4. Check that reason categories are properly mapped
5. Verify appointment date/time synchronization
6. Confirm disconnect date synchronization (for Revenue Collection)

**Expected Results**:
- All form data synchronizes correctly
- Field mapping follows specification requirements
- Real-time updates are reflected in external system

#### TC-006.2: Customer Management System Integration
**Test Objective**: Verify Customer Management System data flow
**Preconditions**: Integration with Customer Management System active
**Test Steps**:
1. Submit complete non-payment reason information
2. Verify contact information synchronization
3. Check appointment scheduling data transfer
4. Verify customer interaction history updates
5. Confirm proper field mapping as per specification

**Expected Results**:
- Contact information updates correctly
- Appointment data synchronizes in real-time
- Historical data maintains integrity

#### TC-006.3: Multi-System Integration Consistency
**Test Objective**: Verify data consistency across all integrated systems
**Preconditions**: All external systems active and accessible
**Test Steps**:
1. Submit non-payment reason with complete information
2. Verify same data appears correctly in all three systems
3. Update existing reason information
4. Verify updates propagate to all systems
5. Check data consistency after system refresh

**Expected Results**:
- Data remains consistent across all systems
- Updates propagate correctly
- No data discrepancies between systems

### TC-007: Data Mapping and Field Population

#### TC-007.1: Automatic Field Population
**Test Objective**: Verify automatic field mapping per specification
**Preconditions**: User submitting non-payment reason
**Test Steps**:
1. Complete and submit non-payment reason form
2. Verify in Customer Debt Management Tool:
   - "Contact Person" is left blank
   - "Payment Capability" is left blank
   - "Action" is left blank
   - "Contact Channel" is set to "MobiX"
   - "Care Result Notes" contains MobiX notes content
3. Verify appointment and disconnect information populates correctly

**Expected Results**:
- Specified fields are left blank as required
- "Contact Channel" automatically set to "MobiX"
- Notes transfer correctly from MobiX to external system

---

## Performance Test Cases

### TC-008: Response Time Requirements

#### TC-008.1: Reason Category Loading Performance
**Test Objective**: Verify reason category loading meets performance requirements
**Test Criteria**: Response time < 2 seconds
**Test Steps**:
1. Navigate to Non-Payment Reason screen
2. Measure time for Level 1 reasons to load
3. Select Level 1 reason and measure Level 2 loading time
4. Select Level 2 reason and measure Level 3 loading time
5. Repeat test 10 times and calculate average response time

**Expected Results**:
- Average loading time for each level < 2 seconds
- 95th percentile response time < 3 seconds

#### TC-008.2: Form Submission Performance
**Test Objective**: Verify update processing meets performance requirements
**Test Criteria**: Update processing < 3 seconds
**Test Steps**:
1. Complete all form fields
2. Submit form and measure processing time
3. Verify all external systems receive updates within timeframe
4. Repeat test with different data combinations
5. Test with maximum field content (longest notes, etc.)

**Expected Results**:
- Form submission processing < 3 seconds
- Performance consistent across different data inputs

#### TC-008.3: History Retrieval Performance
**Test Objective**: Verify history display meets performance requirements
**Test Criteria**: History retrieval < 2 seconds
**Test Steps**:
1. Navigate to reason history section
2. Measure time to load current month history
3. Test with contracts having extensive history
4. Test with contracts having minimal history
5. Repeat test multiple times for consistency

**Expected Results**:
- History loading time < 2 seconds consistently
- Performance stable regardless of history volume

#### TC-008.4: External System Integration Performance
**Test Objective**: Verify system integration meets performance requirements
**Test Criteria**: All external system updates < 5 seconds
**Test Steps**:
1. Submit complete non-payment reason form
2. Measure total time for all external system updates
3. Monitor each individual system update time
4. Test during peak usage hours
5. Test with network latency simulation

**Expected Results**:
- Total integration time < 5 seconds
- Individual system updates complete within allocated time
- Performance maintained under various network conditions

---

## Security and Audit Test Cases

### TC-009: Access Control and Authorization

#### TC-009.1: Role-Based Access Testing
**Test Objective**: Verify proper access control implementation
**Test Steps**:
1. Test with Revenue Collection role - verify full access
2. Test with other roles - verify appropriate restrictions
3. Attempt to access disconnection features with non-authorized role
4. Verify URL manipulation doesn't bypass restrictions
5. Test session timeout handling

**Expected Results**:
- Access controls enforce role-based restrictions
- Unauthorized access attempts are blocked
- Security measures prevent privilege escalation

#### TC-009.2: Data Privacy and Security
**Test Objective**: Verify secure handling of customer information
**Test Steps**:
1. Verify sensitive data is not logged in plain text
2. Check data transmission encryption
3. Verify customer data access is properly audited
4. Test data masking in logs and error messages
5. Verify secure session management

**Expected Results**:
- Customer data handled securely
- No sensitive information exposed in logs
- Proper encryption and audit trails maintained

### TC-010: Audit Trail and Change Tracking

#### TC-010.1: Complete Audit Logging
**Test Objective**: Verify comprehensive audit trail functionality
**Test Steps**:
1. Perform various reason updates
2. Verify all changes are logged with timestamps
3. Check staff identification in audit records
4. Verify change details are captured accurately
5. Test audit log integrity and tamper prevention

**Expected Results**:
- All user actions properly logged
- Audit records include complete change information
- Audit trail maintains data integrity

---

## Error Handling Test Cases

### TC-011: Validation Error Handling

#### TC-011.1: Date Validation Error Messages
**Test Objective**: Verify proper error messaging for date validation failures
**Test Steps**:
1. Attempt to select invalid disconnect date (before 13th of month)
2. Verify specific error message appears
3. Attempt to select past date for disconnect
4. Verify error message: "Operation failed. Only allows disconnect schedule updates from 13th to month end and cannot select dates less than or equal to current date."
5. Test various invalid date combinations

**Expected Results**:
- Error messages are specific and actionable
- Users understand exactly what needs to be corrected

#### TC-011.2: System Integration Error Handling
**Test Objective**: Verify handling of external system connection failures
**Test Steps**:
1. Simulate Customer Debt Management Tool unavailability
2. Attempt to submit form
3. Verify appropriate error message displays
4. Simulate partial system failures
5. Test retry mechanisms
6. Verify transaction rollback on failures

**Expected Results**:
- Clear error messages for system integration issues
- Data integrity maintained during failures
- Appropriate retry mechanisms function correctly

### TC-012: Data Consistency and Recovery

#### TC-012.1: Transaction Rollback Testing
**Test Objective**: Verify data integrity during system failures
**Test Steps**:
1. Submit form while simulating system failure mid-process
2. Verify partial updates are rolled back
3. Test recovery after system restoration
4. Verify no orphaned or inconsistent data remains
5. Test various failure scenarios

**Expected Results**:
- Data integrity maintained during failures
- Proper rollback mechanisms prevent data corruption
- System recovery restores consistent state

---

## User Interface Test Cases

### TC-013: Screen Layout and Navigation

#### TC-013.1: Conditional Field Display
**Test Objective**: Verify proper show/hide logic for dependent fields
**Test Steps**:
1. Verify Level 3 is hidden initially
2. Test Level 3 appearance after Level 1 and Level 2 selection
3. Verify disconnect option boxes appear/hide correctly
4. Test field visibility with different user roles
5. Verify responsive layout on different screen sizes

**Expected Results**:
- Fields appear and hide according to business rules
- Layout remains functional across different screen sizes
- Visual hierarchy is clear and intuitive

#### TC-013.2: Date Picker Integration
**Test Objective**: Verify date and time selection user experience
**Test Steps**:
1. Test date picker functionality
2. Verify calendar navigation
3. Test time selection interface
4. Verify selected values display correctly
5. Test date picker accessibility features

**Expected Results**:
- Date picker is user-friendly and intuitive
- Time selection integrates seamlessly
- Accessibility standards are met

#### TC-013.3: Navigation Flow
**Test Objective**: Verify proper navigation between screens
**Test Steps**:
1. Navigate from Payment screen via three-dot menu
2. Complete reason update
3. Verify return to reason history display
4. Test navigation with unsaved changes
5. Verify data persistence during navigation

**Expected Results**:
- Navigation flow matches specification
- Data persistence works correctly
- User experience is smooth and intuitive

---

## Regression Test Cases

### TC-014: Existing Functionality Impact

#### TC-014.1: Payment Screen Integration
**Test Objective**: Verify new module doesn't affect existing payment functionality
**Test Steps**:
1. Test existing payment processes
2. Verify three-dot menu addition doesn't break existing features
3. Test payment screen performance after integration
4. Verify existing payment workflows remain intact

**Expected Results**:
- Existing payment functionality unaffected
- Performance remains acceptable
- No regressions in established workflows

---

## Test Execution Guidelines

### Test Data Management
- Use dedicated test environment with isolated data
- Maintain test data sets for different scenarios
- Reset test environment between test runs
- Document test data requirements for each test case

### Test Environment Requirements
- Staging environment matching production configuration
- All external system integrations must be available
- Test user accounts with appropriate role assignments
- Network simulation tools for performance testing

### Defect Reporting
- Document all deviations from expected results
- Include screenshots and detailed reproduction steps
- Classify defects by severity and priority
- Track defect resolution and retest requirements

### Test Completion Criteria
- All test cases executed with pass/fail results documented
- No critical or high-severity defects remaining open
- Performance requirements validated and met
- Integration functionality verified across all systems
- User acceptance criteria confirmed by business stakeholders

---

## Test Schedule and Resource Allocation

### Testing Phases
1. **Unit Testing**: Individual component functionality
2. **Integration Testing**: External system connectivity and data flow
3. **System Testing**: End-to-end business process validation
4. **Performance Testing**: Response time and load validation
5. **Security Testing**: Access control and audit functionality
6. **User Acceptance Testing**: Business stakeholder validation

### Test Execution Estimates
- **Functional Testing**: 40 hours
- **Integration Testing**: 24 hours
- **Performance Testing**: 16 hours
- **Security Testing**: 8 hours
- **Regression Testing**: 16 hours
- **Total Estimated Effort**: 104 hours

---

*This comprehensive test case specification ensures thorough validation of the Non-Payment Reason Management module functionality, performance, security, and integration requirements.*