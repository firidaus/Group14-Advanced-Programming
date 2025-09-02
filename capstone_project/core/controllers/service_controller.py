# core/controllers/service_controller.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models.service import Service
from core.forms.service_form import ServiceForm

def service_list(request):
    services = Service.objects.select_related('FacilityId').all()
    
    # Filtering based on your model fields
    category = request.GET.get("category")
    skill_type = request.GET.get("skill_type")
    facility = request.GET.get("facility")
    
    if category:
        services = services.filter(category=category)
    if skill_type:
        services = services.filter(skill_type=skill_type)
    if facility:
        services = services.filter(FacilityId_id=facility)
    
    context = {
        "services": services,
        "categories": [choice[0] for choice in Service.CATEGORY_CHOICES],
        "skill_types": [choice[0] for choice in Service.SKILL_TYPE_CHOICES],
    }
    return render(request, "service/list.html", context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "service/detail.html", {"service": service})

def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully!")
            return redirect("core:service_list")
    else:
        form = ServiceForm()
    return render(request, "service/form.html", {"form": form})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect("core:service_detail", pk=service.ServiceId)
    else:
        form = ServiceForm(instance=service)
    return render(request, "service/form.html", {"form": form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect("core:service_list")
    return render(request, "service/confirm_delete.html", {"service": service})