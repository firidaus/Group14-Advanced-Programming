"""
Service Layer

Contains all business logic and use cases.
Services use repositories for data access (dependency injection).

Key Principles:
- Services contain business rules (validation, calculations, workflows)
- Services are UI-agnostic (work with web, mobile, CLI)
- Services use repositories for data access (testable with mocks)
- Services can be tested without database
"""

from .program_service import ProgramService
from .facility_service import FacilityService
from .project_service import ProjectService
from .service_service import ServiceService
from .equipment_service import EquipmentService
from .participant_service import ParticipantService
from .outcome_service import OutcomeService

__all__ = [
    'ProgramService',
    'FacilityService',
    'ProjectService',
    'ServiceService',
    'EquipmentService',
    'ParticipantService',
    'OutcomeService',
]
