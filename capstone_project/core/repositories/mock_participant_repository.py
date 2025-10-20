"""
Mock Participant Repository

Used for unit testing business logic without database dependency.
Simulates database operations in memory.
"""

from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockParticipantRepository:
    """
    Mock repository for testing Participant services in isolation.
    Stores data in memory instead of database.
    """

    def __init__(self):
        """Initialize with empty in-memory storage."""
        self.participants: List[Mock] = []
        self._next_id = 1

    # -----------------------------
    # Basic CRUD
    # -----------------------------
    def get_all(self) -> List[Mock]:
        """Return all participants from in-memory storage."""
        return self.participants.copy()

    def get_by_id(self, participant_id: int) -> Optional[Mock]:
        """Find a participant by ID from in-memory storage."""
        for p in self.participants:
            if getattr(p, 'participant_id', None) == participant_id:
                return p
        return None

    def create(self, data: Dict[str, Any]) -> Mock:
        """
        Create a new mock participant.
        """
        participant = Mock()
        participant.participant_id = self._next_id
        self._next_id += 1

        # Set all fields from data
        for key, value in data.items():
            setattr(participant, key, value)

        # Provide typical model-like helpers
        participant.save = Mock()
        participant.delete = Mock()

        self.participants.append(participant)
        return participant

    def update(self, participant: Mock, data: Dict[str, Any]) -> Mock:
        """Update a mock participant."""
        for key, value in data.items():
            setattr(participant, key, value)
        return participant

    def delete(self, participant: Mock) -> None:
        """Delete a mock participant."""
        if participant in self.participants:
            self.participants.remove(participant)

    # -----------------------------
    # Filters & Queries
    # -----------------------------
    def filter_by_project(self, project_id: int) -> List[Mock]:
        """Get participants assigned to a given project id."""
        return [p for p in self.participants if getattr(p, 'project_id', None) == project_id]

    def filter_cross_skill_trained(self) -> List[Mock]:
        """Get participants who are cross-skill trained."""
        return [p for p in self.participants if getattr(p, 'cross_skill_trained', False)]

    def filter_by_specialization(self, specialization: str) -> List[Mock]:
        """Filter by specialization (exact match)."""
        return [p for p in self.participants if getattr(p, 'specialization', None) == specialization]

    def filter_by_institution(self, institution: str) -> List[Mock]:
        """Filter by institution (exact match)."""
        return [p for p in self.participants if getattr(p, 'institution', None) == institution]

    def count(self) -> int:
        """Count total participants."""
        return len(self.participants)

    def clear(self):
        """Clear storage (for test isolation if needed)."""
        self.participants = []
        self._next_id = 1
