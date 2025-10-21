"""
Unit Tests for EquipmentService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested (from Table 1.2):
1. Required Fields: FacilityId, Name, and InventoryCode must be provided
2. Uniqueness: InventoryCode must be unique across all Equipment
3. UsageDomain-SupportPhase Coherence: If UsageDomain is Electronics, 
   then SupportPhase must include Prototyping or Testing (cannot be Training only)
4. Delete Guard: Equipment cannot be deleted if referenced by an active Project

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
def valid_equipment_data():
    """Valid equipment data matching actual Equipment model fields."""
    return {
        'name': 'CNC Milling Machine',
        'description': 'High-precision CNC machine',
        'capabilities': 'Metal, Wood, Plastic milling',
        'inventory_code': 'EQ001',
        'usage_domain': 'Prototyping',
        'support_phase': 'Design',
        'facility_id': 1
    }


# ============================================================================
# BUSINESS RULE TESTS - Equipment Business Rules
# ============================================================================

@pytest.mark.unit
class TestEquipmentBusinessRules:
    """Test the 4 core business rules for Equipment entity (Table 1.2)."""
    
    def test_required_fields_all_missing(self, equipment_service):
        """
        Business Rule #1: Required Fields - FacilityId, Name, and InventoryCode must be provided.
        
        Regression: Prevents creation of equipment without required fields.
        
        Arrange: Equipment data missing all required fields
        Act: Attempt to create equipment
        Assert: ValidationError raised with required fields message
        """
        from django.core.exceptions import ValidationError
        
        # Arrange - Missing all required fields
        invalid_equipment = {
            'description': 'Equipment without required fields',
            'capabilities': 'Various capabilities'
            # Missing: facility_id, name, inventory_code - INVALID!
        }
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required"):
            equipment_service.create_equipment(invalid_equipment)
    
    def test_uniqueness_duplicate_inventory_code(self, equipment_service, valid_equipment_data):
        """
        Business Rule #2: Uniqueness - InventoryCode must be unique across all Equipment.
        
        Regression: Prevents duplicate inventory codes in the system.
        
        Arrange: Create first equipment with specific inventory code
        Act: Attempt to create second equipment with same inventory code
        Assert: ValidationError raised with 'Equipment.InventoryCode already exists' message
        """
        from django.core.exceptions import ValidationError
        
        # Arrange - Create first equipment
        equipment_service.create_equipment(valid_equipment_data)
        
        # Act & Assert - Try to create duplicate inventory code
        duplicate_equipment = {
            'name': 'Different Equipment Name',
            'inventory_code': 'EQ001',  # Same inventory code - INVALID!
            'description': 'Different description',
            'capabilities': 'Different capabilities',
            'usage_domain': 'Prototyping',
            'support_phase': 'Testing',
            'facility_id': 1
        }
        
        with pytest.raises(ValidationError, match="Equipment.InventoryCode already exists"):
            equipment_service.create_equipment(duplicate_equipment)
    
    def test_usage_domain_support_phase_coherence_electronics_invalid_phase(self, equipment_service):
        """
        Business Rule #3: UsageDomain-SupportPhase Coherence - Electronics equipment 
        must support Prototyping or Testing.
        
        Regression: Prevents Electronics equipment from supporting invalid phases.
        
        Arrange: Electronics equipment with Training support phase
        Act: Attempt to create equipment
        Assert: ValidationError raised with coherence violation message
        """
        from django.core.exceptions import ValidationError
        
        # Arrange - Electronics with Training phase (INVALID!)
        invalid_equipment = {
            'name': 'Electronics Equipment',
            'inventory_code': 'EQ002',
            'description': 'Electronics for training',
            'capabilities': 'Circuits and sensors',
            'usage_domain': 'Electronics',  # Electronics...
            'support_phase': 'Training',    # ...but Training phase - INVALID!
            'facility_id': 1
        }
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Electronics equipment must support Prototyping or Testing"):
            equipment_service.create_equipment(invalid_equipment)
    
    def test_usage_domain_support_phase_coherence_electronics_valid_prototyping(self, equipment_service):
        """
        Business Rule #3: UsageDomain-SupportPhase Coherence - Electronics equipment 
        CAN support Prototyping (positive test).
        
        Regression: Verifies Electronics with Prototyping is valid.
        
        Arrange: Electronics equipment with Prototyping support phase
        Act: Create equipment
        Assert: Equipment created successfully
        """
        # Arrange - Electronics with Prototyping (VALID!)
        valid_equipment = {
            'name': 'Electronics Equipment',
            'inventory_code': 'EQ003',
            'description': 'Electronics for prototyping',
            'capabilities': 'Circuits and sensors',
            'usage_domain': 'Electronics',
            'support_phase': 'Prototyping',  # Valid!
            'facility_id': 1
        }
        
        # Act
        equipment = equipment_service.create_equipment(valid_equipment)
        
        # Assert
        assert equipment is not None
        assert equipment.usage_domain == 'Electronics'
        assert equipment.support_phase == 'Prototyping'
    
    def test_delete_guard_equipment_referenced_by_active_project(self, equipment_service, valid_equipment_data):
        """
        Business Rule #4: Delete Guard - Cannot delete equipment referenced by active Project.
        
        Regression: Prevents deletion of equipment still in use by active projects.
        
        Arrange: Create equipment and link it to an active project
        Act: Attempt to delete the equipment
        Assert: ValidationError raised with 'Equipment referenced by active Project' message
        """
        from django.core.exceptions import ValidationError
        
        # Arrange - Create equipment
        equipment = equipment_service.create_equipment(valid_equipment_data)
        
        # Simulate linking to active project (mock repository handles this)
        equipment_service.repository.link_to_project(equipment.equipment_id, project_id=1, active=True)
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Equipment referenced by active Project"):
            equipment_service.delete_equipment(equipment.equipment_id)

