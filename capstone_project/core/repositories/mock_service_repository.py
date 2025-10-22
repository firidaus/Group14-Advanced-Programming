from typing import List, Optional, Dict, Any
from unittest.mock import Mock


class MockServiceRepository:
    def __init__(self):
        self.services = []
        self._next_id = 1

    def get_all(self) -> List[Mock]:
        return self.services.copy()

    def get_by_id(self, service_id: int) -> Optional[Mock]:
        for s in self.services:
            if getattr(s, 'service_id', None) == service_id or getattr(s, 'ServiceId', None) == service_id:
                return s
        return None

    def create(self, data: Dict[str, Any]) -> Mock:
        service = Mock()
        # set id
        service.service_id = self._next_id
        service.ServiceId = self._next_id
        self._next_id += 1
        # copy fields
        for key, value in data.items():
            setattr(service, key, value)
        service.save = Mock()
        service.delete = Mock()
        self.services.append(service)
        return service

    def update(self, service: Mock, data: Dict[str, Any]) -> Mock:
        for key, value in data.items():
            setattr(service, key, value)
        return service

    def delete(self, service: Mock) -> None:
        if service in self.services:
            self.services.remove(service)

    def filter_by_facility(self, facility_id: int) -> List[Mock]:
        return [s for s in self.services if hasattr(s, 'facility_id') and s.facility_id == facility_id]

    def exists_by_name_in_facility(self, name: str, facility_id: int) -> bool:
        return any(
            hasattr(s, 'name') and hasattr(s, 'facility_id') and
            s.name.lower() == name.lower() and s.facility_id == facility_id
            for s in self.services
        )

    def count(self) -> int:
        return len(self.services)

    def clear(self):
        self.services = []
        self._next_id = 1
