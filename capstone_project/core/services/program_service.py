"""
Program Service

Contains all business logic for Program entity.
Uses dependency injection to allow repository swapping for testing.

Business Rules Implemented:
- No duplicate program names
- End date must be after start date
- Duration must match date range
- Program name must be at least 3 characters
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from core.repositories.program_repository import ProgramRepository


class ProgramService:
    """
    Service class for Program business logic.
    All business rules and use cases for programs.
    """
    
    def __init__(self, repository=None):
        """
        Initialize service with repository.
        
        Args:
            repository: Repository instance (defaults to ProgramRepository).
                       Can be MockProgramRepository for testing.
        """
        self.repository = repository or ProgramRepository()
    
    def get_all_programs(self) -> List:
        """
        Get all programs.
        
        Returns:
            List of all Program objects
        """
        return self.repository.get_all()
    
    def get_program_by_id(self, program_id: int) -> Optional:
        """
        Get a specific program by ID.
        
        Args:
            program_id: The ID of the program
            
        Returns:
            Program object if found, None otherwise
        """
        return self.repository.get_by_id(program_id)
    
    def create_program(self, data: Dict[str, Any]):
        """
        Create a new program with business validation.
        
        Business Rules:
        - Name must be unique
        - Name must be at least 3 characters
        - End date must be after start date
        
        Args:
            data: Dictionary with program fields (from form.cleaned_data)
            
        Returns:
            Newly created Program object
            
        Raises:
            ValueError: If business rules are violated
        """
        # Business Rule #1: Name must be at least 3 characters
        name = data.get('name', '')
        if len(name) < 3:
            raise ValueError("Program name must be at least 3 characters")
        
        # Business Rule #2: No duplicate names
        if self.repository.exists_by_name(name):
            raise ValueError(f"Program with name '{name}' already exists")
        
        # Business Rule #3: End date must be after start date
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
        
        # All validations passed - create program
        return self.repository.create(data)
    
    def update_program(self, program_id: int, data: Dict[str, Any]):
        """
        Update an existing program with business validation.
        
        Args:
            program_id: ID of program to update
            data: Dictionary with fields to update
            
        Returns:
            Updated Program object
            
        Raises:
            ValueError: If business rules violated or program not found
        """
        program = self.repository.get_by_id(program_id)
        if not program:
            raise ValueError(f"Program with ID {program_id} not found")
        
        # Business Rule: Name must be unique (except for current program)
        new_name = data.get('name')
        if new_name and new_name != program.name:
            if self.repository.exists_by_name(new_name):
                raise ValueError(f"Program with name '{new_name}' already exists")
        
        # Business Rule: End date must be after start date
        start_date = data.get('start_date', program.start_date)
        end_date = data.get('end_date', program.end_date)
        
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        return self.repository.update(program, data)
    
    def delete_program(self, program_id: int) -> bool:
        """
        Delete a program.
        
        Args:
            program_id: ID of program to delete
            
        Returns:
            True if deleted, False if not found
        """
        program = self.repository.get_by_id(program_id)
        if not program:
            return False
        
        self.repository.delete(program)
        return True
    
    def search_programs(self, query: str) -> List:
        """
        Search programs by name.
        
        Args:
            query: Search string
            
        Returns:
            List of matching programs
        """
        if not query or len(query) < 2:
            return []
        
        return self.repository.filter_by_name(query)
    
    def filter_by_duration(self, duration: int) -> List:
        """
        Get programs with specific duration.
        
        Args:
            duration: Duration in months
            
        Returns:
            List of matching programs
        """
        return self.repository.filter_by_duration(duration)
    
    def get_program_statistics(self):
        """
        Get statistics about programs.
        
        Returns:
            Dictionary with program statistics including:
            - total_programs: Total number of programs
            - active_programs: Number of active programs
        """
        all_programs = self.repository.get_all()
        
        total = len(all_programs)
        active = len([p for p in all_programs if p.active])
        
        return {
            'total_programs': total,
            'active_programs': active,
        }
    
    def _calculate_duration_months(self, start_date, end_date) -> int:
        """
        Calculate duration in months between two dates.
        This is a private business logic method.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Duration in months
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        months = (end_date.year - start_date.year) * 12
        months += end_date.month - start_date.month
        
        return months
