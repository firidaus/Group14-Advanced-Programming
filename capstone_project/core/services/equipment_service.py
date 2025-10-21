"""
Equipment Service

Contains all business logic for Equipment entity.
Uses dependency injection for testability.

Business Rules:
1. Equipment must have unique inventory codes within the system
2. Equipment must be linked to an existing facility
3. Equipment cannot be deleted if assigned to active projects
4. Equipment must have valid usage_domain and support_phase values
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from django.core.exceptions import ValidationError

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
        1. Equipment must have unique inventory codes within the system
        2. Equipment must be linked to an existing facility
        3. Equipment must have valid usage_domain and support_phase values
        
        Args:
            data: Equipment data dictionary
            
        Returns:
            Created Equipment object
            
        Raises:
            ValidationError: If business rules violated
        """
        # Business Rule 1: Unique inventory codes
        inventory_code = data.get('inventory_code')
        if inventory_code and self.repository.exists_by_inventory_code(inventory_code):
            raise ValidationError(f"Inventory code '{inventory_code}' already exists")
        
        # Business Rule 2: Equipment must be linked to a facility
        facility_id = data.get('facility_id')
        if not facility_id:
            raise ValidationError("Equipment must be linked to a facility")
        
        # Business Rule 4: Valid usage_domain and support_phase choices
        valid_domains = ['Research', 'Production', 'Prototyping', 'Testing']
        valid_phases = ['Design', 'Development', 'Production', 'Maintenance']
        
        usage_domain = data.get('usage_domain')
        if usage_domain and usage_domain not in valid_domains:
            raise ValidationError(f"Invalid usage_domain '{usage_domain}'. Must be one of: {valid_domains}")
        
        support_phase = data.get('support_phase')
        if support_phase and support_phase not in valid_phases:
            raise ValidationError(f"Invalid support_phase '{support_phase}'. Must be one of: {valid_phases}")
        
        return self.repository.create(data)
    
    def update_equipment(self, equipment_id: int, data: Dict[str, Any]):
        """Update equipment with business validation"""
        equipment = self.repository.get_by_id(equipment_id)
        if not equipment:
            raise ValueError(f"Equipment with ID {equipment_id} not found")
        
        return self.repository.update(equipment, data)
    
    def delete_equipment(self, equipment_id: int) -> bool:
        """
        Delete equipment with business validation.
        
        Business Rules:
        3. Equipment cannot be deleted if assigned to active projects
        
        Args:
            equipment_id: ID of equipment to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValidationError: If equipment is assigned to active projects
        """
        equipment = self.repository.get_by_id(equipment_id)
        if not equipment:
            return False
        
        # Business Rule 3: Check if equipment is assigned to active projects
        if hasattr(self.repository, 'is_equipment_in_use') and self.repository.is_equipment_in_use(equipment_id):
            raise ValidationError("Cannot delete equipment that is assigned to active projects")
        
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
