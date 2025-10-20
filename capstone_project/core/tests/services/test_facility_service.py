"""
Unit Tests for FacilityService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested:
1. Facility name must be unique
2. Facility name must be at least 3 characters
3. Location is required

Test Pattern: AAA (Arrange-Act-Assert)
Isolation: MockFacilityRepository (No Database)
Speed: < 0.5 seconds for all tests
Focus: Business Rule Violations
"""

import pytest
from core.services.facility_service import FacilityService
from core.repositories.mock_facility_repository import MockFacilityRepository


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
        'description': 'State-of-the-art innovation laboratory',
        'partner': 'UniPod',
        'facility_type': 'Laboratory',
        'capabilities': 'CNC'
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


# ============================================================================
# BUSINESS RULE TESTS - Facility Creation
# ============================================================================

@pytest.mark.unit
class TestFacilityBusinessRules:
    """Test the 3 core business rules for Facility entity."""
    
    def test_facility_name_must_be_unique(self, facility_service, valid_facility_data):
        """
        Business Rule #1: Facility name must be unique.
        
        Regression: Prevents duplicate facility names in the system.
        
        Arrange: Create first facility with a specific name
        Act: Attempt to create second facility with same name
        Assert: ValueError raised with 'already exists' message
        """
        # Arrange - Create first facility
        facility_service.create_facility(valid_facility_data)
        
        # Act & Assert - Try to create duplicate
        duplicate_facility = {
            'name': 'Innovation Lab Kampala',  # Same name!
            'location': 'Different Location, Uganda',
            'description': 'Different description',
            'partner': 'UIRI',
            'facility_type': 'Workshop',
            'capabilities': 'Materials Testing'
        }
        
        with pytest.raises(ValueError, match="already exists"):
            facility_service.create_facility(duplicate_facility)
    
    def test_facility_name_minimum_length(self, facility_service):
        """
        Business Rule #2: Facility name must be at least 3 characters.
        
        Regression: Prevents meaningless single/double character names.
        
        Arrange: Facility data with 2-character name
        Act: Attempt to create facility
        Assert: ValueError raised with 'at least 3 characters' message
        """
        # Arrange
        invalid_facility = {
            'name': 'AI',  # Only 2 characters - INVALID!
            'location': 'Kampala, Uganda',
            'description': 'Artificial Intelligence lab',
            'partner': 'UniPod',
            'facility_type': 'Laboratory',
            'capabilities': 'CNC'
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="at least 3 characters"):
            facility_service.create_facility(invalid_facility)
    
    def test_location_is_required(self, facility_service):
        """
        Business Rule #3: Location is required.
        
        Regression: Prevents facilities without location information.
        
        Arrange: Facility data with empty/missing location
        Act: Attempt to create facility
        Assert: ValueError raised with 'Location is required' message
        """
        # Test with empty location
        invalid_facility_empty = {
            'name': 'Valid Lab Name',
            'location': '',  # Empty location - INVALID!
            'description': 'Testing location validation',
            'partner': 'UniPod',
            'facility_type': 'Laboratory',
            'capabilities': 'CNC'
        }
        
        with pytest.raises(ValueError, match="Location is required"):
            facility_service.create_facility(invalid_facility_empty)
        
        # Test with missing location
        invalid_facility_missing = {
            'name': 'Valid Lab Name',
            # No location field - INVALID!
            'description': 'Testing location validation',
            'partner': 'UniPod',
            'facility_type': 'Laboratory',
            'capabilities': 'CNC'
        }
        
        with pytest.raises(ValueError, match="Location is required"):
            facility_service.create_facility(invalid_facility_missing)


# ============================================================================
# BUSINESS LOGIC TESTS - CRUD Operations
# ============================================================================

@pytest.mark.unit
class TestFacilityServiceOperations:
    """Test facility service CRUD operations and business logic."""
    
    def test_create_facility_success(self, facility_service, valid_facility_data):
        """
        Test successful facility creation with valid data.
        
        Arrange: Valid facility data
        Act: Create facility
        Assert: Facility created with correct attributes
        """
        # Act
        facility = facility_service.create_facility(valid_facility_data)
        
        # Assert
        assert facility is not None
        assert facility.name == 'Innovation Lab Kampala'
        assert facility.location == 'Kampala, Central Region'
        assert facility.partner == 'UniPod'
        assert facility.facility_type == 'Laboratory'
    
    def test_get_all_facilities(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test retrieving all facilities.
        
        Arrange: Create multiple facilities
        Act: Get all facilities
        Assert: All facilities returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)
        facility_service.create_facility(another_facility_data)
        
        # Act
        facilities = facility_service.get_all_facilities()
        
        # Assert
        assert len(facilities) == 2
        facility_names = [f.name for f in facilities]
        assert 'Innovation Lab Kampala' in facility_names
        assert 'Maker Space Lwera' in facility_names
    
    def test_get_facility_by_id_success(self, facility_service, valid_facility_data):
        """
        Test retrieving facility by ID.
        
        Arrange: Create a facility
        Act: Get facility by ID
        Assert: Correct facility returned
        """
        # Arrange
        created_facility = facility_service.create_facility(valid_facility_data)
        
        # Act
        facility = facility_service.get_facility_by_id(created_facility.facility_id)
        
        # Assert
        assert facility is not None
        assert facility.name == 'Innovation Lab Kampala'
        assert facility.facility_id == created_facility.facility_id
    
    def test_get_facility_by_id_not_found(self, facility_service):
        """
        Test retrieving non-existent facility.
        
        Arrange: Empty repository
        Act: Get facility by non-existent ID
        Assert: None returned
        """
        # Act
        facility = facility_service.get_facility_by_id(999)
        
        # Assert
        assert facility is None
    
    def test_update_facility_success(self, facility_service, valid_facility_data):
        """
        Test successful facility update.
        
        Arrange: Create facility
        Act: Update facility with new data
        Assert: Facility updated correctly
        """
        # Arrange
        facility = facility_service.create_facility(valid_facility_data)
        update_data = {
            'description': 'Updated laboratory description',
            'partner': 'UIRI'
        }
        
        # Act
        updated_facility = facility_service.update_facility(facility.facility_id, update_data)
        
        # Assert
        assert updated_facility.description == 'Updated laboratory description'
        assert updated_facility.partner == 'UIRI'
        assert updated_facility.name == 'Innovation Lab Kampala'  # Unchanged
    
    def test_update_facility_with_unique_name_check(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test updating facility name to existing name fails.
        
        Arrange: Create two facilities
        Act: Try to update first facility's name to second facility's name
        Assert: ValueError raised for duplicate name
        """
        # Arrange
        facility1 = facility_service.create_facility(valid_facility_data)
        facility_service.create_facility(another_facility_data)
        
        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            facility_service.update_facility(facility1.facility_id, {
                'name': 'Maker Space Lwera'  # Name of second facility
            })
    
    def test_update_facility_not_found(self, facility_service):
        """
        Test updating non-existent facility.
        
        Arrange: Empty repository
        Act: Try to update non-existent facility
        Assert: ValueError raised for facility not found
        """
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            facility_service.update_facility(999, {'name': 'New Name'})
    
    def test_delete_facility_success(self, facility_service, valid_facility_data):
        """
        Test successful facility deletion.
        
        Arrange: Create facility
        Act: Delete facility
        Assert: Facility deleted and returns True
        """
        # Arrange
        facility = facility_service.create_facility(valid_facility_data)
        
        # Act
        result = facility_service.delete_facility(facility.facility_id)
        
        # Assert
        assert result is True
        assert facility_service.get_facility_by_id(facility.facility_id) is None
    
    def test_delete_facility_not_found(self, facility_service):
        """
        Test deleting non-existent facility.
        
        Arrange: Empty repository
        Act: Try to delete non-existent facility
        Assert: Returns False
        """
        # Act
        result = facility_service.delete_facility(999)
        
        # Assert
        assert result is False


# ============================================================================
# SEARCH AND FILTER TESTS
# ============================================================================

@pytest.mark.unit
class TestFacilitySearchAndFilter:
    """Test facility search and filtering functionality."""
    
    def test_search_facilities_by_name(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test searching facilities by name.
        
        Arrange: Create facilities with different names
        Act: Search by partial name
        Assert: Matching facilities returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)
        facility_service.create_facility(another_facility_data)
        
        # Act
        results = facility_service.search_facilities(name='Innovation')
        
        # Assert
        assert len(results) == 1
        assert results[0].name == 'Innovation Lab Kampala'
    
    def test_filter_by_type(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test filtering facilities by type.
        
        Arrange: Create facilities with different types
        Act: Filter by specific type
        Assert: Only matching facilities returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)  # Laboratory
        facility_service.create_facility(another_facility_data)  # Maker Space
        
        # Act
        laboratories = facility_service.filter_by_type('Laboratory')
        maker_spaces = facility_service.filter_by_type('Maker Space')
        
        # Assert
        assert len(laboratories) == 1
        assert laboratories[0].facility_type == 'Laboratory'
        assert len(maker_spaces) == 1
        assert maker_spaces[0].facility_type == 'Maker Space'
    
    def test_filter_by_partner(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test filtering facilities by partner.
        
        Arrange: Create facilities with different partners
        Act: Filter by specific partner
        Assert: Only matching facilities returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)  # UniPod
        facility_service.create_facility(another_facility_data)  # Lwera
        
        # Act
        unipod_facilities = facility_service.filter_by_partner('UniPod')
        lwera_facilities = facility_service.filter_by_partner('Lwera')
        
        # Assert
        assert len(unipod_facilities) == 1
        assert unipod_facilities[0].partner == 'UniPod'
        assert len(lwera_facilities) == 1
        assert lwera_facilities[0].partner == 'Lwera'
    
    def test_get_facility_statistics(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test getting facility statistics.
        
        Arrange: Create multiple facilities
        Act: Get statistics
        Assert: Correct count returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)
        facility_service.create_facility(another_facility_data)
        
        # Act
        stats = facility_service.get_facility_statistics()
        
        # Assert
        assert stats['total_facilities'] == 2


# ============================================================================
# EDGE CASES AND VALIDATION TESTS
# ============================================================================

@pytest.mark.unit
class TestFacilityEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_name_exactly_three_characters(self, facility_service):
        """
        Test facility name with exactly 3 characters (boundary condition).
        
        Arrange: Facility data with 3-character name
        Act: Create facility
        Assert: Creation succeeds
        """
        # Arrange
        boundary_facility = {
            'name': 'Lab',  # Exactly 3 characters - VALID!
            'location': 'Kampala, Uganda',
            'description': 'Testing boundary condition',
            'partner': 'UniPod',
            'facility_type': 'Laboratory',
            'capabilities': 'CNC'
        }
        
        # Act
        facility = facility_service.create_facility(boundary_facility)
        
        # Assert
        assert facility is not None
        assert facility.name == 'Lab'
    
    def test_case_insensitive_name_uniqueness(self, facility_service, valid_facility_data):
        """
        Test that name uniqueness check is case-insensitive.
        
        Arrange: Create facility with specific case
        Act: Try to create facility with different case but same name
        Assert: ValueError raised for duplicate name
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)  # 'Innovation Lab Kampala'
        
        # Act & Assert - Different case should still fail
        duplicate_facility = {
            'name': 'INNOVATION LAB KAMPALA',  # Same name, different case
            'location': 'Different Location',
            'partner': 'UIRI',
            'facility_type': 'Workshop',
            'capabilities': 'Materials Testing'
        }
        
        with pytest.raises(ValueError, match="already exists"):
            facility_service.create_facility(duplicate_facility)
    
    def test_update_facility_same_name_allowed(self, facility_service, valid_facility_data):
        """
        Test that updating facility with same name is allowed.
        
        Arrange: Create facility
        Act: Update facility with same name but different other fields
        Assert: Update succeeds
        """
        # Arrange
        facility = facility_service.create_facility(valid_facility_data)
        
        # Act
        updated_facility = facility_service.update_facility(facility.facility_id, {
            'name': 'Innovation Lab Kampala',  # Same name
            'description': 'Updated description'
        })
        
        # Assert
        assert updated_facility.name == 'Innovation Lab Kampala'
        assert updated_facility.description == 'Updated description'
    
    def test_search_with_empty_query(self, facility_service, valid_facility_data):
        """
        Test search behavior with empty parameters.
        
        Arrange: Create facility
        Act: Search with no parameters
        Assert: All facilities returned
        """
        # Arrange
        facility_service.create_facility(valid_facility_data)
        
        # Act
        results = facility_service.search_facilities()
        
        # Assert
        assert len(results) == 1
        assert results[0].name == 'Innovation Lab Kampala'


# ============================================================================
# INTEGRATION-STYLE TESTS (Still using mock, but testing workflows)
# ============================================================================

@pytest.mark.unit
class TestFacilityWorkflows:
    """Test complete facility management workflows."""
    
    def test_complete_facility_lifecycle(self, facility_service, valid_facility_data):
        """
        Test complete CRUD lifecycle for a facility.
        
        This tests the full workflow: Create → Read → Update → Delete
        """
        # 1. CREATE
        facility = facility_service.create_facility(valid_facility_data)
        assert facility.name == 'Innovation Lab Kampala'
        
        # 2. READ
        retrieved = facility_service.get_facility_by_id(facility.facility_id)
        assert retrieved.name == 'Innovation Lab Kampala'
        
        # 3. UPDATE
        updated = facility_service.update_facility(facility.facility_id, {
            'description': 'Updated facility description',
            'partner': 'UIRI'
        })
        assert updated.description == 'Updated facility description'
        assert updated.partner == 'UIRI'
        
        # 4. DELETE
        deleted = facility_service.delete_facility(facility.facility_id)
        assert deleted is True
        
        # 5. VERIFY DELETION
        not_found = facility_service.get_facility_by_id(facility.facility_id)
        assert not_found is None
    
    def test_facility_management_with_multiple_facilities(self, facility_service, valid_facility_data, another_facility_data):
        """
        Test managing multiple facilities simultaneously.
        
        Tests: Creating multiple, searching, filtering, statistics
        """
        # Create multiple facilities
        facility1 = facility_service.create_facility(valid_facility_data)
        facility2 = facility_service.create_facility(another_facility_data)
        
        # Test statistics
        stats = facility_service.get_facility_statistics()
        assert stats['total_facilities'] == 2
        
        # Test search
        innovation_labs = facility_service.search_facilities(name='Innovation')
        assert len(innovation_labs) == 1
        
        maker_spaces = facility_service.search_facilities(name='Maker')
        assert len(maker_spaces) == 1
        
        # Test filtering by type
        laboratories = facility_service.filter_by_type('Laboratory')
        assert len(laboratories) == 1
        
        # Test filtering by partner
        unipod_facilities = facility_service.filter_by_partner('UniPod')
        lwera_facilities = facility_service.filter_by_partner('Lwera')
        assert len(unipod_facilities) == 1
        assert len(lwera_facilities) == 1
        
        # Clean up
        facility_service.delete_facility(facility1.facility_id)
        facility_service.delete_facility(facility2.facility_id)
        
        # Verify cleanup
        final_stats = facility_service.get_facility_statistics()
        assert final_stats['total_facilities'] == 0
