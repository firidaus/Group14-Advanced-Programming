"""
Unit Tests for ServiceService - Business Rules ONLY

Business Rules (from Table 1.4):
1. Required Fields: FacilityId, Name, Category, SkillType must be provided
2. Scoped Uniqueness: Service name must be unique within a Facility
3. Delete Guard: Cannot delete Service if any Project at that Facility references its Category in TestingRequirements

Uses MockServiceRepository for isolation.
"""

import pytest
from core.services.service_service import ServiceService
from core.repositories.mock_service_repository import MockServiceRepository
from unittest.mock import Mock


@pytest.fixture
def service_service():
    repo = MockServiceRepository()
    repo.clear()
    return ServiceService(repository=repo)


@pytest.fixture
def valid_service_data():
    return {
        'name': 'Functional Testing',
        'description': 'Service for functional testing of devices',
        'category': 'Testing',
        'skill_type': 'Hardware',
        'facility_id': 1
    }


@pytest.mark.unit
class TestServiceBusinessRules:

    def test_required_fields(self, service_service):
        """Missing required fields should be rejected"""
        from django.core.exceptions import ValidationError

        # missing facility_id
        data = {'name': 'S1', 'category': 'Testing', 'skill_type': 'Hardware'}
        with pytest.raises(ValueError, match="Service.Facilityld, Service.Name, Service.Category, and Service.SkillType are required"):
            service_service.create_service(data)

        # missing name
        data = {'facility_id': 1, 'category': 'Testing', 'skill_type': 'Hardware'}
        with pytest.raises(ValueError, match="Service.Facilityld, Service.Name, Service.Category, and Service.SkillType are required"):
            service_service.create_service(data)

        # missing category
        data = {'facility_id': 1, 'name': 'S1', 'skill_type': 'Hardware'}
        with pytest.raises(ValueError, match="Service.Facilityld, Service.Name, Service.Category, and Service.SkillType are required"):
            service_service.create_service(data)

        # missing skill_type
        data = {'facility_id': 1, 'name': 'S1', 'category': 'Testing'}
        with pytest.raises(ValueError, match="Service.Facilityld, Service.Name, Service.Category, and Service.SkillType are required"):
            service_service.create_service(data)

    def test_scoped_uniqueness_same_facility_fails(self, service_service, valid_service_data):
        # Create first service
        service_service.create_service(valid_service_data)

        duplicate = valid_service_data.copy()
        duplicate['description'] = 'Duplicate'
        with pytest.raises(ValueError, match="A service with this name already exists in this facility"):
            service_service.create_service(duplicate)

    def test_scoped_uniqueness_different_facility_succeeds(self, service_service, valid_service_data):
        # Create first service at facility 1
        service_service.create_service(valid_service_data)

        # Same name different facility
        other = valid_service_data.copy()
        other['facility_id'] = 2
        service = service_service.create_service(other)
        assert service is not None

    def test_delete_guard_service_in_use_by_project_fails(self, service_service, valid_service_data):
        """If any Project at the Facility references the Service category in testing requirements, deletion fails"""
        from django.core.exceptions import ValidationError

        # Create service
        service = service_service.create_service(valid_service_data)

        # Simulate a project at the same facility that references this category
        # We'll mock repository method that service_service should consult; since it uses repository directly,
        # add a helper on the mock repo to simulate the check.
        # attach the project check helper to the repository
        def project_refs_category(facility_id, category):
            return True if facility_id == 1 and category == 'Testing' else False

        service_service.repository.project_refs_category = project_refs_category

        with pytest.raises(ValueError, match="Service in use by Project testing requirements"):
            service_service.delete_service(service.service_id)

    def test_delete_guard_service_not_in_use_succeeds(self, service_service, valid_service_data):
        # Create service
        service = service_service.create_service(valid_service_data)

        # ensure project_refs_category returns False
        service_service.repository.project_refs_category = lambda f, c: False

        result = service_service.delete_service(service.service_id)
        assert result is True
