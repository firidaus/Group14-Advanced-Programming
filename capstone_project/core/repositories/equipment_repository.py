"""
Equipment Repository

Handles all database operations for Equipment entity.
"""

from typing import List, Optional, Dict, Any
from django.db.models import Q
from core.models.Equipment import Equipment


class EquipmentRepository:
    """Data access layer for Equipment entity"""
    
    def get_all(self) -> List[Equipment]:
        """Get all equipment"""
        return list(Equipment.objects.all())
    
    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """Get equipment by ID"""
        try:
            return Equipment.objects.get(pk=equipment_id)
        except Equipment.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Equipment:
        """Create new equipment"""
        return Equipment.objects.create(**data)
    
    def update(self, equipment: Equipment, data: Dict[str, Any]) -> Equipment:
        """Update existing equipment"""
        for key, value in data.items():
            setattr(equipment, key, value)
        equipment.save()
        return equipment
    
    def delete(self, equipment: Equipment) -> None:
        """Delete equipment"""
        equipment.delete()
    
    def filter_by_facility(self, facility_id: int) -> List[Equipment]:
        """Filter equipment by facility"""
        return list(Equipment.objects.filter(facility_id=facility_id))
    
    def search(self, query: str) -> List[Equipment]:
        """Search equipment by name, description, capabilities, or usage domain"""
        if not query:
            return []
        
        return list(Equipment.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(capabilities__icontains=query) |
            Q(usage_domain__icontains=query)
        ))
    
    def count(self) -> int:
        """Count total equipment"""
        return Equipment.objects.count()
