"""
Mock Program Repository

Used for unit testing business logic without database dependency.
Simulates database operations in memory.
"""

from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockProgramRepository:
    """
    Mock repository for testing Program services in isolation.
    Stores data in memory instead of database.
    """
    
    def __init__(self):
        """Initialize with empty in-memory storage."""
        self.programs = []
        self._next_id = 1
    
    def get_all(self) -> List[Mock]:
        """Return all programs from in-memory storage."""
        return self.programs.copy()
    
    def get_by_id(self, program_id: int) -> Optional[Mock]:
        """Find a program by ID from in-memory storage."""
        for program in self.programs:
            if program.id == program_id:
                return program
        return None
    
    def create(self, data: Dict[str, Any]) -> Mock:
        """
        Create a new mock program.
        
        Args:
            data: Program fields
            
        Returns:
            Mock program object
        """
        program = Mock()
        program.id = self._next_id
        self._next_id += 1
        
        # Set all fields from data
        for key, value in data.items():
            setattr(program, key, value)
        
        # Add save method (does nothing in mock)
        program.save = Mock()
        program.delete = Mock()
        
        self.programs.append(program)
        return program
    
    def update(self, program: Mock, data: Dict[str, Any]) -> Mock:
        """Update a mock program."""
        for key, value in data.items():
            setattr(program, key, value)
        return program
    
    def delete(self, program: Mock) -> None:
        """Delete a mock program."""
        if program in self.programs:
            self.programs.remove(program)
    
    def filter_by_name(self, name: str) -> List[Mock]:
        """Filter programs by name (case-insensitive)."""
        return [
            p for p in self.programs 
            if hasattr(p, 'name') and name.lower() in p.name.lower()
        ]
    
    def filter_by_duration(self, duration: int) -> List[Mock]:
        """Filter programs by duration."""
        return [
            p for p in self.programs 
            if hasattr(p, 'duration') and p.duration == duration
        ]
    
    def exists_by_name(self, name: str) -> bool:
        """Check if a program with given name exists."""
        return any(
            hasattr(p, 'name') and p.name.lower() == name.lower() 
            for p in self.programs
        )
    
    def count(self) -> int:
        """Count total programs."""
        return len(self.programs)
    
    def clear(self):
        """Clear all data (useful between tests)."""
        self.programs = []
        self._next_id = 1
