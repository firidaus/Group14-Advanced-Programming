"""
Unit Tests for ProgramService - Business Rules ONLY

This test suite focuses exclusively on testing business rule validation.
Uses Mock Repository for isolation (no database dependency).

Business Rules Tested:
1. Program name must be unique
2. Program name must be at least 3 characters
3. End date must be after start date

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
        'national_alignment': 'National Innovation Strategy',
        'focus_areas': 'AI, Robotics, IoT',
        'phases': 'Cross-Skilling',
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'active': True
    }


# ============================================================================
# BUSINESS RULE TESTS - Program Creation
# ============================================================================

@pytest.mark.unit
class TestProgramBusinessRules:
    """Test the 3 core business rules for Program entity."""
    
    def test_program_name_must_be_unique(self, program_service):
        """
        Business Rule #1: Program name must be unique.
        
        Regression: Prevents duplicate program names in the system.
        
        Arrange: Create first program with a specific name
        Act: Attempt to create second program with same name
        Assert: ValueError raised with 'already exists' message
        """
        # Arrange - Create first program
        first_program = {
            'name': 'Machine Learning Program',
            'description': 'ML research and development',
            'national_alignment': 'Digital Economy',
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
            'start_date': date(2024, 7, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        with pytest.raises(ValueError, match="already exists"):
            program_service.create_program(duplicate_program)
    
    def test_program_name_minimum_length(self, program_service):
        """
        Business Rule #2: Program name must be at least 3 characters.
        
        Regression: Prevents meaningless single/double character names.
        Bug Reference: Issue #42
        
        Arrange: Program data with 2-character name
        Act: Attempt to create program
        Assert: ValueError raised with 'at least 3 characters' message
        """
        # Arrange
        invalid_program = {
            'name': 'AI',  # Only 2 characters - INVALID!
            'description': 'Artificial Intelligence program',
            'national_alignment': 'Innovation Strategy',
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'active': True
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="at least 3 characters"):
            program_service.create_program(invalid_program)
    
    def test_end_date_must_be_after_start_date(self, program_service):
        """
        Business Rule #3: End date must be after start date.
        
        Regression: Prevents illogical date ranges (end before start).
        
        Arrange: Program with end_date before start_date
        Act: Attempt to create program
        Assert: ValueError raised with 'End date must be after start date' message
        """
        # Arrange
        invalid_program = {
            'name': 'Invalid Date Program',
            'description': 'Testing date validation',
            'national_alignment': 'Test Alignment',
            'focus_areas': 'Testing',
            'start_date': date(2024, 12, 31),  # December 31
            'end_date': date(2024, 1, 1),      # January 1 - BEFORE START!
            'active': True
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="End date must be after start date"):
            program_service.create_program(invalid_program)
