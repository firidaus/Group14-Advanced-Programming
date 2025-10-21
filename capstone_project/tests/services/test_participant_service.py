"""
Unit Tests for ParticipantService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses MockParticipantRepository to avoid database dependency.

Business Rules Tested:
1. Required Fields: FullName, Email, and Affiliation must be provided
2. Email Uniqueness: Email must be unique across all participants (case-insensitive)
3. Specialization Requirement: CrossSkillTrained requires Specialization to be defined

Test Pattern: AAA (Arrange-Act-Assert)
Focus: Business Rule Validation
"""

import pytest
from core.services.participant_service import ParticipantService
from core.repositories.mock_participant_repository import MockParticipantRepository


# ================================================================
# Fixtures
# ================================================================

@pytest.fixture
def participant_service():
    repo = MockParticipantRepository()
    return ParticipantService(repository=repo)


@pytest.fixture
def valid_participant():
    return {
        'full_name': 'Jane Doe',
        'email': 'jane@example.com',
        'affiliation': 'SCIT',
        'specialization': 'CS',
        'cross_skill_trained': True,
        'institution': 'SCIT',
        # In the mock repo we store project_id directly for simplicity
        'project_id': 101,
    }


@pytest.fixture
def another_participant():
    return {
        'full_name': 'John Smith',
        'email': 'john@example.com',
        'affiliation': 'CEDAT',
        'specialization': 'ENG',
        'cross_skill_trained': False,
        'institution': 'CEDAT',
        'project_id': 202,
    }


# ================================================================
# Business Rule Tests
# ================================================================

@pytest.mark.unit
class TestParticipantBusinessRules:
    """Test the 3 core business rules for Participant entity."""
    
    def test_required_fields(self, participant_service):
        """
        Business Rule #1: FullName, Email, and Affiliation are required fields.
        
        Error Message: "Participant.FullName, Participant.Email, and Participant.Affiliation are required"
        """
        # Test missing full_name
        invalid_data = {
            'email': 'test@example.com',
            'affiliation': 'Test Org'
        }
        with pytest.raises(ValueError, match="Participant.FullName, Participant.Email, and Participant.Affiliation are required"):
            participant_service.create_participant(invalid_data)

        # Test missing email
        invalid_data = {
            'full_name': 'Test User',
            'affiliation': 'Test Org'
        }
        with pytest.raises(ValueError, match="Participant.FullName, Participant.Email, and Participant.Affiliation are required"):
            participant_service.create_participant(invalid_data)

        # Test missing affiliation
        invalid_data = {
            'full_name': 'Test User',
            'email': 'test@example.com'
        }
        with pytest.raises(ValueError, match="Participant.FullName, Participant.Email, and Participant.Affiliation are required"):
            participant_service.create_participant(invalid_data)

    def test_email_uniqueness(self, participant_service, valid_participant):
        """
        Business Rule #2: Email must be unique (case-insensitive).
        
        Error Message: "Participant.Email already exists"
        """
        # Create first participant
        participant_service.create_participant(valid_participant)

        # Try to create another participant with same email (different case)
        duplicate_data = valid_participant.copy()
        duplicate_data['email'] = valid_participant['email'].upper()
        duplicate_data['full_name'] = 'Different Name'
        
        with pytest.raises(ValueError, match="Participant.Email already exists"):
            participant_service.create_participant(duplicate_data)

        # Should allow different email
        different_email = valid_participant.copy()
        different_email['email'] = 'different@example.com'
        participant_service.create_participant(different_email)  # Should not raise error

    def test_specialization_requirement(self, participant_service, valid_participant):
        """
        Business Rule #3: CrossSkillTrained requires Specialization.
        
        Error Message: "Cannot set CrossSkillTrained without Specialization"
        """
        # Try to create participant with cross_skill_trained but no specialization
        invalid_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'affiliation': 'Test Org',
            'cross_skill_trained': True  # Cannot be true without specialization
        }
        with pytest.raises(ValueError, match="Cannot set CrossSkillTrained without Specialization"):
            participant_service.create_participant(invalid_data)

        # Try to update participant to have cross_skill_trained but no specialization
        participant = participant_service.create_participant(valid_participant)
        with pytest.raises(ValueError, match="Cannot set CrossSkillTrained without Specialization"):
            participant_service.update_participant(
                participant.participant_id,
                {'specialization': None, 'cross_skill_trained': True}
            )

        # Should work when specialization is provided
        valid_update = {
            'specialization': 'New Specialization',
            'cross_skill_trained': True
        }
        updated = participant_service.update_participant(participant.participant_id, valid_update)
        assert updated.specialization == 'New Specialization'
        assert updated.cross_skill_trained is True



