"""
Unit Tests for EquipmentService - Business Rules ONLY

This test suite focuse        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError, match="Inventory code.*already exists"):
            equipment_service.create_equipment(duplicate_equipment)exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested:
1. Unique inventory code
2. Belongs to one facility  
3. Cannot delete equipment linked to active projects
4. Valid domain and support phase choices

Test Pattern: AAA (Arrange-Act-Assert)
Isolation: MockEquipmentRepository (No Database)
Speed: < 0.5 seconds for all tests
Focus: Business Rule Violations
"""

import pytest
from core.services.equipment_service import EquipmentService
from core.repositories.mock_equipment_repository import MockEquipmentRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def equipment_service():
    """
    Create a fresh EquipmentService with mock repository for each test.
    This ensures test isolation - each test gets a clean slate.
    """
    mock_repo = MockEquipmentRepository()
    mock_repo.clear()  # Clear any existing test data
    return EquipmentService(repository=mock_repo)


@pytest.fixture
def another_equipment_data():
    """Different valid equipment data for testing scenarios."""
    return {
        'name': '3D Printer Delta',
        'description': 'Professional 3D printing system',
        'capabilities': 'PLA, ABS, PETG printing',
        'inventory_code': 'EQ002',
        'usage_domain': 'Prototyping',
        'support_phase': 'Design',
        'facility_id': 1
    }


# ============================================================================
# BUSINESS RULE TESTS - Equipment Business Rules
# ============================================================================

@pytest.mark.unit
class TestEquipmentBusinessRules:
    """Test the 4 core business rules for Equipment entity."""
    
    def test_unique_inventory_code(self, equipment_service, valid_equipment_data):
        """
        Business Rule #1: Unique inventory code - Prevent duplicates.
        
        Regression: Prevents duplicate inventory codes in the system.
        
        Arrange: Create first equipment with specific inventory code
        Act: Attempt to create second equipment with same inventory code
        Assert: ValidationError raised with 'already exists' message
        """
        from django.core.exceptions import ValidationError
        
        # Arrange - Clear mock data and create first equipment
        equipment_service.repository.clear()
        equipment_service.create_equipment(valid_equipment_data)
        
        # Act & Assert - Try to create duplicate inventory code
        duplicate_equipment = {
            'name': 'Different Equipment Name',
            'inventory_code': 'EQ001',  # Same inventory code!
            'description': 'Different description',
            'capabilities': 'Different capabilities',
            'usage_domain': 'Research',
            'support_phase': 'Design',
            'facility_id': 1
        }
        
        with pytest.raises(ValidationError, match="Inventory code.*already exists"):
            equipment_service.create_equipment(duplicate_equipment)
    
    def test_belongs_to_one_facility(self, equipment_service):
        """
        Business Rule #2: Belongs to one facility - Validate linkage.
        
        Regression: Ensures equipment is properly linked to a facility.
        
        Arrange: Equipment data without facility_id
        Act: Attempt to create equipment  
        Assert: ValueError raised with 'facility is required' message
        """
        # Arrange
        invalid_equipment = {
            'name': 'Orphaned Equipment',
            'inventory_code': 'EQ002',
            'description': 'Equipment without facility',
            'capabilities': 'Various capabilities',
            'usage_domain': 'Research',
            'support_phase': 'Design'
            # Missing facility_id - INVALID!
        }
        
        # Act & Assert
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError, match="must be linked to a facility"):
            equipment_service.create_equipment(invalid_equipment)
    
    def test_cannot_delete_equipment_linked_to_active_projects(self, equipment_service, valid_equipment_data):
        """
        Business Rule #3: Cannot delete equipment linked to active projects - Data consistency rule.
        
        Regression: Prevents deletion of equipment still in use by active projects.
        
        Arrange: Create equipment and link it to an active project
        Act: Attempt to delete the equipment
        Assert: ValueError raised with 'linked to active projects' message
        """
        # Arrange - Create equipment
        equipment = equipment_service.create_equipment(valid_equipment_data)
        
        # Simulate linking to active project (mock repository handles this)
        equipment_service.repository.link_to_project(equipment.equipment_id, project_id=1, active=True)
        
        # Act & Assert
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError, match="assigned to active projects"):
            equipment_service.delete_equipment(equipment.equipment_id)
    
    def test_valid_domain_and_support_phase_choices(self, equipment_service):
        """
        Business Rule #4: Valid domain and support phase choices - Ensure controlled values.
        
        Regression: Ensures only valid domain and support phase values are accepted.
        
        Arrange: Equipment data with invalid usage_domain
        Act: Attempt to create equipment
        Assert: ValueError raised with 'invalid usage domain' message
        """
        # Test invalid usage_domain
        invalid_domain_equipment = {
            'name': 'Test Equipment',
            'inventory_code': 'EQ003',
            'description': 'Test equipment with invalid domain',
            'capabilities': 'Testing capabilities',
            'usage_domain': 'InvalidDomain',  # INVALID!
            'support_phase': 'Design',
            'facility_id': 1
        }
        
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError, match="Invalid usage_domain"):
            equipment_service.create_equipment(invalid_domain_equipment)
        
        # Test invalid support_phase
        invalid_phase_equipment = {
            'name': 'Test Equipment 2',
            'inventory_code': 'EQ004',
            'description': 'Test equipment with invalid phase',
            'capabilities': 'Testing capabilities',
            'usage_domain': 'Research',
            'support_phase': 'InvalidPhase',  # INVALID!
            'facility_id': 1
        }
        
        with pytest.raises(ValidationError, match="Invalid support_phase"):
            equipment_service.create_equipment(invalid_phase_equipment)

