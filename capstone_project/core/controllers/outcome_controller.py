from django.shortcuts import render, get_object_or_404, redirect
from core.models.Outcome import Outcome
from core.forms.OutcomeForm import OutcomeForm


def outcome_list(request):
    outcomes = Outcome.objects.all()
    return render(request, "outcomes/outcome_list.html", {"outcomes": outcomes})


def outcome_detail(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    return render(request, "outcomes/outcome_detail.html", {"outcome": outcome})


def outcome_create(request):
    if request.method == "POST":
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:outcome_list")
    else:
        form = OutcomeForm()
    return render(request, "outcomes/outcome_form.html", {"form": form})


def outcome_update(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    if request.method == "POST":
        form = OutcomeForm(request.POST, instance=outcome)
        if form.is_valid():
            form.save()
            return redirect("core:outcome_list")
    else:
        form = OutcomeForm(instance=outcome)
    return render(request, "outcomes/outcome_form.html", {"form": form})


def outcome_delete(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    if request.method == "POST":
        outcome.delete()
        return redirect("core:outcome_list")
    return render(request, "outcomes/outcome_confirm_delete.html", {"outcome": outcome})
