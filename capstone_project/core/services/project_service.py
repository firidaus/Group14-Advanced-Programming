"""
Project Service

Contains all business logic for Project entity.
Uses dependency injection for testability.

Business Rules:
1. Required Associations: Each Project must be associated with exactly one Program and one Facility
2. Team Tracking: Each Project must have at least one Team member assigned
3. Outcome Validation: If Status is 'Completed', at least one Outcome must be attached
4. Name Uniqueness: Project Name must be unique within a Program
5. Facility Compatibility: Project's technical requirements must be compatible with facility capabilities
"""

from typing import Dict, List, Optional, Any
from core.repositories.project_repository import ProjectRepository


class ProjectService:
    """Service class for Project business logic"""
    
    def __init__(self, repository=None):
        """Initialize service with repository"""
        self.repository = repository or ProjectRepository()
    
    def get_all_projects(self) -> List:
        """Get all projects"""
        return self.repository.get_all()
    
    def get_project_by_id(self, project_id: int) -> Optional:
        """Get project by ID"""
        return self.repository.get_by_id(project_id)
    
    def create_project(self, data: Dict[str, Any]):
        """
        Create new project with business validation.
        
        Business Rules:
        1. Required Associations: ProgramId and FacilityId are required
        2. Team Tracking: At least one team member must be assigned
        3. Name Uniqueness: Project name must be unique within a Program
        4. Facility Compatibility: Technical requirements must match facility capabilities
        
        Args:
            data: Project data dictionary
            
        Returns:
            Created Project object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule 1: Required Associations
        program_id = data.get('program_id')
        facility_id = data.get('facility_id')
        
        if not program_id or not facility_id:
            raise ValueError("Project.ProgramId and Project.FacilityId are required.")
        
        # Business Rule 2: Team Tracking
        team_members = data.get('team_members', [])
        if not team_members or len(team_members) == 0:
            raise ValueError("Project must have at least one team member assigned.")
        
        # Business Rule 4: Name Uniqueness within Program
        title = data.get('title', '')
        if len(title) < 3:
            raise ValueError("Project title must be at least 3 characters")
        
        # Check if project name exists in the same program
        if self.repository.exists_by_title_in_program(title, program_id):
            raise ValueError("A project with this name already exists in this program.")
        
        # Business Rule 5: Facility Compatibility (if technical requirements provided)
        technical_requirements = data.get('technical_requirements')
        if technical_requirements:
            facility_capabilities = data.get('facility_capabilities')
            if not self._check_facility_compatibility(technical_requirements, facility_capabilities):
                raise ValueError("Project requirements not compatible with facility capabilities.")
        
        # Validate dates if provided
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        return self.repository.create(data)
    
    def _check_facility_compatibility(self, requirements: List[str], capabilities: List[str]) -> bool:
        """
        Check if facility capabilities meet project requirements.
        
        Args:
            requirements: List of technical requirements
            capabilities: List of facility capabilities
            
        Returns:
            True if compatible, False otherwise
        """
        if not capabilities:
            return False
        
        # All requirements must be in capabilities
        return all(req in capabilities for req in requirements)
    
    def update_project(self, project_id: int, data: Dict[str, Any]):
        """
        Update project with business validation.
        
        Business Rules:
        3. Outcome Validation: If Status is 'Completed', at least one Outcome must be attached
        4. Name Uniqueness: Project name must be unique within a Program
        """
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        
        # Business Rule 3: Outcome Validation
        new_status = data.get('status')
        if new_status == 'Completed':
            outcomes = data.get('outcomes', [])
            if not outcomes or len(outcomes) == 0:
                raise ValueError("Completed projects must have at least one documented outcome.")
        
        # Business Rule 4: Check unique title within program (if changing)
        new_title = data.get('title')
        if new_title and new_title != project.title:
            program_id = data.get('program_id', project.program_id)
            if self.repository.exists_by_title_in_program(new_title, program_id):
                raise ValueError("A project with this name already exists in this program.")
        
        # Business Rule 5: Facility Compatibility (if technical requirements updated)
        technical_requirements = data.get('technical_requirements')
        if technical_requirements:
            facility_capabilities = data.get('facility_capabilities')
            if not self._check_facility_compatibility(technical_requirements, facility_capabilities):
                raise ValueError("Project requirements not compatible with facility capabilities.")
        
        # Validate dates
        start_date = data.get('start_date', project.start_date)
        end_date = data.get('end_date', project.end_date)
        
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        return self.repository.update(project, data)
    
    def delete_project(self, project_id: int) -> bool:
        """Delete project"""
        project = self.repository.get_by_id(project_id)
        if not project:
            return False
        
        self.repository.delete(project)
        return True
    
    def get_projects_by_program(self, program_id: int) -> List:
        """Get all projects for a program"""
        return self.repository.filter_by_program(program_id)
    
    def get_projects_by_facility(self, facility_id: int) -> List:
        """Get all projects for a facility"""
        return self.repository.filter_by_facility(facility_id)
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """Get statistics about projects"""
        return {
            'total_projects': self.repository.count(),
        }
