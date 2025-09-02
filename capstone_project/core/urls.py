from django.urls import path
from core.controllers import program_controller as pc
from core.controllers import Facility_controller as fa
from core.controllers import project_controller as pr
from core.controllers import service_controller as sc
from .views import (
    EquipmentListView,
    FacilityEquipmentListView,
    EquipmentDetailView,
    EquipmentCreateView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    EquipmentSearchView,
)

app_name = 'core'

urlpatterns = [
    # Programs
    path('', pc.program_list, name='home'),
    path('programs/', pc.program_list, name='program_list'),
    path('programs/create/', pc.program_create, name='program_create'),
    path('programs/<int:pk>/', pc.program_detail, name='program_detail'),
    path('programs/<int:pk>/edit/', pc.program_update, name='program_update'),
    path('programs/<int:pk>/delete/', pc.program_delete, name='program_delete'),

    # Facilities
    path('facilities/', fa.facility_list, name='facility_list'),
    path('facilities/create/', fa.facility_create, name='facility_create'),
    path('facilities/<int:pk>/', fa.facility_detail, name='facility_detail'),
    path('facilities/<int:pk>/edit/', fa.facility_update, name='facility_update'),
    path('facilities/<int:pk>/delete/', fa.facility_delete, name='facility_delete'),

    # Projects
    path('projects/', pr.project_list, name='project_list'),
    path('projects/create/', pr.project_create, name='project_create'),
    path('projects/<int:pk>/', pr.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', pr.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', pr.project_delete, name='project_delete'),

    # Services
    path('services/', sc.service_list, name='service_list'),
    path('services/create/', sc.service_create, name='service_create'),
    path('services/<int:pk>/', sc.service_detail, name='service_detail'),
    path('services/<int:pk>/edit/', sc.service_update, name='service_update'),
    path('services/<int:pk>/delete/', sc.service_delete, name='service_delete'),

    # Equipments
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/search/', EquipmentSearchView.as_view(), name='equipment_search'),
    path('equipment/<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('facility/<int:facility_id>/equipment/', FacilityEquipmentListView.as_view(), name='facility_equipment_list'),
]
