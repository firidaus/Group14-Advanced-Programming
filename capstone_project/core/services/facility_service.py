"""
Facility Service

Contains all business logic for Facility entity.
Uses dependency injection for testability.

Business Rules:
- Facility name must be unique
- Facility name must be at least 3 characters
- City and address are required
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
    
    def get_facility_by_id(self, facility_id: int) -> Optional:
        """Get facility by ID"""
        return self.repository.get_by_id(facility_id)
    
    def create_facility(self, data: Dict[str, Any]):
        """
        Create new facility with business validation.
        
        Business Rules:
        - Name must be unique
        - Name must be at least 3 characters
        - Location is required
        
        Args:
            data: Facility data dictionary
            
        Returns:
            Created Facility object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Name must be at least 3 characters
        name = data.get('name', '')
        if len(name) < 3:
            raise ValueError("Facility name must be at least 3 characters")
        
        # Business Rule: Name must be unique
        if self.repository.exists_by_name(name):
            raise ValueError(f"Facility '{name}' already exists")
        
        # Business Rule: Location is required
        if not data.get('location'):
            raise ValueError("Location is required")
        
        return self.repository.create(data)
    
    def update_facility(self, facility_id: int, data: Dict[str, Any]):
        """
        Update facility with business validation.
        
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
        
        # Business Rule: Check unique name (if changing)
        new_name = data.get('name')
        if new_name and new_name != facility.name:
            if self.repository.exists_by_name(new_name):
                raise ValueError(f"Facility '{new_name}' already exists")
        
        return self.repository.update(facility, data)
    
    def delete_facility(self, facility_id: int) -> bool:
        """Delete facility"""
        facility = self.repository.get_by_id(facility_id)
        if not facility:
            return False
        
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
