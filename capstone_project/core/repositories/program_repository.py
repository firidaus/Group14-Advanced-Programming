"""
Program Repository

Handles all database operations for Program entity.
Abstracts Django ORM so services don't depend on it directly.
"""

from typing import List, Optional, Dict, Any
from core.models.program import Program


class ProgramRepository:
    """
    Data access layer for Program entity.
    All database queries for programs go through this repository.
    """
    
    def get_all(self) -> List[Program]:
        """
        Retrieve all programs from database.
        
        Returns:
            List of all Program objects
        """
        return list(Program.objects.all())
    
    def get_by_id(self, program_id: int) -> Optional[Program]:
        """
        Find a program by its ID.
        
        Args:
            program_id: The ID of the program
            
        Returns:
            Program object if found, None otherwise
        """
        try:
            return Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return None
    
    def create(self, data: Dict[str, Any]) -> Program:
        """
        Create a new program.
        
        Args:
            data: Dictionary containing program fields
            
        Returns:
            Newly created Program object
        """
        return Program.objects.create(**data)
    
    def update(self, program: Program, data: Dict[str, Any]) -> Program:
        """
        Update an existing program.
        
        Args:
            program: Program instance to update
            data: Dictionary containing fields to update
            
        Returns:
            Updated Program object
        """
        for key, value in data.items():
            setattr(program, key, value)
        program.save()
        return program
    
    def delete(self, program: Program) -> None:
        """
        Delete a program.
        
        Args:
            program: Program instance to delete
        """
        program.delete()
    
    def filter_by_name(self, name: str) -> List[Program]:
        """
        Filter programs by name (case-insensitive contains).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching Program objects
        """
        return list(Program.objects.filter(name__icontains=name))
    
    def filter_by_duration(self, duration: int) -> List[Program]:
        """
        Filter programs by exact duration.
        
        Args:
            duration: Duration in months
            
        Returns:
            List of matching Program objects
        """
        return list(Program.objects.filter(duration=duration))
    
    def exists_by_name(self, name: str) -> bool:
        """
        Check if a program with given name exists.
        
        Args:
            name: Program name to check
            
        Returns:
            True if program exists, False otherwise
        """
        return Program.objects.filter(name__iexact=name).exists()
    
    def count(self) -> int:
        """
        Count total programs in database.
        
        Returns:
            Total number of programs
        """
        return Program.objects.count()
