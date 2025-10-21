
import pytest
from core.services.outcome_service import OutcomeService
from core.repositories.mock_outcome_repository import MockOutcomeRepository


@pytest.fixture
def mock_repository():
    repo = MockOutcomeRepository()
    yield repo
    repo.clear()


@pytest.fixture
def outcome_service(mock_repository):
    return OutcomeService(repository=mock_repository)


class TestOutcomeServiceCreate:
     #Test outcome creation
    def test_create_outcome_success(self, outcome_service):
        data = {
            'title': 'Research Publication',
            'outcome_type': 'Publication',
            'project_id': 1,
            'description': 'Published in top-tier journal',
        }
        
        outcome = outcome_service.create_outcome(data)
        
        assert outcome is not None
        assert outcome.title == 'Research Publication'
        assert outcome.outcome_type == 'Publication'
        assert outcome.OutcomeId is not None
    
    #short title is rejection
    def test_create_outcome_short_title_fails(self, outcome_service):
       
        data = {
            'title': 'AB',
            'outcome_type': 'Patent',
            'project_id': 1,
        }
        
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            outcome_service.create_outcome(data)
    
    #empty title rejection
    def test_create_outcome_empty_title_fails(self, outcome_service):
       
        data = {
            'title': '',
            'outcome_type': 'Patent',
            'project_id': 1,
        }
        
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            outcome_service.create_outcome(data)
    
    #creating outcome with all fields
    def test_create_outcome_with_all_fields(self, outcome_service):
        
        data = {
            'title': 'Complete Outcome',
            'outcome_type': 'Patent',
            'project_id': 1,
            'description': 'Full description',
            'impact_score': 85,
            'quality_certification': 'ISO 9001',
            'patents_filed': 3,
        }
        
        outcome = outcome_service.create_outcome(data)
        
        assert outcome.title == 'Complete Outcome'
        assert outcome.outcome_type == 'Patent'
        assert outcome.impact_score == 85
        assert outcome.quality_certification == 'ISO 9001'
        assert outcome.patents_filed == 3


 #outcome retrieval logic
class TestOutcomeServiceRead:
   
    
    #getting all outcomes when none exist
    def test_get_all_outcomes_empty(self, outcome_service):
        outcomes = outcome_service.get_all_outcomes()
        assert outcomes == []
    
    def test_get_all_outcomes(self, outcome_service):
        outcome_service.create_outcome({
            'title': 'Outcome 1',
            'outcome_type': 'Publication',
            'project_id': 1,
        })
        outcome_service.create_outcome({
            'title': 'Outcome 2',
            'outcome_type': 'Patent',
            'project_id': 2,
        })
        
        outcomes = outcome_service.get_all_outcomes()
        
        assert len(outcomes) == 2
        assert outcomes[0].title == 'Outcome 1'
        assert outcomes[1].title == 'Outcome 2'
    
    def test_get_outcome_by_id_success(self, outcome_service):
        created = outcome_service.create_outcome({
            'title': 'Test Outcome',
            'outcome_type': 'Publication',
            'project_id': 1,
        })
        
        outcome = outcome_service.get_outcome_by_id(created.OutcomeId)
        
        assert outcome is not None
        assert outcome.OutcomeId == created.OutcomeId
        assert outcome.title == 'Test Outcome'
    
    def test_get_outcome_by_id_not_found(self, outcome_service):
        outcome = outcome_service.get_outcome_by_id(999)
        assert outcome is None
    
    #Test filtering outcomes by project
    def test_get_outcomes_by_project(self, outcome_service):
        outcome_service.create_outcome({
            'title': 'Project 1 Outcome 1',
            'outcome_type': 'Publication',
            'project_id': 1,
        })
        outcome_service.create_outcome({
            'title': 'Project 1 Outcome 2',
            'outcome_type': 'Patent',
            'project_id': 1,
        })
        outcome_service.create_outcome({
            'title': 'Project 2 Outcome',
            'outcome_type': 'Publication',
            'project_id': 2,
        })
        
        project_1_outcomes = outcome_service.get_outcomes_by_project(1)
        
        assert len(project_1_outcomes) == 2
        assert all(o.project_id == 1 for o in project_1_outcomes)
    
    #Test filtering by project with no outcomes
    def test_get_outcomes_by_project_empty(self, outcome_service):
        outcomes = outcome_service.get_outcomes_by_project(999)
        assert outcomes == []


class TestOutcomeServiceUpdate:
    """Test outcome update logic"""
    
    def test_update_outcome_success(self, outcome_service):
        created = outcome_service.create_outcome({
            'title': 'Original Title',
            'outcome_type': 'Publication',
            'project_id': 1,
        })
        
        updated_data = {
            'title': 'Updated Title',
            'outcome_type': 'Patent',
        }
        
        updated = outcome_service.update_outcome(created.OutcomeId, updated_data)
        
        assert updated.title == 'Updated Title'
        assert updated.outcome_type == 'Patent'
    
    def test_update_outcome_not_found(self, outcome_service):
        with pytest.raises(ValueError, match="not found"):
            outcome_service.update_outcome(999, {'title': 'New Title'})
    
    def test_update_outcome_partial(self, outcome_service):
        created = outcome_service.create_outcome({
            'title': 'Original',
            'outcome_type': 'Publication',
            'project_id': 1,
            'impact_score': 75,
        })
        
        # Update only impact score
        updated = outcome_service.update_outcome(
            created.OutcomeId, 
            {'impact_score': 90}
        )
        
        assert updated.title == 'Original'
        assert updated.impact_score == 90


class TestOutcomeServiceDelete:
    """Test outcome deletion logic"""
    
    def test_delete_outcome_success(self, outcome_service):
        created = outcome_service.create_outcome({
            'title': 'To Delete',
            'outcome_type': 'Publication',
            'project_id': 1,
        })
        
        result = outcome_service.delete_outcome(created.OutcomeId)
        
        assert result is True
        assert outcome_service.get_outcome_by_id(created.OutcomeId) is None
    
    def test_delete_outcome_not_found(self, outcome_service):
        result = outcome_service.delete_outcome(999)
        assert result is False

