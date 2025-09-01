
from django.shortcuts import render, get_object_or_404, redirect
from core.models.project import Project
from core.forms.project_form import ProjectForm


def project_list(request):
    projects = Project.objects.select_related("program", "facility").all()
    return render(request, "project/list.html", {"projects": projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project/detail.html", {"project": project})


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:project_list")
    else:
        form = ProjectForm()
    return render(request, "project/form.html", {"form": form})


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("core:project_detail", pk=project.ProjectId)
    else:
        form = ProjectForm(instance=project)
    return render(request, "project/form.html", {"form": form, "project": project})


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("core:project_list")
    return render(request, "project/confirm_delete.html", {"project": project})
