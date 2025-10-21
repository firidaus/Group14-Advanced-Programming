"""
Equipment Service

Contains all business logic for Equipment entity.
Uses dependency injection for testability.

Business Rules (from Table 1.2):
1. Required Fields: FacilityId, Name, and InventoryCode must be provided
2. Uniqueness: InventoryCode must be unique across all Equipment
3. UsageDomain-SupportPhase Coherence: If UsageDomain is Electronics, 
   then SupportPhase must include Prototyping or Testing (cannot be Training only)
4. Delete Guard: Equipment cannot be deleted if referenced by an active Project
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
        
        Business Rules (from Table 1.2):
        1. Required Fields: FacilityId, Name, and InventoryCode must be provided
        2. Uniqueness: InventoryCode must be unique across all Equipment
        3. UsageDomain-SupportPhase Coherence: Electronics equipment must support 
           Prototyping or Testing
        
        Args:
            data: Equipment data dictionary
            
        Returns:
            Created Equipment object
            
        Raises:
            ValidationError: If business rules violated
        """
        # Business Rule #1: Required Fields - FacilityId, Name, and InventoryCode
        facility_id = data.get('facility_id')
        name = data.get('name', '').strip()
        inventory_code = data.get('inventory_code', '').strip()
        
        if not facility_id:
            raise ValidationError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        if not name:
            raise ValidationError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        if not inventory_code:
            raise ValidationError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        # Business Rule #2: Uniqueness - InventoryCode must be unique
        if self.repository.exists_by_inventory_code(inventory_code):
            raise ValidationError("Equipment.InventoryCode already exists.")
        
        # Business Rule #3: UsageDomain-SupportPhase Coherence
        # If UsageDomain is Electronics, SupportPhase must include Prototyping or Testing
        usage_domain = data.get('usage_domain', '').strip()
        support_phase = data.get('support_phase', '').strip()
        
        if usage_domain == 'Electronics':
            if support_phase not in ['Prototyping', 'Testing']:
                raise ValidationError("Electronics equipment must support Prototyping or Testing.")
        
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
        
        Business Rule #4 (Delete Guard):
        Equipment cannot be deleted if referenced by an active Project in the same Facility
        
        Args:
            equipment_id: ID of equipment to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValidationError: If equipment is referenced by active projects
        """
        equipment = self.repository.get_by_id(equipment_id)
        if not equipment:
            raise ValidationError(f"Equipment with ID {equipment_id} not found")
        
        # Business Rule #4: Delete Guard - Check if equipment is referenced by active projects
        if hasattr(self.repository, 'is_equipment_in_use') and self.repository.is_equipment_in_use(equipment_id):
            raise ValidationError("Equipment referenced by active Project.")
        
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
