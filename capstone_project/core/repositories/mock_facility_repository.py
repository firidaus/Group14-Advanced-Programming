"""
Mock Facility Repository for testing without database.
Stores facilities in memory for unit tests.
"""
from typing import List, Optional
from core.models.Facility import Facility


class MockFacilityRepository:
    """In-memory facility repository for testing."""
    
    def __init__(self):
        """Initialize with empty facility list."""
        self.facilities: List[Facility] = []
        self._next_id = 1
    
    def get_all(self) -> List[Facility]:
        """Get all facilities."""
        return self.facilities.copy()
    
    def get_by_id(self, facility_id: int) -> Optional[Facility]:
        """Get facility by ID."""
        for facility in self.facilities:
            if facility.FacilityId == facility_id:
                return facility
        return None
    
    def create(self, facility_name: str, facility_type: str, location_city: str,
               location_district: str, capabilities: str, partner: str) -> Facility:
        """Create a new facility."""
        facility = Facility(
            FacilityId=self._next_id,
            facility_name=facility_name,
            facility_type=facility_type,
            location_city=location_city,
            location_district=location_district,
            capabilities=capabilities,
            partner=partner
        )
        self._next_id += 1
        self.facilities.append(facility)
        return facility
    
    def update(self, facility_id: int, facility_name: str, facility_type: str,
               location_city: str, location_district: str, capabilities: str,
               partner: str) -> Optional[Facility]:
        """Update an existing facility."""
        facility = self.get_by_id(facility_id)
        if facility:
            facility.facility_name = facility_name
            facility.facility_type = facility_type
            facility.location_city = location_city
            facility.location_district = location_district
            facility.capabilities = capabilities
            facility.partner = partner
        return facility
    
    def delete(self, facility_id: int) -> bool:
        """Delete a facility."""
        facility = self.get_by_id(facility_id)
        if facility:
            self.facilities.remove(facility)
            return True
        return False
    
    def exists_by_name(self, facility_name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if facility name exists."""
        for facility in self.facilities:
            if facility.facility_name == facility_name:
                if exclude_id is None or facility.FacilityId != exclude_id:
                    return True
        return False
    
    def filter_by_type(self, facility_type: str) -> List[Facility]:
        """Filter facilities by type."""
        return [f for f in self.facilities if f.facility_type == facility_type]
    
    def filter_by_partner(self, partner: str) -> List[Facility]:
        """Filter facilities by partner."""
        return [f for f in self.facilities if f.partner == partner]
    
    def search(self, query: str) -> List[Facility]:
        """Search facilities by name or capabilities."""
        query_lower = query.lower()
        return [
            f for f in self.facilities
            if query_lower in f.facility_name.lower() or query_lower in f.capabilities.lower()
        ]
    
    def count(self) -> int:
        """Count total facilities."""
        return len(self.facilities)
