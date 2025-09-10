"""
Test data management utilities for Mobinet NextGen automation.
Provides test data generation, management, and validation functionality.
"""

import random
import string
from datetime import datetime, timedelta
from faker import Faker
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TestContract:
    """Test contract data structure."""
    contract_id: str
    customer_name: str
    status: str
    payment_due_date: str
    amount_due: float
    service_type: str


@dataclass
class ReasonHierarchy:
    """Reason hierarchy data structure."""
    level1: str
    level2: str = None
    level3: str = None


@dataclass
class AppointmentData:
    """Appointment data structure."""
    date: str
    time: str
    notes: str


@dataclass
class DisconnectData:
    """Service disconnection data structure."""
    option1: str
    option2: str = None
    disconnect_date: str = None
    status: str = None


class TestDataManager:
    """
    Manages test data generation and validation for automation tests.
    Provides realistic data for various test scenarios.
    """
    
    def __init__(self, config_data=None, logger=None):
        """
        Initialize test data manager.
        
        Args:
            config_data (dict): Configuration data
            logger: Logger instance
        """
        self.config_data = config_data or {}
        self.logger = logger
        self.faker = Faker(['en_US', 'vi_VN'])  # English and Vietnamese locales
        
        # Predefined test data from configuration
        self.predefined_contracts = config_data.get('test_data', {}).get('contracts', {})
        self.predefined_reasons = config_data.get('test_data', {}).get('reasons', {})
        
    def generate_test_contract(self, status="overdue"):
        """
        Generate test contract data.
        
        Args:
            status (str): Contract status ('overdue', 'paid', 'pending')
            
        Returns:
            TestContract: Generated contract data
        """
        contract = TestContract(
            contract_id=f"CON{random.randint(100000000, 999999999)}",
            customer_name=self.faker.name(),
            status=status,
            payment_due_date=(datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            amount_due=round(random.uniform(100000, 5000000), 2),  # VND amounts
            service_type=random.choice(["Mobile", "Internet", "TV", "Bundle"])
        )
        
        if self.logger:
            self.logger.debug(f"Generated test contract: {contract.contract_id}")
            
        return contract
        
    def get_predefined_contract(self, contract_type="valid"):
        """
        Get predefined contract from configuration.
        
        Args:
            contract_type (str): Type of contract ('valid', 'overdue', 'paid')
            
        Returns:
            str: Contract ID
        """
        contract_key = f"{contract_type}_contract_id"
        return self.predefined_contracts.get(contract_key, "CON001234567")
        
    def generate_reason_hierarchy_data(self):
        """
        Generate hierarchical reason data for testing.
        
        Returns:
            List[ReasonHierarchy]: List of reason hierarchies
        """
        reason_hierarchies = []
        
        # Financial issues hierarchy
        financial_reasons = [
            ReasonHierarchy("Customer Financial Issues", "Temporary Financial Hardship", "Job Loss Impact"),
            ReasonHierarchy("Customer Financial Issues", "Temporary Financial Hardship", "Medical Expenses"),
            ReasonHierarchy("Customer Financial Issues", "Business Cash Flow", "Seasonal Business Decline"),
        ]
        
        # Technical problems hierarchy
        technical_reasons = [
            ReasonHierarchy("System Technical Problems", "Network Connectivity", "Signal Quality Issues"),
            ReasonHierarchy("System Technical Problems", "Device Issues", "Equipment Malfunction"),
            ReasonHierarchy("System Technical Problems", "Software Problems", "Application Errors"),
        ]
        
        # Service quality hierarchy
        service_reasons = [
            ReasonHierarchy("Service Quality Issues", "Poor Network Coverage", "Indoor Coverage Problems"),
            ReasonHierarchy("Service Quality Issues", "Service Interruptions", "Frequent Disconnections"),
            ReasonHierarchy("Service Quality Issues", "Speed Issues", "Slow Data Connection"),
        ]
        
        # Billing disputes hierarchy
        billing_reasons = [
            ReasonHierarchy("Billing Disputes", "Incorrect Charges", "Unauthorized Services"),
            ReasonHierarchy("Billing Disputes", "Billing Errors", "Double Billing"),
            ReasonHierarchy("Billing Disputes", "Rate Plan Issues", "Unexpected Rate Changes"),
        ]
        
        reason_hierarchies.extend(financial_reasons)
        reason_hierarchies.extend(technical_reasons)
        reason_hierarchies.extend(service_reasons)
        reason_hierarchies.extend(billing_reasons)
        
        return reason_hierarchies
        
    def generate_appointment_data(self, days_ahead=1):
        """
        Generate appointment data for future dates.
        
        Args:
            days_ahead (int): Number of days in the future
            
        Returns:
            AppointmentData: Generated appointment data
        """
        appointment_date = datetime.now() + timedelta(days=days_ahead)
        
        # Generate appointment time (business hours)
        appointment_times = [
            "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"
        ]
        
        appointment = AppointmentData(
            date=appointment_date.strftime("%Y-%m-%d"),
            time=random.choice(appointment_times),
            notes=self.faker.sentence(nb_words=10)
        )
        
        return appointment
        
    def generate_disconnect_data(self, include_date=True):
        """
        Generate service disconnection data.
        
        Args:
            include_date (bool): Whether to include disconnect date
            
        Returns:
            DisconnectData: Generated disconnect data
        """
        disconnect = DisconnectData(
            option1="Option 2: Disconnect after Option 1 and until end of month disconnect completely",
            option2="Select specific disconnect date",
            status=random.choice(["Maintain", "Temporary"])
        )
        
        if include_date:
            # Generate disconnect date between 13th and end of month, in future
            current_date = datetime.now()
            
            # If current date is after 13th, use next month
            if current_date.day >= 13:
                next_month = current_date.replace(month=current_date.month + 1, day=1)
                disconnect_day = random.randint(13, 28)  # Safe range for any month
                disconnect_date = next_month.replace(day=disconnect_day)
            else:
                # Use current month
                disconnect_day = random.randint(max(13, current_date.day + 1), 28)
                disconnect_date = current_date.replace(day=disconnect_day)
                
            disconnect.disconnect_date = disconnect_date.strftime("%Y-%m-%d")
            
        return disconnect
        
    def generate_notes_text(self, length="medium"):
        """
        Generate notes text for testing.
        
        Args:
            length (str): Length of notes ('short', 'medium', 'long')
            
        Returns:
            str: Generated notes text
        """
        if length == "short":
            return self.faker.sentence(nb_words=5)
        elif length == "medium":
            return self.faker.paragraph(nb_sentences=3)
        elif length == "long":
            return self.faker.text(max_nb_chars=500)
        else:
            return self.faker.sentence(nb_words=10)
            
    def generate_invalid_data_scenarios(self):
        """
        Generate invalid data scenarios for negative testing.
        
        Returns:
            Dict[str, Any]: Dictionary of invalid data scenarios
        """
        scenarios = {
            "empty_notes": "",
            "whitespace_only_notes": "   \n\t   ",
            "past_appointment_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "invalid_disconnect_date_early": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),  # Before 13th
            "past_disconnect_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "special_characters_notes": "!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
            "very_long_notes": "A" * 1000,  # Excessively long text
            "sql_injection_attempt": "'; DROP TABLE users; --",
            "xss_attempt": "<script>alert('XSS')</script>",
        }
        
        return scenarios
        
    def get_test_data_combinations(self):
        """
        Generate various combinations of test data for comprehensive testing.
        
        Returns:
            List[Dict]: List of test data combinations
        """
        combinations = []
        
        # Basic positive scenarios
        reason_hierarchies = self.generate_reason_hierarchy_data()
        
        for i, reason in enumerate(reason_hierarchies[:5]):  # Limit to 5 for efficiency
            combination = {
                "scenario_name": f"Valid Reason Hierarchy {i+1}",
                "contract": self.generate_test_contract(),
                "reason_hierarchy": reason,
                "appointment": self.generate_appointment_data(days_ahead=i+1),
                "disconnect": self.generate_disconnect_data() if i % 2 == 0 else None,
                "notes": self.generate_notes_text(),
                "expected_result": "success"
            }
            combinations.append(combination)
            
        # Negative scenarios
        invalid_data = self.generate_invalid_data_scenarios()
        
        for key, invalid_value in invalid_data.items():
            combination = {
                "scenario_name": f"Invalid Data - {key}",
                "contract": self.generate_test_contract(),
                "reason_hierarchy": reason_hierarchies[0],  # Use valid hierarchy
                "appointment": self.generate_appointment_data(),
                "disconnect": None,
                "notes": invalid_value if "notes" in key else self.generate_notes_text(),
                "invalid_field": key,
                "expected_result": "validation_error"
            }
            
            # Override specific fields for date-related scenarios
            if "appointment_date" in key:
                combination["appointment"].date = invalid_value
            elif "disconnect_date" in key:
                combination["disconnect"] = self.generate_disconnect_data()
                combination["disconnect"].disconnect_date = invalid_value
                
            combinations.append(combination)
            
        return combinations
        
    def validate_business_rules(self, data):
        """
        Validate data against business rules.
        
        Args:
            data (dict): Test data to validate
            
        Returns:
            Dict[str, List[str]]: Validation results with errors
        """
        validation_results = {
            "valid": True,
            "errors": []
        }
        
        # Validate appointment date (must be current or future)
        if "appointment" in data and data["appointment"]:
            appointment_date = datetime.strptime(data["appointment"].date, "%Y-%m-%d")
            if appointment_date < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                validation_results["valid"] = False
                validation_results["errors"].append("Appointment date must be current or future date")
                
        # Validate disconnect date (must be between 13th and end of month, greater than current date)
        if "disconnect" in data and data["disconnect"] and data["disconnect"].disconnect_date:
            disconnect_date = datetime.strptime(data["disconnect"].disconnect_date, "%Y-%m-%d")
            
            if disconnect_date <= datetime.now():
                validation_results["valid"] = False
                validation_results["errors"].append("Disconnect date must be greater than current date")
                
            if disconnect_date.day < 13:
                validation_results["valid"] = False
                validation_results["errors"].append("Disconnect date must be between 13th and end of month")
                
        # Validate notes (cannot be empty or whitespace only)
        if "notes" in data:
            if not data["notes"] or data["notes"].strip() == "":
                validation_results["valid"] = False
                validation_results["errors"].append("Notes field cannot be empty")
                
        # Validate reason hierarchy (Level 1 and Level 2 are mandatory)
        if "reason_hierarchy" in data:
            reason = data["reason_hierarchy"]
            if not reason.level1:
                validation_results["valid"] = False
                validation_results["errors"].append("Level 1 reason is mandatory")
            if not reason.level2:
                validation_results["valid"] = False
                validation_results["errors"].append("Level 2 reason is mandatory")
                
        return validation_results
        
    def create_performance_test_data(self, num_records=100):
        """
        Create large dataset for performance testing.
        
        Args:
            num_records (int): Number of test records to generate
            
        Returns:
            List[Dict]: List of performance test data
        """
        performance_data = []
        
        for i in range(num_records):
            data = {
                "id": i + 1,
                "contract": self.generate_test_contract(),
                "reason_hierarchy": random.choice(self.generate_reason_hierarchy_data()),
                "appointment": self.generate_appointment_data(days_ahead=random.randint(1, 30)),
                "notes": self.generate_notes_text("medium"),
                "timestamp": datetime.now().isoformat()
            }
            
            # Add disconnect data for Revenue Collection scenarios
            if i % 3 == 0:  # 1/3 of records have disconnect data
                data["disconnect"] = self.generate_disconnect_data()
                
            performance_data.append(data)
            
        if self.logger:
            self.logger.info(f"Generated {num_records} performance test records")
            
        return performance_data
        
    def get_role_specific_test_data(self, role):
        """
        Get role-specific test data.
        
        Args:
            role (str): User role ('revenue_collection', 'customer_care', etc.)
            
        Returns:
            Dict: Role-specific test data
        """
        base_data = {
            "contract": self.generate_test_contract(),
            "reason_hierarchy": random.choice(self.generate_reason_hierarchy_data()),
            "appointment": self.generate_appointment_data(),
            "notes": self.generate_notes_text()
        }
        
        # Add disconnect data only for Revenue Collection role
        if role == "revenue_collection":
            base_data["disconnect"] = self.generate_disconnect_data()
            
        return base_data