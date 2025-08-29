from django.shortcuts import render, get_object_or_404, redirect
from core.models.program import Program
from core.forms.program_form import ProgramForm


def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program/list.html', {'programs': programs})


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
