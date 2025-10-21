"""
Pytest configuration and shared fixtures for all tests.
This file provides common test utilities and fixtures.
"""
import os
import sys
import pytest
import django
from datetime import date

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, '..'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone_project.settings')
django.setup()

# Import after Django setup
from core.repositories.mock_program_repository import MockProgramRepository
from core.repositories.mock_facility_repository import MockFacilityRepository
from core.repositories.mock_equipment_repository import MockEquipmentRepository
from core.services import (
    ProgramService, FacilityService, ProjectService, ServiceService,
    EquipmentService, ParticipantService, OutcomeService
)


# ============================================================================
# SERVICE FIXTURES (with Mock Repositories)
# ============================================================================

@pytest.fixture
def program_service():
    """Create ProgramService with mock repository for testing."""
    mock_repo = MockProgramRepository()
    return ProgramService(mock_repo)


@pytest.fixture
def facility_service():
    """Create FacilityService with mock repository for testing."""
    mock_repo = MockFacilityRepository()
    return FacilityService(mock_repo)


@pytest.fixture
def equipment_service():
    """Create EquipmentService with mock repository for testing."""
    mock_repo = MockEquipmentRepository()
    return EquipmentService(mock_repo)


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_program_data():
    """Sample program data for testing."""
    return {
        'name': 'Innovation Program 2024',
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'duration': 12
    }


@pytest.fixture
def sample_facility_data():
    """Sample facility data for testing."""
    return {
        'facility_name': 'Innovation Lab',
        'facility_type': 'Laboratory',
        'location_city': 'Kampala',
        'location_district': 'Central',
        'capabilities': '3D Printing, Testing, AI',
        'partner': 'UniPod'
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        'title': 'Smart Agriculture Project',
        'description': 'IoT-based smart farming solution',
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 6, 30),
        'status': 'Active'
    }


@pytest.fixture
def sample_service_data():
    """Sample service data for testing."""
    return {
        'service_name': 'Technical Training',
        'category': 'Training',
        'skill_type': 'Technical'
    }


@pytest.fixture
def sample_equipment_data():
    """Sample equipment data for testing."""
    return {
        'name': '3D Printer Pro',
        'description': 'High-precision 3D printer',
        'capabilities': 'PLA, ABS, PETG printing',
        'usage_domain': 'Prototyping'
    }


@pytest.fixture
def sample_participant_data():
    """Sample participant data for testing."""
    return {
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'institution': 'Makerere University',
        'cross_skill': 'Programming, Design'
    }


@pytest.fixture
def sample_outcome_data():
    """Sample outcome data for testing."""
    return {
        'economic_impact_score': 85,
        'social_impact_score': 75,
        'environmental_impact_score': 90,
        'patents_filed': 2
    }


# ============================================================================
# DATABASE FIXTURES (for integration tests)
# ============================================================================

@pytest.fixture(scope='function')
def db_setup(django_db_setup, django_db_blocker):
    """
    Setup test database for integration tests.
    This fixture uses Django's test database.
    """
    with django_db_blocker.unblock():
        # Database is automatically created by pytest-django
        yield
        # Database is automatically cleaned up after the test


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def assert_validation_error(error_message, expected_substring):
    """
    Helper to assert that a validation error contains expected message.
    
    Args:
        error_message: The actual error message
        expected_substring: The expected substring in the error
    """
    assert expected_substring.lower() in str(error_message).lower(), \
        f"Expected '{expected_substring}' in error message, got: {error_message}"


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require database"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that require database"
    )
    config.addinivalue_line(
        "markers", "api: API endpoint tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
