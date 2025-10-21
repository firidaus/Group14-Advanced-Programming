from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockOutcomeRepository:
    
    def __init__(self):
        """Initialize with empty in-memory storage."""
        self.outcomes = []
        self._next_id = 1
    
    def get_all(self) -> List[Mock]:
        """Return all outcomes from in-memory storage."""
        return self.outcomes.copy()
    
    def get_by_id(self, outcome_id: int) -> Optional[Mock]:
        """Find an outcome by ID from in-memory storage."""
        for outcome in self.outcomes:
            if outcome.OutcomeId == outcome_id:
                return outcome
        return None
    
    def create(self, data: Dict[str, Any]) -> Mock:
        outcome = Mock()
        outcome.OutcomeId = self._next_id
        self._next_id += 1
        
        # Set all fields from data
        for key, value in data.items():
            setattr(outcome, key, value)
        
        # Add save method (does nothing in mock)
        outcome.save = Mock()
        outcome.delete = Mock()
        
        self.outcomes.append(outcome)
        return outcome
    
    def update(self, outcome: Mock, data: Dict[str, Any]) -> Mock:
        """Update a mock outcome."""
        for key, value in data.items():
            setattr(outcome, key, value)
        return outcome
    
    def delete(self, outcome: Mock) -> None:
        """Delete a mock outcome."""
        if outcome in self.outcomes:
            self.outcomes.remove(outcome)
    
    def filter_by_project(self, project_id: int) -> List[Mock]:
        """Filter outcomes by project."""
        return [
            o for o in self.outcomes 
            if hasattr(o, 'project_id') and o.project_id == project_id
        ]
    
    def filter_by_outcome_type(self, outcome_type: str) -> List[Mock]:
        """Filter outcomes by type."""
        return [
            o for o in self.outcomes 
            if hasattr(o, 'outcome_type') and o.outcome_type == outcome_type
        ]
    
    def filter_by_certification(self, certification: str) -> List[Mock]:
        return [
            o for o in self.outcomes 
            if hasattr(o, 'quality_certification') and o.quality_certification == certification
        ]
    
    def count(self) -> int:
        """Count total outcomes."""
        return len(self.outcomes)
    
    def clear(self):
        """Clear all data."""
        self.outcomes = []
        self._next_id = 1
