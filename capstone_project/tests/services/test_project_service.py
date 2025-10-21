
import pytest
from datetime import date, timedelta
from core.services.project_service import ProjectService
from core.repositories.mock_project_repository import MockProjectRepository


@pytest.fixture
def mock_repository():
    repo = MockProjectRepository()
    yield repo
    repo.clear()


@pytest.fixture
def project_service(mock_repository):
    return ProjectService(repository=mock_repository)

#Test project creation logic
class TestProjectServiceCreate:
    
    def test_create_project_success(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        data = {
            'title': 'Research Project',
            'description': 'A research project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        }
        
        project = project_service.create_project(data)
        
        assert project is not None
        assert project.title == 'Research Project'
        assert project.program_id == 1
        assert project.facility_id == 1
        assert project.ProjectId is not None
    
    def test_create_project_short_title_fails(self, project_service):
        data = {
            'title': 'AB',
            'program_id': 1,
            'facility_id': 1,
        }
        
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            project_service.create_project(data)
    
    def test_create_project_empty_title_fails(self, project_service):
        data = {
            'title': '',
            'program_id': 1,
            'facility_id': 1,
        }
        
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            project_service.create_project(data)
    
    def test_create_project_duplicate_title_fails(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        data = {
            'title': 'Unique Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        }
        
        project_service.create_project(data)
        
        with pytest.raises(ValueError, match="already exists"):
            project_service.create_project(data)
    
    def test_create_project_invalid_dates_fails(self, project_service):
        """Test that end date before start date is rejected"""
        today = date.today()
        past = today - timedelta(days=30)
        
        data = {
            'title': 'Invalid Date Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': past,
        }
        
        with pytest.raises(ValueError, match="End date must be after start date"):
            project_service.create_project(data)
    
    def test_create_project_same_start_end_date_fails(self, project_service):
        today = date.today()
        
        data = {
            'title': 'Same Date Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': today,
        }
        
        with pytest.raises(ValueError, match="End date must be after start date"):
            project_service.create_project(data)
    
    def test_create_project_with_all_fields(self, project_service):
        today = date.today()
        future = today + timedelta(days=90)
        
        data = {
            'title': 'Complete Project',
            'description': 'Full description',
            'program_id': 1,
            'facility_id': 2,
            'start_date': today,
            'end_date': future,
            'budget': 100000,
            'status': 'Active',
        }
        
        project = project_service.create_project(data)
        
        assert project.title == 'Complete Project'
        assert project.description == 'Full description'
        assert project.budget == 100000
        assert project.status == 'Active'

#Test project retrieval logic
class TestProjectServiceRead:
    
    def test_get_all_projects_empty(self, project_service):
        """Test getting all projects when none exist"""
        projects = project_service.get_all_projects()
        assert projects == []
    
    def test_get_all_projects(self, project_service):
        """Test getting all projects"""
        today = date.today()
        future = today + timedelta(days=30)
        
        # Create test projects
        project_service.create_project({
            'title': 'Project 1',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Project 2',
            'program_id': 2,
            'facility_id': 2,
            'start_date': today,
            'end_date': future,
        })
        
        projects = project_service.get_all_projects()
        
        assert len(projects) == 2
        assert projects[0].title == 'Project 1'
        assert projects[1].title == 'Project 2'
    
    def test_get_project_by_id_success(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        created = project_service.create_project({
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        project = project_service.get_project_by_id(created.ProjectId)
        
        assert project is not None
        assert project.ProjectId == created.ProjectId
        assert project.title == 'Test Project'
    
    def test_get_project_by_id_not_found(self, project_service):
        project = project_service.get_project_by_id(999)
        assert project is None
    
    def test_get_projects_by_program(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        project_service.create_project({
            'title': 'Program 1 Project 1',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Program 1 Project 2',
            'program_id': 1,
            'facility_id': 2,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Program 2 Project',
            'program_id': 2,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        program_1_projects = project_service.get_projects_by_program(1)
        
        assert len(program_1_projects) == 2
        assert all(p.program_id == 1 for p in program_1_projects)
    
    def test_get_projects_by_program_empty(self, project_service):
        projects = project_service.get_projects_by_program(999)
        assert projects == []
    
    def test_get_projects_by_facility(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        project_service.create_project({
            'title': 'Facility 1 Project 1',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Facility 1 Project 2',
            'program_id': 2,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Facility 2 Project',
            'program_id': 1,
            'facility_id': 2,
            'start_date': today,
            'end_date': future,
        })
        
        facility_1_projects = project_service.get_projects_by_facility(1)
        
        assert len(facility_1_projects) == 2
        assert all(p.facility_id == 1 for p in facility_1_projects)
    
    def test_get_projects_by_facility_empty(self, project_service):
        """Test filtering by facility with no projects"""
        projects = project_service.get_projects_by_facility(999)
        assert projects == []

#Test project update logic
class TestProjectServiceUpdate:

    def test_update_project_success(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        created = project_service.create_project({
            'title': 'Original Title',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
        }
        
        updated = project_service.update_project(created.ProjectId, updated_data)
        
        assert updated.title == 'Updated Title'
        assert updated.description == 'Updated description'
    
    def test_update_project_not_found(self, project_service):
        with pytest.raises(ValueError, match="not found"):
            project_service.update_project(999, {'title': 'New Title'})
    
    def test_update_project_duplicate_title_fails(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        project_service.create_project({
            'title': 'Existing Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        created2 = project_service.create_project({
            'title': 'Another Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        #update to existing title
        with pytest.raises(ValueError, match="already exists"):
            project_service.update_project(
                created2.ProjectId, 
                {'title': 'Existing Project'}
            )
    
    def test_update_project_invalid_dates_fails(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        created = project_service.create_project({
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        # Try to set end date before start date
        past = today - timedelta(days=10)
        with pytest.raises(ValueError, match="End date must be after start date"):
            project_service.update_project(
                created.ProjectId,
                {'end_date': past}
            )
    
    def test_update_project_partial(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        created = project_service.create_project({
            'title': 'Original',
            'description': 'Original description',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        updated = project_service.update_project(
            created.ProjectId, 
            {'description': 'New description'}
        )
        
        assert updated.title == 'Original'
        assert updated.description == 'New description'


class TestProjectServiceDelete:

    def test_delete_project_success(self, project_service):
        today = date.today()
        future = today + timedelta(days=30)
        
        created = project_service.create_project({
            'title': 'To Delete',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        
        result = project_service.delete_project(created.ProjectId)
        
        assert result is True
        assert project_service.get_project_by_id(created.ProjectId) is None
    
    def test_delete_project_not_found(self, project_service):
        result = project_service.delete_project(999)
        assert result is False


class TestProjectServiceStatistics:
    
    def test_get_statistics_empty(self, project_service):
        """Test statistics with no projects"""
        stats = project_service.get_project_statistics()
        
        assert stats['total_projects'] == 0
    
    def test_get_statistics(self, project_service):
        """Test statistics with projects"""
        today = date.today()
        future = today + timedelta(days=30)
        
        project_service.create_project({
            'title': 'Project 1',
            'program_id': 1,
            'facility_id': 1,
            'start_date': today,
            'end_date': future,
        })
        project_service.create_project({
            'title': 'Project 2',
            'program_id': 2,
            'facility_id': 2,
            'start_date': today,
            'end_date': future,
        })
        
        stats = project_service.get_project_statistics()
        
        assert stats['total_projects'] == 2
