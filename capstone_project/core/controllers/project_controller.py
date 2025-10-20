
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.project_form import ProjectForm
from core.services import ProjectService
from core.repositories import ProjectRepository


def project_list(request):
    project_service = ProjectService(ProjectRepository())
    projects = project_service.get_all_projects()
    return render(request, "project/list.html", {"projects": projects})


def project_detail(request, pk):
    project_service = ProjectService(ProjectRepository())
    project = project_service.get_project_by_id(pk)
    
    if not project:
        messages.error(request, "Project not found.")
        return redirect("core:project_list")
    
    return render(request, "project/detail.html", {"project": project})


def project_create(request):
    project_service = ProjectService(ProjectRepository())
    
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            try:
                project_service.create_project({
                    'title': form.cleaned_data.get('title', ''),
                    'nature_of_project': form.cleaned_data.get('nature_of_project', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'innovation_focus': form.cleaned_data.get('innovation_focus', ''),
                    'prototype_stage': form.cleaned_data.get('prototype_stage', ''),
                    'testing_requirements': form.cleaned_data.get('testing_requirements', ''),
                    'commercialization_plan': form.cleaned_data.get('commercialization_plan', ''),
                    'program': form.cleaned_data.get('program'),  # Pass the Program object directly
                    'facility': form.cleaned_data.get('facility')  # Pass the Facility object directly
                })
                messages.success(request, "Project created successfully!")
                return redirect("core:project_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ProjectForm()
    return render(request, "project/form.html", {"form": form})


def project_update(request, pk):
    project_service = ProjectService(ProjectRepository())
    project = project_service.get_project_by_id(pk)
    
    if not project:
        messages.error(request, "Project not found.")
        return redirect("core:project_list")
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            try:
                project_service.update_project(pk, {
                    'title': form.cleaned_data.get('title', ''),
                    'nature_of_project': form.cleaned_data.get('nature_of_project', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'innovation_focus': form.cleaned_data.get('innovation_focus', ''),
                    'prototype_stage': form.cleaned_data.get('prototype_stage', ''),
                    'testing_requirements': form.cleaned_data.get('testing_requirements', ''),
                    'commercialization_plan': form.cleaned_data.get('commercialization_plan', ''),
                    'program': form.cleaned_data.get('program'),  # Pass the Program object directly
                    'facility': form.cleaned_data.get('facility')  # Pass the Facility object directly
                })
                messages.success(request, "Project updated successfully!")
                return redirect("core:project_detail", pk=project.ProjectId)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ProjectForm(instance=project)
    return render(request, "project/form.html", {"form": form, "project": project})


def project_delete(request, pk):
    project_service = ProjectService(ProjectRepository())
    project = project_service.get_project_by_id(pk)
    
    if not project:
        messages.error(request, "Project not found.")
        return redirect("core:project_list")
    
    if request.method == "POST":
        try:
            project_service.delete_project(pk)
            messages.success(request, "Project deleted successfully!")
            return redirect("core:project_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:project_detail", pk=pk)
    
    return render(request, "project/confirm_delete.html", {"project": project})
