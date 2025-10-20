"""
Unit Tests for ParticipantService - Business Rules and Operations

Uses MockParticipantRepository to avoid database dependency.

Business Rules Tested:
1. Full name must be at least 3 characters

Operations Tested:
- Create / Read / Update / Delete
- Assign / Remove project
- Filters and statistics
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
    def test_full_name_minimum_length(self, participant_service):
        invalid = {
            'full_name': 'Al',  # 2 chars
            'email': 'al@example.com',
            'specialization': 'CS',
            'institution': 'SCIT',
        }
        with pytest.raises(ValueError, match='at least 3 characters'):
            participant_service.create_participant(invalid)

    def test_create_participant_success(self, participant_service, valid_participant):
        p = participant_service.create_participant(valid_participant)
        assert p.full_name == 'Jane Doe'
        assert p.email == 'jane@example.com'


# ================================================================
# CRUD and Operations
# ================================================================

@pytest.mark.unit
class TestParticipantOperations:
    def test_get_all_and_by_id(self, participant_service, valid_participant, another_participant):
        p1 = participant_service.create_participant(valid_participant)
        p2 = participant_service.create_participant(another_participant)

        all_ps = participant_service.get_all_participants()
        assert len(all_ps) == 2

        found = participant_service.get_participant_by_id(p1.participant_id)
        assert found.full_name == 'Jane Doe'

    def test_update_participant(self, participant_service, valid_participant):
        p = participant_service.create_participant(valid_participant)
        updated = participant_service.update_participant(p.participant_id, {'full_name': 'Jane A. Doe'})
        assert updated.full_name == 'Jane A. Doe'

    def test_update_participant_not_found(self, participant_service):
        with pytest.raises(ValueError, match='not found'):
            participant_service.update_participant(999, {'full_name': 'X'})

    def test_delete_participant(self, participant_service, valid_participant):
        p = participant_service.create_participant(valid_participant)
        ok = participant_service.delete_participant(p.participant_id)
        assert ok is True
        assert participant_service.get_participant_by_id(p.participant_id) is None

    def test_delete_participant_not_found(self, participant_service):
        ok = participant_service.delete_participant(999)
        assert ok is False


# ================================================================
# Project Assignment & Filters
# ================================================================

@pytest.mark.unit
class TestParticipantAssignmentsAndFilters:
    def test_assign_and_remove_project(self, participant_service, valid_participant):
        p = participant_service.create_participant(valid_participant)
        # Reassign to new project
        ok_assign = participant_service.assign_to_project(p.participant_id, 303)
        assert ok_assign is True
        # Remove assignment
        ok_remove = participant_service.remove_from_project(p.participant_id)
        assert ok_remove is True

    def test_filters_and_statistics(self, participant_service, valid_participant, another_participant):
        participant_service.create_participant(valid_participant)
        participant_service.create_participant(another_participant)

        cs = participant_service.get_participants_by_project(101)
        assert len(cs) == 1

        cross = participant_service.get_cross_skill_trained_participants()
        assert len(cross) == 1

        scit = participant_service.repository.filter_by_institution('SCIT')
        assert len(scit) == 1

        stats = participant_service.get_participant_statistics()
        assert stats['total_participants'] == 2
        assert stats['cross_skill_trained_count'] == 1
