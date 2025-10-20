from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.OutcomeForm import OutcomeForm
from core.services import OutcomeService
from core.repositories import OutcomeRepository


def outcome_list(request):
    outcome_service = OutcomeService(OutcomeRepository())
    outcomes = outcome_service.get_all_outcomes()
    return render(request, "outcomes/outcome_list.html", {"outcomes": outcomes})


def outcome_detail(request, pk):
    outcome_service = OutcomeService(OutcomeRepository())
    outcome = outcome_service.get_outcome_by_id(pk)
    
    if not outcome:
        messages.error(request, "Outcome not found.")
        return redirect("core:outcome_list")
    
    return render(request, "outcomes/outcome_detail.html", {"outcome": outcome})


def outcome_create(request):
    outcome_service = OutcomeService(OutcomeRepository())
    
    if request.method == "POST":
        form = OutcomeForm(request.POST)
        if form.is_valid():
            try:
                outcome_service.create_outcome({
                    'project': form.cleaned_data.get('project'),  # Pass the Project object directly
                    'title': form.cleaned_data.get('title', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'artifact_link': form.cleaned_data.get('artifact_link', ''),
                    'outcome_type': form.cleaned_data.get('outcome_type', ''),
                    'quality_certification': form.cleaned_data.get('quality_certification', ''),
                    'commercialization_status': form.cleaned_data.get('commercialization_status', '')
                })
                messages.success(request, "Outcome created successfully!")
                return redirect("core:outcome_list")
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error creating outcome: {str(e)}")
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = OutcomeForm()
    return render(request, "outcomes/outcome_form.html", {"form": form})


def outcome_update(request, pk):
    outcome_service = OutcomeService(OutcomeRepository())
    outcome = outcome_service.get_outcome_by_id(pk)
    
    if not outcome:
        messages.error(request, "Outcome not found.")
        return redirect("core:outcome_list")
    
    if request.method == "POST":
        form = OutcomeForm(request.POST, instance=outcome)
        if form.is_valid():
            try:
                outcome_service.update_outcome(pk, {
                    'project': form.cleaned_data.get('project'),  # Pass the Project object directly
                    'title': form.cleaned_data.get('title', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'artifact_link': form.cleaned_data.get('artifact_link', ''),
                    'outcome_type': form.cleaned_data.get('outcome_type', ''),
                    'quality_certification': form.cleaned_data.get('quality_certification', ''),
                    'commercialization_status': form.cleaned_data.get('commercialization_status', '')
                })
                messages.success(request, "Outcome updated successfully!")
                return redirect("core:outcome_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = OutcomeForm(instance=outcome)
    return render(request, "outcomes/outcome_form.html", {"form": form})


def outcome_delete(request, pk):
    outcome_service = OutcomeService(OutcomeRepository())
    outcome = outcome_service.get_outcome_by_id(pk)
    
    if not outcome:
        messages.error(request, "Outcome not found.")
        return redirect("core:outcome_list")
    
    if request.method == "POST":
        try:
            outcome_service.delete_outcome(pk)
            messages.success(request, "Outcome deleted successfully!")
            return redirect("core:outcome_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:outcome_detail", pk=pk)
    
    return render(request, "outcomes/outcome_confirm_delete.html", {"outcome": outcome})
