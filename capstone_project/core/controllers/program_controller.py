from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from core.models.program import Program
from core.models.Faciltymodels import Facility
from core.models.project import Project
from core.models.participant import Participant
from core.models.Equipment import Equipment
from core.models.service import Service
from core.models.Outcome import Outcome
from core.forms.program_form import ProgramForm


def program_list(request):
    # For the home page, gather dashboard data
    context = {
        'programs': Program.objects.all(),
        'programs_count': Program.objects.count(),
        'facilities_count': Facility.objects.count(),
        'projects_count': Project.objects.count(),
        'participants_count': Participant.objects.count(),
        'equipment_count': Equipment.objects.count(),
        'services_count': Service.objects.count(),
        'outcomes_count': Outcome.objects.count(),
        'today': timezone.now().date(),
        'now': timezone.now(),
    }
    
    # If accessing the root URL, show dashboard; otherwise show program list
    if request.resolver_match.url_name == 'home':
        return render(request, 'home.html', context)
    else:
        return render(request, 'program/list.html', context)


def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'program/detail.html', {'program': program})


def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            p = form.save()
            return redirect('core:program_list')
    else:
        form = ProgramForm()
    return render(request, 'program/form.html', {'form': form})


def program_update(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('core:program_detail', pk=program.ProgramId)
    else:
        form = ProgramForm(instance=program)
    return render(request, 'program/form.html', {'form': form, 'program': program})


def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('core:program_list')
    return render(request, 'program/confirm_delete.html', {'program': program})
