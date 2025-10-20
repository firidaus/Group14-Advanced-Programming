"""
Project Repository

Handles all database operations for Project entity.
"""

from typing import List, Optional, Dict, Any
from core.models.project import Project


class ProjectRepository:
    """Data access layer for Project entity"""
    
    def get_all(self) -> List[Project]:
        """Get all projects with related data"""
        return list(Project.objects.select_related('program', 'facility').all())
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        try:
            return Project.objects.select_related('program', 'facility').get(pk=project_id)
        except Project.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Project:
        """Create new project"""
        return Project.objects.create(**data)
    
    def update(self, project: Project, data: Dict[str, Any]) -> Project:
        """Update existing project"""
        for key, value in data.items():
            setattr(project, key, value)
        project.save()
        return project
    
    def delete(self, project: Project) -> None:
        """Delete project"""
        project.delete()
    
    def filter_by_program(self, program_id: int) -> List[Project]:
        """Filter projects by program"""
        return list(Project.objects.filter(program_id=program_id))
    
    def filter_by_facility(self, facility_id: int) -> List[Project]:
        """Filter projects by facility"""
        return list(Project.objects.filter(facility_id=facility_id))
    
    def exists_by_title(self, title: str) -> bool:
        """Check if project title exists"""
        return Project.objects.filter(title__iexact=title).exists()
    
    def count(self) -> int:
        """Count total projects"""
        return Project.objects.count()
