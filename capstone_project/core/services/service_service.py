"""
Service Service

Contains all business logic for Service entity.
Uses dependency injection for testability.

Business Rules:
- Service name must not be empty
- Service must have a valid facility
- Category and skill type must be from allowed choices
"""

from typing import Dict, List, Optional, Any
from core.repositories.service_repository import ServiceRepository


class ServiceService:
    """Service class for Service business logic"""
    
    def __init__(self, repository=None):
        """Initialize service with repository"""
        self.repository = repository or ServiceRepository()
    
    def get_all_services(self) -> List[Any]:
        """Get all services"""
        return self.repository.get_all()
    
    def get_service_by_id(self, service_id: int) -> Optional[Any]:
        """Get service by ID"""
        return self.repository.get_by_id(service_id)
    
    def create_service(self, data: Dict[str, Any]):
        """
        Create new service with business validation.
        
        Business Rules:
        - Service name is required
        - Service name must be at least 3 characters
        
        Args:
            data: Service data dictionary
            
        Returns:
            Created Service object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Required fields
        facility_id = data.get('facility_id') or data.get('FacilityId')
        name = data.get('name')
        category = data.get('category')
        skill_type = data.get('skill_type')

        if not facility_id or not name or not category or not skill_type:
            raise ValueError("Service.Facilityld, Service.Name, Service.Category, and Service.SkillType are required")

        # Name length check (keep existing behaviour)
        if len(str(name)) < 3:
            raise ValueError("Service name must be at least 3 characters")

        # Scoped uniqueness: name must be unique within the same facility
        exists_fn = getattr(self.repository, 'exists_by_name_in_facility', None)
        if callable(exists_fn):
            if exists_fn(name, facility_id):
                raise ValueError("A service with this name already exists in this facility")

        return self.repository.create(data)
    
    def update_service(self, service_id: int, data: Dict[str, Any]):
        """Update service with business validation"""
        service = self.repository.get_by_id(service_id)
        if not service:
            raise ValueError(f"Service with ID {service_id} not found")
        
        return self.repository.update(service, data)
    
    def delete_service(self, service_id: int) -> bool:
        """Delete service"""
        service = self.repository.get_by_id(service_id)
        if not service:
            return False
        # Delete guard: check if any Project at the Facility references this service category
        # Repository may expose a helper `project_refs_category(facility_id, category)` for tests
        project_check = getattr(self.repository, 'project_refs_category', None)
        service_facility = getattr(service, 'facility_id', None) or getattr(service, 'FacilityId', None)
        service_category = getattr(service, 'category', None)
        if callable(project_check) and project_check(service_facility, service_category):
            raise ValueError("Service in use by Project testing requirements")

        self.repository.delete(service)
        return True
    
    def filter_services(self, category: str = None, skill_type: str = None, 
                       facility_id: int = None) -> List[Any]:
        """
        Filter services by criteria.
        
        Args:
            category: Filter by category
            skill_type: Filter by skill type
            facility_id: Filter by facility
            
        Returns:
            List of matching services
        """
        if category:
            return self.repository.filter_by_category(category)
        elif skill_type:
            return self.repository.filter_by_skill_type(skill_type)
        elif facility_id:
            return self.repository.filter_by_facility(facility_id)
        else:
            return self.repository.get_all()
    
    def filter_by_category(self, category: str) -> List[Any]:
        """Filter services by category"""
        return self.repository.filter_by_category(category)
    
    def filter_by_skill_type(self, skill_type: str) -> List[Any]:
        """Filter services by skill type"""
        return self.repository.filter_by_skill_type(skill_type)
    
    def filter_by_facility(self, facility_id: int) -> List[Any]:
        """Filter services by facility"""
        return self.repository.filter_by_facility(facility_id)
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get statistics about services"""
        return {
            'total_services': self.repository.count(),
        }
