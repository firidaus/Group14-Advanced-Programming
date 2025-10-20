"""
Service Repository

Handles all database operations for Service entity.
"""

from typing import List, Optional, Dict, Any
from core.models.service import Service


class ServiceRepository:
    """Data access layer for Service entity"""
    
    def get_all(self) -> List[Service]:
        """Get all services with related data"""
        return list(Service.objects.select_related('FacilityId').all())
    
    def get_by_id(self, service_id: int) -> Optional[Service]:
        """Get service by ID"""
        try:
            return Service.objects.select_related('FacilityId').get(pk=service_id)
        except Service.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Service:
        """Create new service"""
        return Service.objects.create(**data)
    
    def update(self, service: Service, data: Dict[str, Any]) -> Service:
        """Update existing service"""
        for key, value in data.items():
            setattr(service, key, value)
        service.save()
        return service
    
    def delete(self, service: Service) -> None:
        """Delete service"""
        service.delete()
    
    def filter_by_category(self, category: str) -> List[Service]:
        """Filter services by category"""
        return list(Service.objects.filter(category=category))
    
    def filter_by_skill_type(self, skill_type: str) -> List[Service]:
        """Filter services by skill type"""
        return list(Service.objects.filter(skill_type=skill_type))
    
    def filter_by_facility(self, facility_id: int) -> List[Service]:
        """Filter services by facility"""
        return list(Service.objects.filter(FacilityId_id=facility_id))
    
    def count(self) -> int:
        """Count total services"""
        return Service.objects.count()
