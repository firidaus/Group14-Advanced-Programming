
import pytest
from datetime import date
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


class TestBusinessRule_RequiredAssociations:
    
    def test_create_project_with_program_and_facility_succeeds(self, project_service):
        """Test project creation with both Program and Facility IDs succeeds"""
        # Arrange
        data = {
            'title': 'Valid Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project = project_service.create_project(data)
        
        # Assert
        assert project is not None
        assert project.program_id == 1
        assert project.facility_id == 1
    
    def test_create_project_missing_program_id_fails(self, project_service):
        """Test project without ProgramId is rejected"""
        # Arrange
        data = {
            'title': 'Test Project',
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project.ProgramId and Project.FacilityId are required"):
            project_service.create_project(data)
    
    def test_create_project_missing_facility_id_fails(self, project_service):
        """Test project without FacilityId is rejected"""
        # Arrange
        data = {
            'title': 'Test Project',
            'program_id': 1,
            'team_members': ['Benjamin Nakabaale'],
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project.ProgramId and Project.FacilityId are required"):
            project_service.create_project(data)
    
    def test_create_project_missing_both_ids_fails(self, project_service):
        """Test project without ProgramId and FacilityId is rejected"""
        # Arrange
        data = {
            'title': 'Test Project',
            'team_members': ['Benjamin Nakabaale'],
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project.ProgramId and Project.FacilityId are required"):
            project_service.create_project(data)

class TestBusinessRule_TeamTracking:
    """Each Project must have at least one Team member assigned"""
    
    def test_create_project_with_team_members_succeeds(self, project_service):
        """Test project with team members succeeds"""
        # Arrange
        data = {
            'title': 'Team Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale', 'Ruth Angel'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project = project_service.create_project(data)
        
        # Assert
        assert project is not None
        assert len(project.team_members) >= 1
    
    def test_create_project_no_team_members_fails(self, project_service):
        """Test project with empty team members list is rejected"""
        # Arrange
        data = {
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': [],
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project must have at least one team member assigned"):
            project_service.create_project(data)
    
    def test_create_project_missing_team_members_field_fails(self, project_service):
        """Test project without team_members field is rejected"""
        # Arrange
        data = {
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project must have at least one team member assigned"):
            project_service.create_project(data)

class TestBusinessRule_OutcomeValidation:
    """If Status is 'Completed', at least one Outcome must be attached"""
    
    def test_update_project_to_completed_with_outcomes_succeeds(self, project_service):
        """Test marking project as completed with outcomes succeeds"""
        # Arrange
        created = project_service.create_project({
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'status': 'Active',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        
        # Act
        updated = project_service.update_project(
            created.ProjectId,
            {
                'status': 'Completed',
                'outcomes': ['Research Paper Published', 'Patent Filed']
            }
        )
        
        # Assert
        assert updated.status == 'Completed'
        assert len(updated.outcomes) >= 1
    
    def test_update_project_to_completed_without_outcomes_fails(self, project_service):
        """Test marking project as completed without outcomes is rejected"""
        # Arrange
        created = project_service.create_project({
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'status': 'Active',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        
        # Act & Assert
        with pytest.raises(ValueError, match="Completed projects must have at least one documented outcome"):
            project_service.update_project(
                created.ProjectId,
                {'status': 'Completed', 'outcomes': []}
            )

class TestBusinessRule4_NameUniqueness:
    """Project Name must be unique within a Program"""
    
    def test_create_project_unique_name_in_program_succeeds(self, project_service):
        """Test creating project with unique name in program succeeds"""
        # Arrange
        data = {
            'title': 'Unique Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project = project_service.create_project(data)
        
        # Assert
        assert project is not None
    
    def test_create_project_duplicate_name_same_program_fails(self, project_service):
        """Test creating project with duplicate name in same program is rejected"""
        # Arrange
        data = {
            'title': 'Unique Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        project_service.create_project(data)
        
        # Act & Assert
        with pytest.raises(ValueError, match="A project with this name already exists in this program"):
            project_service.create_project(data)
    
    def test_create_project_same_name_different_program_succeeds(self, project_service):
        """Test creating project with same name in different program succeeds"""
        # Arrange
        data1 = {
            'title': 'Common Project Name',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        data2 = {
            'title': 'Common Project Name',
            'program_id': 2,
            'facility_id': 1,
            'team_members': ['Ruth Angel'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project1 = project_service.create_project(data1)
        project2 = project_service.create_project(data2)
        
        # Assert
        assert project1.title == project2.title
        assert project1.program_id != project2.program_id
    
    def test_update_project_duplicate_name_same_program_fails(self, project_service):
        """Test updating project to duplicate name in same program is rejected"""
        # Arrange
        project_service.create_project({
            'title': 'Existing Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        
        created2 = project_service.create_project({
            'title': 'Another Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Ruth Angel'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        
        # Act & Assert
        with pytest.raises(ValueError, match="A project with this name already exists in this program"):
            project_service.update_project(
                created2.ProjectId, 
                {'title': 'Existing Project'}
            )


class TestBusinessRule5_FacilityCompatibility:
    """Project's technical requirements must be compatible with facility capabilities"""
    
    def test_create_project_compatible_facility_succeeds(self, project_service):
        """Test project with compatible facility requirements succeeds"""
        # Arrange
        data = {
            'title': 'Lab Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'technical_requirements': ['High-Performance Computing', 'Clean Room'],
            'facility_capabilities': ['High-Performance Computing', 'Clean Room', 'Lab Equipment'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project = project_service.create_project(data)
        
        # Assert
        assert project is not None
    
    def test_create_project_incompatible_facility_fails(self, project_service):
        """Test project with incompatible facility requirements is rejected"""
        # Arrange
        data = {
            'title': 'Lab Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'technical_requirements': ['High-Performance Computing', 'Clean Room'],
            'facility_capabilities': ['Basic Computing'], 
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project requirements not compatible with facility capabilities"):
            project_service.create_project(data)
    
    def test_create_project_no_technical_requirements_succeeds(self, project_service):
        """Test project without technical requirements succeeds"""
        # Arrange
        data = {
            'title': 'Simple Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        }
        
        # Act
        project = project_service.create_project(data)
        
        # Assert
        assert project is not None
    
    def test_update_project_incompatible_facility_fails(self, project_service):
        """Test updating project with incompatible facility is rejected"""
        # Arrange
        created = project_service.create_project({
            'title': 'Test Project',
            'program_id': 1,
            'facility_id': 1,
            'team_members': ['Benjamin Nakabaale'],
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        
        # Act & Assert
        with pytest.raises(ValueError, match="Project requirements not compatible with facility capabilities"):
            project_service.update_project(
                created.ProjectId,
                {
                    'technical_requirements': ['Advanced Lab', 'Clean Room'],
                    'facility_capabilities': ['Basic Lab']  # Missing required capabilities
                }
            )


