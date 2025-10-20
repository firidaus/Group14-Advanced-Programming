from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from core.forms.program_form import ProgramForm
from core.services import ProgramService, FacilityService, ProjectService, ServiceService
from core.services import EquipmentService, ParticipantService, OutcomeService
from core.repositories import (
    ProgramRepository, FacilityRepository, ProjectRepository, ServiceRepository,
    EquipmentRepository, ParticipantRepository, OutcomeRepository
)


def program_list(request):
    # Instantiate services with repositories
    program_service = ProgramService(ProgramRepository())
    facility_service = FacilityService(FacilityRepository())
    project_service = ProjectService(ProjectRepository())
    service_service = ServiceService(ServiceRepository())
    equipment_service = EquipmentService(EquipmentRepository())
    participant_service = ParticipantService(ParticipantRepository())
    outcome_service = OutcomeService(OutcomeRepository())
    
    # For the home page, gather dashboard data using services
    context = {
        'programs': program_service.get_all_programs(),
        'programs_count': program_service.get_program_statistics()['total_programs'],
        'facilities_count': facility_service.get_facility_statistics()['total_facilities'],
        'projects_count': project_service.get_project_statistics()['total_projects'],
        'participants_count': participant_service.get_participant_statistics()['total_participants'],
        'equipment_count': equipment_service.get_equipment_statistics()['total_equipment'],
        'services_count': service_service.get_service_statistics()['total_services'],
        'outcomes_count': outcome_service.get_outcome_statistics()['total_outcomes'],
        'today': timezone.now().date(),
        'now': timezone.now(),
    }
    
    # If accessing the root URL, show dashboard; otherwise show program list
    if request.resolver_match.url_name == 'home':
        return render(request, 'home.html', context)
    else:
        return render(request, 'program/list.html', context)


def program_detail(request, pk):
    program_service = ProgramService(ProgramRepository())
    program = program_service.get_program_by_id(pk)
    
    if not program:
        messages.error(request, "Program not found.")
        return redirect('core:program_list')
    
    return render(request, 'program/detail.html', {'program': program})


def program_create(request):
    program_service = ProgramService(ProgramRepository())
    
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            try:
                # Use service to create with validation
                program_service.create_program({
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'national_alignment': form.cleaned_data.get('national_alignment', ''),
                    'focus_areas': form.cleaned_data.get('focus_areas', ''),
                    'phases': form.cleaned_data.get('phases', ''),
                    'start_date': form.cleaned_data.get('start_date'),
                    'end_date': form.cleaned_data.get('end_date'),
                    'active': form.cleaned_data.get('active', True)
                })
                messages.success(request, "Program created successfully!")
                return redirect('core:program_list')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ProgramForm()
    return render(request, 'program/form.html', {'form': form})


def program_update(request, pk):
    program_service = ProgramService(ProgramRepository())
    program = program_service.get_program_by_id(pk)
    
    if not program:
        messages.error(request, "Program not found.")
        return redirect('core:program_list')
    
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            try:
                # Use service to update with validation
                program_service.update_program(pk, {
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'national_alignment': form.cleaned_data.get('national_alignment', ''),
                    'focus_areas': form.cleaned_data.get('focus_areas', ''),
                    'phases': form.cleaned_data.get('phases', ''),
                    'start_date': form.cleaned_data.get('start_date'),
                    'end_date': form.cleaned_data.get('end_date'),
                    'active': form.cleaned_data.get('active', True)
                })
                messages.success(request, "Program updated successfully!")
                return redirect('core:program_detail', pk=program.ProgramId)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ProgramForm(instance=program)
    return render(request, 'program/form.html', {'form': form, 'program': program})


def program_delete(request, pk):
    program_service = ProgramService(ProgramRepository())
    program = program_service.get_program_by_id(pk)
    
    if not program:
        messages.error(request, "Program not found.")
        return redirect('core:program_list')
    
    if request.method == 'POST':
        try:
            program_service.delete_program(pk)
            messages.success(request, "Program deleted successfully!")
            return redirect('core:program_list')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('core:program_detail', pk=pk)
    
    return render(request, 'program/confirm_delete.html', {'program': program})
