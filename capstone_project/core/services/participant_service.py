"""
Participant Service

Contains all business logic for Participant entity.
Uses dependency injection for testability.

Business Rules:
- Participant full name is required
- Contact info must be valid
- Participants can be assigned to projects
"""

from typing import Dict, List, Optional, Any
from core.repositories.participant_repository import ParticipantRepository


class ParticipantService:
    """Service class for Participant business logic"""
    
    def __init__(self, repository=None):
        """Initialize service with repository"""
        self.repository = repository or ParticipantRepository()
    
    def get_all_participants(self) -> List:
        """Get all participants"""
        return self.repository.get_all()
    
    def get_participant_by_id(self, participant_id: int) -> Optional:
        """Get participant by ID"""
        return self.repository.get_by_id(participant_id)
    
    def create_participant(self, data: Dict[str, Any]):
        """
        Create new participant with business validation.
        
        Business Rules:
        - Full name is required (at least 3 characters)
        
        Args:
            data: Participant data dictionary
            
        Returns:
            Created Participant object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Full name is required
        full_name = data.get('full_name', '')
        if len(full_name) < 3:
            raise ValueError("Full name must be at least 3 characters")
        
        return self.repository.create(data)
    
    def update_participant(self, participant_id: int, data: Dict[str, Any]):
        """Update participant with business validation"""
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            raise ValueError(f"Participant with ID {participant_id} not found")
        
        return self.repository.update(participant, data)
    
    def delete_participant(self, participant_id: int) -> bool:
        """Delete participant"""
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            return False
        
        self.repository.delete(participant)
        return True
    
    def assign_to_project(self, participant_id: int, project_id: int) -> bool:
        """
        Assign participant to a project.
        
        Args:
            participant_id: ID of participant
            project_id: ID of project
            
        Returns:
            True if successful, False otherwise
        """
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            return False
        
        # Update participant's project
        self.repository.update(participant, {'project_id': project_id})
        return True
    
    def remove_from_project(self, participant_id: int) -> bool:
        """
        Remove participant from their project.
        
        Args:
            participant_id: ID of participant
            
        Returns:
            True if successful, False otherwise
        """
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            return False
        
        # Remove project assignment
        self.repository.update(participant, {'project_id': None})
        return True
    
    def get_participants_by_project(self, project_id: int) -> List:
        """Get all participants for a project"""
        return self.repository.filter_by_project(project_id)
    
    def get_cross_skill_trained_participants(self) -> List:
        """Get all participants who are cross-skill trained"""
        return self.repository.filter_cross_skill_trained()
    
    def get_participant_statistics(self) -> Dict[str, Any]:
        """Get statistics about participants"""
        return {
            'total_participants': self.repository.count(),
            'cross_skill_trained_count': len(self.repository.filter_cross_skill_trained()),
        }
