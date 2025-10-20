from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.participant_form import ParticipantForm
from core.services import ParticipantService, ProjectService
from core.repositories import ParticipantRepository, ProjectRepository

# List
def participant_list(request):
    participant_service = ParticipantService(ParticipantRepository())
    participants = participant_service.get_all_participants()
    return render(request, "participant/participantview.html", {"participants": participants})

# Detail
def participant_detail(request, pk):
    participant_service = ParticipantService(ParticipantRepository())
    participant = participant_service.get_participant_by_id(pk)
    
    if not participant:
        messages.error(request, "Participant not found.")
        return redirect("core:participant_list")
    
    return render(request, "participant/participantdetail.html", {"participant": participant})

# Create
def participant_create(request):
    participant_service = ParticipantService(ParticipantRepository())
    
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            try:
                participant_service.create_participant({
                    'full_name': form.cleaned_data.get('full_name', ''),
                    'email': form.cleaned_data.get('email', ''),
                    'affiliation': form.cleaned_data.get('affiliation', ''),
                    'specialization': form.cleaned_data.get('specialization', ''),
                    'cross_skill_trained': form.cleaned_data.get('cross_skill_trained', False),
                    'institution': form.cleaned_data.get('institution', ''),
                    'project': form.cleaned_data.get('project')  # Pass the Project object directly
                })
                messages.success(request, "Participant created successfully!")
                return redirect("core:participant_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ParticipantForm()
    return render(request, "participant/participantform.html", {"form": form})

# Update
def participant_update(request, pk):
    participant_service = ParticipantService(ParticipantRepository())
    participant = participant_service.get_participant_by_id(pk)
    
    if not participant:
        messages.error(request, "Participant not found.")
        return redirect("core:participant_list")
    
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            try:
                participant_service.update_participant(pk, {
                    'full_name': form.cleaned_data.get('full_name', ''),
                    'email': form.cleaned_data.get('email', ''),
                    'affiliation': form.cleaned_data.get('affiliation', ''),
                    'specialization': form.cleaned_data.get('specialization', ''),
                    'cross_skill_trained': form.cleaned_data.get('cross_skill_trained', False),
                    'institution': form.cleaned_data.get('institution', ''),
                    'project': form.cleaned_data.get('project')  # Pass the Project object directly
                })
                messages.success(request, "Participant updated successfully!")
                return redirect("core:participant_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ParticipantForm(instance=participant)
    return render(request, "participant/participantform.html", {"form": form})

# Delete
def participant_delete(request, pk):
    participant_service = ParticipantService(ParticipantRepository())
    participant = participant_service.get_participant_by_id(pk)
    
    if not participant:
        messages.error(request, "Participant not found.")
        return redirect("core:participant_list")
    
    if request.method == "POST":
        try:
            participant_service.delete_participant(pk)
            messages.success(request, "Participant deleted successfully!")
            return redirect("core:participant_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:participant_detail", pk=pk)
    
    return render(request, "participant/participant_confirm_delete.html", {"participant": participant})

# Assign participant to project
def assign_participant(request, project_id, participant_id):
    participant_service = ParticipantService(ParticipantRepository())
    project_service = ProjectService(ProjectRepository())
    
    project = project_service.get_project_by_id(project_id)
    participant = participant_service.get_participant_by_id(participant_id)
    
    if not project or not participant:
        messages.error(request, "Project or participant not found.")
        return redirect("core:project_list")
    
    try:
        participant_service.assign_to_project(participant_id, project_id)
        messages.success(request, f"{participant.full_name} assigned to {project.title}.")
        return redirect("core:project_detail", pk=project_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect("core:project_detail", pk=project_id)

# Remove participant from project
def remove_participant(request, project_id, participant_id):
    participant_service = ParticipantService(ParticipantRepository())
    participant = participant_service.get_participant_by_id(participant_id)
    
    if not participant:
        messages.error(request, "Participant not found.")
        return redirect("core:project_detail", pk=project_id)
    
    try:
        participant_service.remove_from_project(participant_id)
        messages.success(request, f"{participant.full_name} removed from project.")
        return redirect("core:project_detail", pk=project_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect("core:project_detail", pk=project_id)

