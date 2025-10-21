
from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockProjectRepository:
    
    def __init__(self):
        """Initialize with empty in-memory storage."""
        self.projects = []
        self._next_id = 1
    
    def get_all(self) -> List[Mock]:
        """Return all projects from in-memory storage."""
        return self.projects.copy()
    
    def get_by_id(self, project_id: int) -> Optional[Mock]:
        """Find a project by ID from in-memory storage."""
        for project in self.projects:
            if project.ProjectId == project_id:
                return project
        return None
    
    def create(self, data: Dict[str, Any]) -> Mock:
        project = Mock()
        project.ProjectId = self._next_id
        self._next_id += 1
        
        # Set all fields from data
        for key, value in data.items():
            setattr(project, key, value)
        
        # Add save method 
        project.save = Mock()
        project.delete = Mock()
        
        self.projects.append(project)
        return project
    
    def update(self, project: Mock, data: Dict[str, Any]) -> Mock:
        for key, value in data.items():
            setattr(project, key, value)
        return project
    
    def delete(self, project: Mock) -> None:
        if project in self.projects:
            self.projects.remove(project)
    
    def filter_by_program(self, program_id: int) -> List[Mock]:
        return [
            p for p in self.projects 
            if hasattr(p, 'program_id') and p.program_id == program_id
        ]
    
    def filter_by_facility(self, facility_id: int) -> List[Mock]:
        return [
            p for p in self.projects 
            if hasattr(p, 'facility_id') and p.facility_id == facility_id
        ]
    
    def exists_by_title(self, title: str) -> bool:
        return any(
            hasattr(p, 'title') and p.title.lower() == title.lower() 
            for p in self.projects
        )
    
    def count(self) -> int:
        return len(self.projects)
    
    def clear(self):
        self.projects = []
        self._next_id = 1
