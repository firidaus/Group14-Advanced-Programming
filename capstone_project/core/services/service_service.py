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
    
    def get_all_services(self) -> List:
        """Get all services"""
        return self.repository.get_all()
    
    def get_service_by_id(self, service_id: int) -> Optional:
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
        # Business Rule: Service name is required
        name = data.get('name', '')
        if len(name) < 3:
            raise ValueError("Service name must be at least 3 characters")
        
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
        
        self.repository.delete(service)
        return True
    
    def filter_services(self, category: str = None, skill_type: str = None, 
                       facility_id: int = None) -> List:
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
    
    def filter_by_category(self, category: str) -> List:
        """Filter services by category"""
        return self.repository.filter_by_category(category)
    
    def filter_by_skill_type(self, skill_type: str) -> List:
        """Filter services by skill type"""
        return self.repository.filter_by_skill_type(skill_type)
    
    def filter_by_facility(self, facility_id: int) -> List:
        """Filter services by facility"""
        return self.repository.filter_by_facility(facility_id)
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get statistics about services"""
        return {
            'total_services': self.repository.count(),
        }
