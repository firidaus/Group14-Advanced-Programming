from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models.participant import Participant
from core.forms.participant_form import ParticipantForm
from core.models.project import Project

# List
def participant_list(request):
    participants = Participant.objects.all()
    return render(request, "participant/participantview.html", {"participants": participants})

# Detail
def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    return render(request, "participant/participantdetail.html", {"participant": participant})

# Create
def participant_create(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant created successfully!")
            return redirect("core:participant_list")
    else:
        form = ParticipantForm()
    return render(request, "participant/participantform.html", {"form": form})

# Update
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect("core:participant_list")
    else:
        form = ParticipantForm(instance=participant)
    return render(request, "participant/participantform.html", {"form": form})

# Delete
def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect("core:participant_list")
    return render(request, "participant/participant_confirm_delete.html", {"participant": participant})

# Assign participant to project
# Assign participant to project
def assign_participant(request, project_id, participant_id):
    project = get_object_or_404(Project, pk=project_id)
    participant = get_object_or_404(Participant, pk=participant_id)
    participant.project = project
    participant.save()
    messages.success(request, f"{participant.full_name} assigned to {project.title}.")
    return redirect("core:project_detail", pk=project_id)

# Remove participant from project
def remove_participant(request, project_id, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id, project_id=project_id)
    participant.project = None  # set to null (only if project field allows null=True)
    participant.save()
    messages.success(request, f"{participant.full_name} removed from project.")
    return redirect("core:project_detail", pk=project_id)

