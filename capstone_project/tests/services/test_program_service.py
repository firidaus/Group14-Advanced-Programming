"""
Unit Tests for ProgramService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested:
1. Required Fields: Name and Description must be provided
2. Uniqueness: Program Name must be unique (case-insensitive)
3. National Alignment: When FocusAreas is non-empty, NationalAlignment must have valid token
4. Lifecycle Protection: Programs cannot be deleted if they have Projects

Test Pattern: AAA (Arrange-Act-Assert)
Isolation: MockProgramRepository (No Database)
Speed: < 0.5 seconds for all tests
Focus: Business Rule Violations
"""

import pytest
from datetime import date
from core.services.program_service import ProgramService
from core.repositories.mock_program_repository import MockProgramRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def program_service():
    """
    Create a fresh ProgramService with mock repository for each test.
    This ensures test isolation - each test gets a clean slate.
    """
    mock_repo = MockProgramRepository()
    return ProgramService(repository=mock_repo)


@pytest.fixture
def valid_program_data():
    """Sample valid program data matching actual Program model fields."""
    return {
        'name': 'Innovation Program 2024',
        'description': 'Accelerating innovation through collaboration',
        'national_alignment': 'NDPIII, DigitalRoadmap2023_2028',
        'focus_areas': 'AI, Robotics, IoT',
        'phases': 'Cross-Skilling',
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'active': True
    }


@pytest.mark.unit
class TestProgramBusinessRules:
    """Test the 4 core business rules for Program entity."""
    
    def test_required_fields_name_missing(self, program_service):
        """
        Business Rule #1: Required Fields - Name must be provided.
        
        Regression: Prevents creation of programs without names.
        
        Arrange: Program data with empty name
        Act: Attempt to create program
        Assert: ValueError raised with 'Program.Name is required.' message
        """
        # Arrange
        invalid_program = {
            'name': '',  # Empty name - INVALID!
            'description': 'Valid description',
            'national_alignment': 'NDPIII',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Program.Name is required."):
            program_service.create_program(invalid_program)
    
    def test_required_fields_description_missing(self, program_service):
        """
        Business Rule #1: Required Fields - Description must be provided.
        
        Regression: Prevents creation of programs without descriptions.
        
        Arrange: Program data with empty description
        Act: Attempt to create program
        Assert: ValueError raised with 'Program.Description is required.' message
        """
        # Arrange
        invalid_program = {
            'name': 'Valid Program Name',
            'description': '',  # Empty description - INVALID!
            'national_alignment': 'NDPIII',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Program.Description is required."):
            program_service.create_program(invalid_program)
    
    def test_uniqueness_duplicate_name(self, program_service):
        """
        Business Rule #2: Uniqueness - Program name must be unique.
        
        Regression: Prevents duplicate program names in the system.
        
        Arrange: Create first program with a specific name
        Act: Attempt to create second program with same name
        Assert: ValueError raised with 'Program.Name already exists.' message
        """
        # Arrange - Create first program
        first_program = {
            'name': 'Machine Learning Program',
            'description': 'ML research and development',
            'national_alignment': 'NDPIII',  # Fixed: Use valid token
            'focus_areas': 'Machine Learning, AI',
            'phases': 'Prototyping',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 6, 30),
            'active': True
        }
        program_service.create_program(first_program)
        
        # Act & Assert - Try to create duplicate
        duplicate_program = {
            'name': 'Machine Learning Program',  # Same name!
            'description': 'Different description',
            'national_alignment': '4IR',  # Valid token
            'start_date': date(2024, 7, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        with pytest.raises(ValueError, match="Program.Name already exists."):
            program_service.create_program(duplicate_program)
    
    def test_national_alignment_required_when_focus_areas_specified(self, program_service):
        """
        Business Rule #3: National Alignment - When FocusAreas is non-empty,
        NationalAlignment must reference at least one valid alignment token.
        
        Regression: Ensures programs with focus areas align with national strategies.
        
        Arrange: Program with focus_areas but no national_alignment
        Act: Attempt to create program
        Assert: ValueError raised with appropriate message
        """
        # Arrange
        invalid_program = {
            'name': 'AI Innovation Program',
            'description': 'Artificial Intelligence focused program',
            'national_alignment': '',  # Empty - INVALID when focus_areas specified!
            'focus_areas': 'AI, Machine Learning',  # Has focus areas
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Program.NationalAlignment must include at least one recognized"):
            program_service.create_program(invalid_program)
    
    def test_lifecycle_protection_cannot_delete_with_projects(self, program_service):
        """
        Business Rule #4: Lifecycle Protection - Programs cannot be deleted
        if they have associated Projects.
        
        Regression: Prevents orphaning of Project entities and maintains data integrity.
        
        Arrange: Create program and mock it to have associated projects
        Act: Attempt to delete program
        Assert: ValueError raised with 'Program has Projects; archive or reassign before delete.' message
        """
        # Arrange - Create program
        program_data = {
            'name': 'Program With Projects',
            'description': 'This program has projects',
            'national_alignment': 'NDPIII',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        program = program_service.create_program(program_data)
        
        # Mock: Simulate that program has associated projects
        # Create a mock project_set with exists() method
        class MockProjectSet:
            def exists(self):
                return True  # Simulate having projects
        
        program.project_set = MockProjectSet()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Program has Projects; archive or reassign before delete."):
            program_service.delete_program(program.id)  # Use .id not .ProgramId
