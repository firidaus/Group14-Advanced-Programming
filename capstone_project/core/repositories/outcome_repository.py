"""
Outcome Repository

Handles all database operations for Outcome entity.
"""

from typing import List, Optional, Dict, Any
from core.models.Outcome import Outcome


class OutcomeRepository:
    """Data access layer for Outcome entity"""
    
    def get_all(self) -> List[Outcome]:
        """Get all outcomes"""
        return list(Outcome.objects.all())
    
    def get_by_id(self, outcome_id: int) -> Optional[Outcome]:
        """Get outcome by ID"""
        try:
            return Outcome.objects.get(pk=outcome_id)
        except Outcome.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Outcome:
        """Create new outcome"""
        return Outcome.objects.create(**data)
    
    def update(self, outcome: Outcome, data: Dict[str, Any]) -> Outcome:
        """Update existing outcome"""
        for key, value in data.items():
            setattr(outcome, key, value)
        outcome.save()
        return outcome
    
    def delete(self, outcome: Outcome) -> None:
        """Delete outcome"""
        outcome.delete()
    
    def filter_by_project(self, project_id: int) -> List[Outcome]:
        """Filter outcomes by project"""
        return list(Outcome.objects.filter(project_id=project_id))
    
    def filter_by_outcome_type(self, outcome_type: str) -> List[Outcome]:
        """Filter outcomes by type"""
        return list(Outcome.objects.filter(outcome_type=outcome_type))
    
    def filter_by_certification(self, certification: str) -> List[Outcome]:
        """Filter outcomes by quality certification"""
        return list(Outcome.objects.filter(quality_certification=certification))
    
    def count(self) -> int:
        """Count total outcomes"""
        return Outcome.objects.count()
