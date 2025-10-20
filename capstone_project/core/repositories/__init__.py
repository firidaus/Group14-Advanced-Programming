"""
Repository Layer

Handles all database operations.
Services depend on repositories, not Django ORM directly.
This allows for:
- Easier testing (can mock repositories)
- Better separation of concerns
- Flexibility to change data sources
"""

from .program_repository import ProgramRepository
from .facility_repository import FacilityRepository
from .project_repository import ProjectRepository
from .service_repository import ServiceRepository
from .equipment_repository import EquipmentRepository
from .participant_repository import ParticipantRepository
from .outcome_repository import OutcomeRepository

__all__ = [
    'ProgramRepository',
    'FacilityRepository',
    'ProjectRepository',
    'ServiceRepository',
    'EquipmentRepository',
    'ParticipantRepository',
    'OutcomeRepository',
]
