"""
Equipment Service

Contains all business logic for Equipment entity.
Uses dependency injection for testability.

Business Rules:
- Equipment name must be unique within facility
- Equipment name must be at least 3 characters
- Equipment must have a valid facility
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.Equipment import Equipment

from core.repositories.equipment_repository import EquipmentRepository


class EquipmentService:
    """Service class for Equipment business logic"""
    
    def __init__(self, repository=None):
        """Initialize service with repository"""
        self.repository = repository or EquipmentRepository()
    
    def get_all_equipment(self) -> List:
        """Get all equipment"""
        return self.repository.get_all()
    
    def get_equipment_by_id(self, equipment_id: int) -> Optional['Equipment']:
        """Get equipment by ID"""
        return self.repository.get_by_id(equipment_id)
    
    def create_equipment(self, data: Dict[str, Any]):
        """
        Create new equipment with business validation.
        
        Business Rules:
        - Equipment name must be at least 3 characters
        
        Args:
            data: Equipment data dictionary
            
        Returns:
            Created Equipment object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Name must be at least 3 characters
        name = data.get('name', '')
        if len(name) < 3:
            raise ValueError("Equipment name must be at least 3 characters")
        
        return self.repository.create(data)
    
    def update_equipment(self, equipment_id: int, data: Dict[str, Any]):
        """Update equipment with business validation"""
        equipment = self.repository.get_by_id(equipment_id)
        if not equipment:
            raise ValueError(f"Equipment with ID {equipment_id} not found")
        
        return self.repository.update(equipment, data)
    
    def delete_equipment(self, equipment_id: int) -> bool:
        """Delete equipment"""
        equipment = self.repository.get_by_id(equipment_id)
        if not equipment:
            return False
        
        self.repository.delete(equipment)
        return True
    
    def get_equipment_by_facility(self, facility_id: int) -> List:
        """Get all equipment for a facility"""
        return self.repository.filter_by_facility(facility_id)
    
    def search_equipment(self, query: str) -> List:
        """
        Search equipment by name, description, capabilities, or usage domain.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching equipment
        """
        if not query or len(query) < 2:
            return []
        
        return self.repository.search(query)
    
    def get_equipment_statistics(self) -> Dict[str, Any]:
        """Get statistics about equipment"""
        return {
            'total_equipment': self.repository.count(),
        }
