"""
Participant Service

Contains all business logic for Participant entity.
Uses dependency injection for testability.

Business Rules:
1. Required Fields: FullName, Email, and Affiliation must be provided
2. Email Uniqueness: Email must be unique across all participants (case-insensitive)
3. Specialization Requirement: CrossSkillTrained requires Specialization to be defined
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
    
    def get_participant_by_id(self, participant_id: int) -> Optional[Any]:
        """Get participant by ID"""
        return self.repository.get_by_id(participant_id)
    
    def create_participant(self, data: Dict[str, Any]):
        """
        Create new participant with business validation.
        
        Business Rules:
        1. Required Fields: FullName, Email, and Affiliation must be provided
        2. Email Uniqueness: Email must be unique across all participants (case-insensitive)
        3. Specialization Requirement: CrossSkillTrained requires Specialization
        
        Args:
            data: Participant data dictionary
            
        Returns:
            Created Participant object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule #1: Required Fields
        required_fields = ['full_name', 'email', 'affiliation']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValueError("Participant.FullName, Participant.Email, and Participant.Affiliation are required")

        # Business Rule #2: Email Uniqueness
        email = data['email']
        for participant in self.repository.get_all():
            if hasattr(participant, 'email') and participant.email.lower() == email.lower():
                raise ValueError("Participant.Email already exists")

        # Business Rule #3: Specialization Requirement
        if data.get('cross_skill_trained') and not data.get('specialization'):
            raise ValueError("Cannot set CrossSkillTrained without Specialization")
        
        return self.repository.create(data)
    
    def update_participant(self, participant_id: int, data: Dict[str, Any]):
        """
        Update participant with business validation.
        
        Business Rules:
        1. Required Fields cannot be cleared
        2. Email Uniqueness must be maintained
        3. Specialization Requirement must be maintained
        
        Args:
            participant_id: ID of participant to update
            data: Updated participant data
            
        Returns:
            Updated Participant object
            
        Raises:
            ValueError: If business rules violated or participant not found
        """
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            raise ValueError(f"Participant with ID {participant_id} not found")
        
        # Business Rule #1: Required Fields can't be cleared
        new_full_name = data.get('full_name', getattr(participant, 'full_name', None))
        new_email = data.get('email', getattr(participant, 'email', None))
        new_affiliation = data.get('affiliation', getattr(participant, 'affiliation', None))
        
        if not all([new_full_name, new_email, new_affiliation]):
            raise ValueError("Participant.FullName, Participant.Email, and Participant.Affiliation are required")
        
        # Business Rule #2: Email Uniqueness
        if new_email != getattr(participant, 'email', None):
            for p in self.repository.get_all():
                if p != participant and hasattr(p, 'email') and p.email.lower() == new_email.lower():
                    raise ValueError("Participant.Email already exists")
        
        # Business Rule #3: Specialization Requirement
        new_cross_skill = data.get('cross_skill_trained', getattr(participant, 'cross_skill_trained', False))
        new_specialization = data.get('specialization', getattr(participant, 'specialization', None))
        
        if new_cross_skill and not new_specialization:
            raise ValueError("Cannot set CrossSkillTrained without Specialization")
        
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
