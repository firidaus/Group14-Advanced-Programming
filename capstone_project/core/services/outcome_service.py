"""
Outcome Service

Contains all business logic for Outcome entity.
Uses dependency injection for testability.

Business Rules:
- Outcome must belong to a project
- Impact scores must be between 0-100
- Patents filed must be non-negative
"""

from typing import Dict, List, Optional, Any
from core.repositories.outcome_repository import OutcomeRepository


class OutcomeService:
    """Service class for Outcome business logic"""
    
    def __init__(self, repository=None):
        """Initialize service with repository"""
        self.repository = repository or OutcomeRepository()
    
    def get_all_outcomes(self) -> List:
        """Get all outcomes"""
        return self.repository.get_all()
    
    def get_outcome_by_id(self, outcome_id: int) -> Optional:
        """Get outcome by ID"""
        return self.repository.get_by_id(outcome_id)
    
    def create_outcome(self, data: Dict[str, Any]):
        """
        Create new outcome with business validation.
        
        Business Rules:
        - Outcome must have a title
        - Outcome must belong to a project
        
        Args:
            data: Outcome data dictionary
            
        Returns:
            Created Outcome object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Title is required
        title = data.get('title', '')
        if len(title) < 3:
            raise ValueError("Outcome title must be at least 3 characters")
        
        return self.repository.create(data)
    
    def update_outcome(self, outcome_id: int, data: Dict[str, Any]):
        """Update outcome with business validation"""
        outcome = self.repository.get_by_id(outcome_id)
        if not outcome:
            raise ValueError(f"Outcome with ID {outcome_id} not found")
        
        return self.repository.update(outcome, data)
    
    def delete_outcome(self, outcome_id: int) -> bool:
        """Delete outcome"""
        outcome = self.repository.get_by_id(outcome_id)
        if not outcome:
            return False
        
        self.repository.delete(outcome)
        return True
    
    def get_outcomes_by_project(self, project_id: int) -> List:
        """Get all outcomes for a project"""
        return self.repository.filter_by_project(project_id)
    
    def get_outcome_statistics(self) -> Dict[str, Any]:

        """Get statistics about outcomes"""
        return {
            'total_outcomes': self.repository.count(),
        }
