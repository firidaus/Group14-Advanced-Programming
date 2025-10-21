"""
Mock Equipment Repository for Testing

This mock repository simulates database operations for Equipment testing
without requiring a real database connection.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class MockEquipment:
    """Mock Equipment model for testing"""
    
    def __init__(self, **kwargs):
        self.equipment_id = kwargs.get('equipment_id')
        self.name = kwargs.get('name', '')
        self.capabilities = kwargs.get('capabilities', '')
        self.description = kwargs.get('description', '')
        self.inventory_code = kwargs.get('inventory_code', '')
        self.usage_domain = kwargs.get('usage_domain', '')
        self.support_phase = kwargs.get('support_phase', '')
        self.facility_id = kwargs.get('facility_id')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def __str__(self):
        return f"{self.name} ({self.inventory_code})"


class MockEquipmentRepository:
    """Mock repository for Equipment testing"""
    
    def __init__(self):
        self._equipment = {}
        self._next_id = 1
        self._equipment_in_use = set()  # Track equipment assigned to projects
        self._populate_test_data()
    
    def _populate_test_data(self):
        """Add sample test data"""
        test_equipment = [
            {
                'equipment_id': 1,
                'name': '3D Printer Pro',
                'capabilities': 'PLA, ABS, PETG printing',
                'description': 'High-precision 3D printer for prototyping',
                'inventory_code': 'EQ001',
                'usage_domain': 'Research',
                'support_phase': 'Production',
                'facility_id': 1
            },
            {
                'equipment_id': 2,
                'name': 'CNC Machine',
                'capabilities': 'Metal cutting, precision machining',
                'description': 'Computer numerical control machine',
                'inventory_code': 'EQ002',
                'usage_domain': 'Production',
                'support_phase': 'Production',
                'facility_id': 1
            },
            {
                'equipment_id': 3,
                'name': 'Oscilloscope Digital',
                'capabilities': 'Signal analysis, testing',
                'description': 'Digital oscilloscope for electronic testing',
                'inventory_code': 'EQ003',
                'usage_domain': 'Testing',
                'support_phase': 'Testing',
                'facility_id': 2
            }
        ]
        
        for data in test_equipment:
            equipment = MockEquipment(**data)
            self._equipment[data['equipment_id']] = equipment
            if data['equipment_id'] >= self._next_id:
                self._next_id = data['equipment_id'] + 1
    
    def get_all(self) -> List[MockEquipment]:
        """Get all equipment"""
        return list(self._equipment.values())
    
    def get_by_id(self, equipment_id: int) -> Optional[MockEquipment]:
        """Get equipment by ID"""
        return self._equipment.get(equipment_id)
    
    def create(self, data: Dict[str, Any]) -> MockEquipment:
        """Create new equipment"""
        equipment_data = data.copy()
        equipment_data['equipment_id'] = self._next_id
        equipment_data['created_at'] = datetime.now()
        equipment_data['updated_at'] = datetime.now()
        
        equipment = MockEquipment(**equipment_data)
        self._equipment[self._next_id] = equipment
        self._next_id += 1
        
        return equipment
    
    def update(self, equipment: MockEquipment, data: Dict[str, Any]) -> MockEquipment:
        """Update existing equipment"""
        for key, value in data.items():
            if hasattr(equipment, key):
                setattr(equipment, key, value)
        
        equipment.updated_at = datetime.now()
        return equipment
    
    def delete(self, equipment: MockEquipment) -> None:
        """Delete equipment"""
        equipment_id = equipment.equipment_id
        if equipment_id in self._equipment:
            del self._equipment[equipment_id]
    
    def filter_by_facility(self, facility_id: int) -> List[MockEquipment]:
        """Filter equipment by facility"""
        return [eq for eq in self._equipment.values() 
                if eq.facility_id == facility_id]
    
    def search(self, query: str) -> List[MockEquipment]:
        """Search equipment by name, description, capabilities, or usage domain"""
        if not query:
            return []
        
        query_lower = query.lower()
        results = []
        
        for equipment in self._equipment.values():
            if (query_lower in equipment.name.lower() or
                query_lower in equipment.description.lower() or
                query_lower in equipment.capabilities.lower() or
                query_lower in equipment.usage_domain.lower()):
                results.append(equipment)
        
        return results
    
    def count(self) -> int:
        """Count total equipment"""
        return len(self._equipment)
    
    def clear(self) -> None:
        """Clear all equipment (for testing)"""
        self._equipment.clear()
        self._next_id = 1
        self._equipment_in_use.clear()
    
    def exists_by_inventory_code(self, inventory_code: str) -> bool:
        """Check if equipment with given inventory code exists"""
        return any(eq.inventory_code == inventory_code for eq in self._equipment.values())
    
    def is_equipment_in_use(self, equipment_id: int) -> bool:
        """Check if equipment is assigned to active projects"""
        return equipment_id in self._equipment_in_use
    
    def set_equipment_in_use(self, equipment_id: int, in_use: bool = True) -> None:
        """Set equipment as in use by projects (for testing)"""
        if in_use:
            self._equipment_in_use.add(equipment_id)
        else:
            self._equipment_in_use.discard(equipment_id)
    
    def link_to_project(self, equipment_id: int, project_id: int, active: bool = True) -> None:
        """Link equipment to a project (for testing business rule #3)"""
        if active:
            self._equipment_in_use.add(equipment_id)