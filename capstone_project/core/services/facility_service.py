"""
Facility Service

Contains all business logic for Facility entity.
Uses dependency injection for testability.

Business Rules:
: Facility has dependent records (Services/Equipment/Projects)
FAILED tests/services/test_facility_service.py::TestFacilityEdgeCases::test_case_insensitive_name_uniqueness - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/services/test_facility_service.py::TestFacilityWorkflows::test_complete_facility_lifecycle - ValueError: Facility has dependent records (Services/Equipment/Projects)
FAILED tests/services/test_facility_service.py::TestFacilityWorkflows::test_facility_management_with_multiple_facilities - ValueError: Facility has dependent records (Services/Equipment/Projects)
ERROR tests/services/test_facility_service.py::TestFacilityBusinessRules::test_deletion_constraints - ValueError: A facility with this name already exists at this location
========================== 5 failed, 17 passed, 1 error in 0.96s ==================1. Required Fields: Name, Location, and FacilityType are required
2. Name-Location Uniqueness: Combination must be unique
3. Deletion Constraints: Cannot delete if linked to Services/Equipment/Projects
4. Capabilities: Required when Services/Equipment exist
"""

from typing import Dict, List, Optional, Any
from core.repositories.facility_repository import FacilityRepository


class FacilityService:
    """Service class for Facility business logic"""
    
    def __init__(self, repository=None):
        """
        Initialize service with repository.
        
        Args:
            repository: Repository instance (defaults to FacilityRepository)
        """
        self.repository = repository or FacilityRepository()
    
    def get_all_facilities(self) -> List:
        """Get all facilities"""
        return self.repository.get_all()
    
    def get_facility_by_id(self, facility_id: int) -> Optional[Any]:
        """Get facility by ID"""
        return self.repository.get_by_id(facility_id)
    
    def create_facility(self, data: Dict[str, Any]):
        """
        Create new facility with business validation.
        
        Business Rules:
        1. Required Fields: Name, Location, and FacilityType are required
        2. Name-Location Uniqueness: Combination must be unique
        
        Args:
            data: Facility data dictionary
            
        Returns:
            Created Facility object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Required Fields
        required_fields = ['name', 'location', 'facility_type']
        for field in required_fields:
            if not data.get(field):
                raise ValueError("Facility.Name, Facility.Location, and Facility.FacilityType are required")
                
        # Business Rule: Name-Location Uniqueness
        name = data['name']
        location = data['location']
        if any(f for f in self.repository.get_all() 
               if getattr(f, 'name', '').lower() == name.lower() 
               and getattr(f, 'location', '').lower() == location.lower()):
            raise ValueError("A facility with this name already exists at this location")
        
        return self.repository.create(data)
    
    def update_facility(self, facility_id: int, data: Dict[str, Any]):
        """
        Update facility with business validation.
        
        Business Rules:
        1. Required Fields: Name, Location, and FacilityType cannot be cleared
        2. Name-Location Uniqueness: Combination must remain unique
        3. Capabilities: Required when Services/Equipment exist
        
        Args:
            facility_id: ID of facility to update
            data: Updated facility data
            
        Returns:
            Updated Facility object
            
        Raises:
            ValueError: If business rules violated or facility not found
        """
        facility = self.repository.get_by_id(facility_id)
        if not facility:
            raise ValueError(f"Facility with ID {facility_id} not found")
        
        # Check required fields aren't being cleared
        new_name = data.get('name', getattr(facility, 'name', None))
        new_location = data.get('location', getattr(facility, 'location', None))
        new_type = data.get('facility_type', getattr(facility, 'facility_type', None))
        
        if not all([new_name, new_location, new_type]):
            raise ValueError("Facility.Name, Facility.Location, and Facility.FacilityType are required")
        
        # Check name-location uniqueness
        if (new_name != getattr(facility, 'name', None) or 
            new_location != getattr(facility, 'location', None)):
            if any(f for f in self.repository.get_all() 
                   if f != facility 
                   and getattr(f, 'name', '').lower() == new_name.lower() 
                   and getattr(f, 'location', '').lower() == new_location.lower()):
                raise ValueError("A facility with this name already exists at this location")
        
        # Check capabilities requirement
        has_services = bool(getattr(facility, 'services', []))
        has_equipment = bool(getattr(facility, 'equipment', []))
        new_capabilities = data.get('capabilities', getattr(facility, 'capabilities', []))
        
        if (has_services or has_equipment) and not new_capabilities:
            raise ValueError("Facility.Capabilities must be populated when Services/Equipment exist")
        
        return self.repository.update(facility, data)
    
    def delete_facility(self, facility_id: int) -> bool:
        """
        Delete facility if no dependent records exist.
        
        Business Rule: Cannot delete if facility has services, equipment, or projects.
        
        Args:
            facility_id: ID of facility to delete
            
        Returns:
            bool indicating success
            
        Raises:
            ValueError: If deletion constraints are violated
        """
        facility = self.repository.get_by_id(facility_id)
        if not facility:
            return False
        
        # Check for dependent records
        has_services = bool(getattr(facility, 'services', []))
        has_equipment = bool(getattr(facility, 'equipment', []))
        has_projects = bool(getattr(facility, 'projects', []))
        
        if has_services or has_equipment or has_projects:
            raise ValueError("Facility has dependent records (Services/Equipment/Projects)")
        
        self.repository.delete(facility)
        return True
    
    def search_facilities(self, name: str = None, facility_type: str = None, location: str = None) -> List:
        """
        Search facilities by multiple criteria.
        
        Args:
            name: Filter by name (partial match)
            facility_type: Filter by facility type
            location: Filter by location
            
        Returns:
            List of matching facilities
        """
        if name:
            return self.repository.filter_by_name(name)
        elif facility_type:
            return self.repository.filter_by_type(facility_type)
        elif location:
            return self.repository.filter_by_location(location)
        else:
            return self.repository.get_all()
    
    def filter_by_type(self, facility_type: str) -> List:
        """Filter facilities by type"""
        return self.repository.filter_by_type(facility_type)
    
    def filter_by_partner(self, partner: str) -> List:
        """Filter facilities by partner"""
        return self.repository.filter_by_partner(partner)
    
    def get_facility_statistics(self) -> Dict[str, Any]:
        """Get statistics about facilities"""
        return {
            'total_facilities': self.repository.count(),
        }
