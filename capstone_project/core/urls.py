from django.urls import path
from core.controllers import program_controller as pc
from core.controllers import Facility_controller as fa
from core.controllers import project_controller as pr
from core.controllers import service_controller as sc
from core.controllers import Equipment_controller as eq
from core.controllers import participant_controller as pa
from core.controllers import outcome_controller as oc
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
    path('facilities/filter/', fa.facility_filter_ajax, name='facility_filter_ajax'),
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
    path('equipment/', eq.equipment_list, name='equipment_list'),
    path('equipment/search/', eq.equipment_search, name='equipment_search'),
    path('equipment/<int:pk>/', eq.equipment_detail, name='equipment_detail'),
    path('equipment/create/', eq.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/edit/', eq.equipment_update, name='equipment_update'),
    path('equipment/<int:pk>/delete/', eq.equipment_delete, name='equipment_delete'),
    path('facility/<int:facility_id>/equipment/', eq.equipment_by_facility, name='facility_equipment_list'),

    path('participants/', pa.participant_list, name='participant_list'),
    path('participants/create/', pa.participant_create, name='participant_create'),
    path('participants/<int:pk>/', pa.participant_detail, name='participant_detail'),
    path('participants/<int:pk>/edit/', pa.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', pa.participant_delete, name='participant_delete'),




    path('projects/<int:project_id>/participants/<int:participant_id>/assign/',
         pa.assign_participant, name='assign_participant'),
    path('projects/<int:project_id>/participants/<int:participant_id>/remove/',
         pa.remove_participant, name='remove_participant'),
    path("outcomes/", oc.outcome_list, name="outcome_list"),
    path("outcomes/create/", oc.outcome_create, name="outcome_create"),
    path("outcomes/<int:pk>/", oc.outcome_detail, name="outcome_detail"),
    path("outcomes/<int:pk>/edit/", oc.outcome_update, name="outcome_update"),
    path("outcomes/<int:pk>/delete/", oc.outcome_delete, name="outcome_delete"),
]

