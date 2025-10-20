"""
Participant Repository

Handles all database operations for Participant entity.
"""

from typing import List, Optional, Dict, Any
from core.models.participant import Participant


class ParticipantRepository:
    """Data access layer for Participant entity"""
    
    def get_all(self) -> List[Participant]:
        """Get all participants"""
        return list(Participant.objects.all())
    
    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """Get participant by ID"""
        try:
            return Participant.objects.get(pk=participant_id)
        except Participant.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Participant:
        """Create new participant"""
        return Participant.objects.create(**data)
    
    def update(self, participant: Participant, data: Dict[str, Any]) -> Participant:
        """Update existing participant"""
        for key, value in data.items():
            setattr(participant, key, value)
        participant.save()
        return participant
    
    def delete(self, participant: Participant) -> None:
        """Delete participant"""
        participant.delete()
    
    def filter_by_specialization(self, specialization: str) -> List[Participant]:
        """Filter participants by specialization"""
        return list(Participant.objects.filter(specialization=specialization))
    
    def filter_by_institution(self, institution: str) -> List[Participant]:
        """Filter participants by institution"""
        return list(Participant.objects.filter(institution=institution))
    
    def filter_by_project(self, project_id: int) -> List[Participant]:
        """Filter participants by project"""
        return list(Participant.objects.filter(project_id=project_id))
    
    def filter_cross_skill_trained(self) -> List[Participant]:
        """Get participants who are cross-skill trained"""
        return list(Participant.objects.filter(cross_skill_trained=True))
    
    def count(self) -> int:
        """Count total participants"""
        return Participant.objects.count()
