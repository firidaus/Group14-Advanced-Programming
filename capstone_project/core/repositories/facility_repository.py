"""
Facility Repository

Handles all database operations for Facility entity.
"""

from typing import List, Optional, Dict, Any
from core.models.Facility import Facility


class FacilityRepository:
    """Data access layer for Facility entity"""
    
    def get_all(self) -> List[Facility]:
        """Get all facilities"""
        return list(Facility.objects.all())
    
    def get_by_id(self, facility_id: int) -> Optional[Facility]:
        """Get facility by ID"""
        try:
            return Facility.objects.get(pk=facility_id)
        except Facility.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Facility:
        """Create new facility"""
        return Facility.objects.create(**data)
    
    def update(self, facility: Facility, data: Dict[str, Any]) -> Facility:
        """Update existing facility"""
        for key, value in data.items():
            setattr(facility, key, value)
        facility.save()
        return facility
    
    def delete(self, facility: Facility) -> None:
        """Delete facility"""
        facility.delete()
    
    def filter_by_name(self, name: str) -> List[Facility]:
        """Filter facilities by name"""
        return list(Facility.objects.filter(name__icontains=name))
    
    def filter_by_type(self, facility_type: str) -> List[Facility]:
        """Filter facilities by facility type"""
        return list(Facility.objects.filter(facility_type=facility_type))
    
    def filter_by_partner(self, partner: str) -> List[Facility]:
        """Filter facilities by partner"""
        return list(Facility.objects.filter(partner=partner))
    
    def filter_by_location(self, location: str) -> List[Facility]:
        """Filter facilities by location"""
        return list(Facility.objects.filter(location__icontains=location))
    
    def exists_by_name(self, name: str) -> bool:
        """Check if facility name exists"""
        return Facility.objects.filter(name__iexact=name).exists()
    
    def count(self) -> int:
        """Count total facilities"""
        return Facility.objects.count()
