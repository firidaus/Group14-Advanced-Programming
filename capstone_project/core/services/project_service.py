"""
Project Service

Contains all business logic for Project entity.
Uses dependency injection for testability.

Business Rules:
- Project title must be unique
- Project must have a valid program
- Project must have a valid facility
- Start date must be before end date
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
        - Title must be unique
        - Title must be at least 3 characters
        - Start date < End date
        
        Args:
            data: Project data dictionary
            
        Returns:
            Created Project object
            
        Raises:
            ValueError: If business rules violated
        """
        # Business Rule: Title must be at least 3 characters
        title = data.get('title', '')
        if len(title) < 3:
            raise ValueError("Project title must be at least 3 characters")
        
        # Business Rule: Title must be unique
        if self.repository.exists_by_title(title):
            raise ValueError(f"Project '{title}' already exists")
        
        # Business Rule: Start date must be before end date
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        return self.repository.create(data)
    
    def update_project(self, project_id: int, data: Dict[str, Any]):
        """Update project with business validation"""
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        
        # Business Rule: Check unique title (if changing)
        new_title = data.get('title')
        if new_title and new_title != project.title:
            if self.repository.exists_by_title(new_title):
                raise ValueError(f"Project '{new_title}' already exists")
        
        # Business Rule: Validate dates
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
