"""
Unit Tests for FacilityService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested:
1. Required Fields: Name, Location, and FacilityType must be provided
2. Name-Location Uniqueness: Combination must be unique
3. Deletion Constraints: Cannot delete if linked to Services/Equipment/Projects
4. Capabilities: Required when Services/Equipment exist

Test Pattern: AAA (Arrange-Act-Assert)
Isolation: MockFacilityRepository (No Database)
Speed: < 0.5 seconds for all tests
Focus: Business Rule Validation
"""

import pytest
from core.services.facility_service import FacilityService
from core.repositories.mock_facility_repository import MockFacilityRepository
from unittest.mock import Mock


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def facility_service():
    """
    Create a fresh FacilityService with mock repository for each test.
    This ensures test isolation - each test gets a clean slate.
    """
    mock_repo = MockFacilityRepository()
    return FacilityService(repository=mock_repo)


@pytest.fixture
def valid_facility_data():
    """Sample valid facility data matching actual Facility model fields."""
    return {
        'name': 'Innovation Lab Kampala',
        'location': 'Kampala, Central Region',
        'facility_type': 'Laboratory',
        'description': 'State-of-the-art innovation laboratory',
        'partner': 'UniPod',
        'capabilities': ['CNC', '3D Printing']
    }


@pytest.fixture
def another_facility_data():
    """Different valid facility data for testing scenarios."""
    return {
        'name': 'Maker Space Lwera',
        'location': 'Lwera Industrial Park',
        'description': 'Creative maker space for prototyping',
        'partner': 'Lwera',
        'facility_type': 'Maker Space',
        'capabilities': 'PCB Fabrication'
    }


@pytest.fixture
def facility_with_services(facility_service):
    """Create a facility with associated services."""
    facility_data = {
        'name': 'Service Lab',
        'location': 'Service Location',
        'facility_type': 'Laboratory',
        'description': 'Facility with services',
        'partner': 'ServicePartner',
        'capabilities': ['Service Testing']
    }
    facility = facility_service.create_facility(facility_data)
    # Mock service relationship
    facility.services = [Mock(service_id=1)]
    return facility


@pytest.fixture
def facility_with_equipment(facility_service):
    """Create a facility with associated equipment."""
    facility_data = {
        'name': 'Equipment Lab',
        'location': 'Equipment Location',
        'facility_type': 'Workshop',
        'description': 'Facility with equipment',
        'partner': 'EquipmentPartner',
        'capabilities': ['Equipment Testing']
    }
    facility = facility_service.create_facility(facility_data)
    # Mock equipment relationship
    facility.equipment = [Mock(equipment_id=1)]
    return facility


@pytest.fixture
def facility_with_projects(facility_service):
    """Create a facility with associated projects."""
    facility_data = {
        'name': 'Project Lab',
        'location': 'Project Location',
        'facility_type': 'Research',
        'description': 'Facility with projects',
        'partner': 'ProjectPartner',
        'capabilities': ['Project Testing']
    }
    facility = facility_service.create_facility(facility_data)
    # Mock project relationship
    facility.projects = [Mock(project_id=1)]
    return facility


# ============================================================================
# BUSINESS RULE TESTS - Facility Creation
# ============================================================================

@pytest.mark.unit
class TestFacilityBusinessRules:
    """Test the 4 core business rules for Facility entity."""
    
    def test_required_fields(self, facility_service):
        """
        Business Rule #1: Name, Location, and FacilityType are required fields.
        
        Error Message: "Facility.Name, Facility.Location, and Facility.FacilityType are required"
        """
        # Test missing name
        invalid_data = {
            'location': 'Kampala',
            'facility_type': 'Laboratory',
        }
        with pytest.raises(ValueError, match="Facility.Name, Facility.Location, and Facility.FacilityType are required"):
            facility_service.create_facility(invalid_data)

        # Test missing location
        invalid_data = {
            'name': 'Test Facility',
            'facility_type': 'Laboratory',
        }
        with pytest.raises(ValueError, match="Facility.Name, Facility.Location, and Facility.FacilityType are required"):
            facility_service.create_facility(invalid_data)

        # Test missing facility_type
        invalid_data = {
            'name': 'Test Facility',
            'location': 'Kampala',
        }
        with pytest.raises(ValueError, match="Facility.Name, Facility.Location, and Facility.FacilityType are required"):
            facility_service.create_facility(invalid_data)

    def test_name_location_uniqueness(self, facility_service, valid_facility_data):
        """
        Business Rule #2: Name and Location combination must be unique.
        
        Error Message: "A facility with this name already exists at this location"
        """
        # Create first facility
        facility_service.create_facility(valid_facility_data)

        # Try to create another facility with same name and location
        duplicate_data = valid_facility_data.copy()
        with pytest.raises(ValueError, match="A facility with this name already exists at this location"):
            facility_service.create_facility(duplicate_data)

        # Should allow same name at different location
        different_location = valid_facility_data.copy()
        different_location['location'] = 'Entebbe'
        facility_service.create_facility(different_location)  # Should not raise error

    def test_deletion_constraints(self, facility_service, facility_with_services, facility_with_equipment, facility_with_projects):
        """
        Business Rule #3: Cannot delete facilities with dependent records.
        
        Error Message: "Facility has dependent records (Services/Equipment/Projects)"
        """
        # Test with services
        with pytest.raises(ValueError, match="Facility has dependent records \\(Services/Equipment/Projects\\)"):
            facility_service.delete_facility(facility_with_services.facility_id)

        # Test with equipment
        with pytest.raises(ValueError, match="Facility has dependent records \\(Services/Equipment/Projects\\)"):
            facility_service.delete_facility(facility_with_equipment.facility_id)

        # Test with projects
        with pytest.raises(ValueError, match="Facility has dependent records \\(Services/Equipment/Projects\\)"):
            facility_service.delete_facility(facility_with_projects.facility_id)

    def test_capabilities_requirement(self, facility_service, valid_facility_data):
        """
        Business Rule #4: Capabilities required when Services/Equipment exist.
        
        Error Message: "Facility.Capabilities must be populated when Services/Equipment exist"
        """
        # Create facility without capabilities
        data_without_capabilities = valid_facility_data.copy()
        data_without_capabilities.pop('capabilities')
        facility = facility_service.create_facility(data_without_capabilities)
        
        # Mock service/equipment relationships
        facility.services = [Mock(service_id=1)]
        facility.equipment = []

        # Try to update without capabilities when services exist
        with pytest.raises(ValueError, match="Facility.Capabilities must be populated when Services/Equipment exist"):
            facility_service.update_facility(facility.facility_id, {'capabilities': []})

        # Add capabilities - should work
        facility_service.update_facility(facility.facility_id, {'capabilities': ['3D Printing']})
        updated = facility_service.get_facility_by_id(facility.facility_id)
        assert updated.capabilities == ['3D Printing']



