"""
Mock Facility Repository for testing without database.
Stores facilities in memory for unit tests.
"""

from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockFacilityRepository:
    """
    Mock repository for testing Facility services in isolation.
    Stores data in memory instead of database.
    """
    
    def __init__(self):
        """Initialize with empty in-memory storage."""
        self.facilities = []
        self._next_id = 1
    
    def get_all(self) -> List[Mock]:
        """Return all facilities from in-memory storage."""
        return self.facilities.copy()
    
    def get_by_id(self, facility_id: int) -> Optional[Mock]:
        """Find a facility by ID from in-memory storage."""
        for facility in self.facilities:
            if facility.facility_id == facility_id:
                return facility
        return None
    
    def create(self, data: Dict[str, Any]) -> Mock:
        """
        Create a new mock facility.
        
        Args:
            data: Facility fields dictionary
            
        Returns:
            Mock facility object
        """
        facility = Mock()
        facility.facility_id = self._next_id
        self._next_id += 1
        
        # Set all fields from data
        for key, value in data.items():
            setattr(facility, key, value)
        
        # Add save and delete methods (do nothing in mock)
        facility.save = Mock()
        facility.delete = Mock()
        
        self.facilities.append(facility)
        return facility
    
    def update(self, facility: Mock, data: Dict[str, Any]) -> Mock:
        """Update a mock facility."""
        for key, value in data.items():
            setattr(facility, key, value)
        return facility
    
    def delete(self, facility: Mock) -> None:
        """Delete a mock facility."""
        if facility in self.facilities:
            self.facilities.remove(facility)
    
    def filter_by_name(self, name: str) -> List[Mock]:
        """Filter facilities by name (case-insensitive)."""
        return [
            f for f in self.facilities 
            if hasattr(f, 'name') and name.lower() in f.name.lower()
        ]
    
    def filter_by_type(self, facility_type: str) -> List[Mock]:
        """Filter facilities by type."""
        return [
            f for f in self.facilities 
            if hasattr(f, 'facility_type') and f.facility_type == facility_type
        ]
    
    def filter_by_partner(self, partner: str) -> List[Mock]:
        """Filter facilities by partner."""
        return [
            f for f in self.facilities 
            if hasattr(f, 'partner') and f.partner == partner
        ]
    
    def filter_by_location(self, location: str) -> List[Mock]:
        """Filter facilities by location (case-insensitive)."""
        return [
            f for f in self.facilities 
            if hasattr(f, 'location') and location.lower() in f.location.lower()
        ]
    
    def exists_by_name(self, name: str) -> bool:
        """Check if a facility with given name exists (case-insensitive)."""
        return any(
            hasattr(f, 'name') and f.name.lower() == name.lower() 
            for f in self.facilities
        )
    
    def count(self) -> int:
        """Count total facilities."""
        return len(self.facilities)
    
    def clear(self):
        """Clear all data (useful between tests)."""
        self.facilities = []
        self._next_id = 1
