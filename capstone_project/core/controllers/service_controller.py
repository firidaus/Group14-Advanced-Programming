# core/controllers/service_controller.py
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.service_form import ServiceForm
from core.services import ServiceService
from core.repositories import ServiceRepository

def service_list(request):
    service_service = ServiceService(ServiceRepository())
    services = service_service.get_all_services()
    
    # Filtering based on your model fields
    category = request.GET.get("category")
    skill_type = request.GET.get("skill_type")
    facility = request.GET.get("facility")
    
    if category:
        services = service_service.filter_by_category(category)
    if skill_type:
        services = service_service.filter_by_skill_type(skill_type)
    if facility:
        services = service_service.filter_by_facility(int(facility))
    
    # Get choices from the service (assuming they match the model)
    from core.models.service import Service
    context = {
        "services": services,
        "categories": [choice[0] for choice in Service.CATEGORY_CHOICES],
        "skill_types": [choice[0] for choice in Service.SKILL_TYPE_CHOICES],
    }
    return render(request, "service/list.html", context)

def service_detail(request, pk):
    service_service = ServiceService(ServiceRepository())
    service = service_service.get_service_by_id(pk)
    
    if not service:
        messages.error(request, "Service not found.")
        return redirect("core:service_list")
    
    return render(request, "service/detail.html", {"service": service})

def service_create(request):
    service_service = ServiceService(ServiceRepository())
    
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            try:
                service_service.create_service({
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'category': form.cleaned_data.get('category', ''),
                    'skill_type': form.cleaned_data.get('skill_type', ''),
                    'FacilityId': form.cleaned_data.get('FacilityId')  # Pass the Facility object directly
                })
                messages.success(request, "Service created successfully!")
                return redirect("core:service_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ServiceForm()
    return render(request, "service/form.html", {"form": form})

def service_update(request, pk):
    service_service = ServiceService(ServiceRepository())
    service = service_service.get_service_by_id(pk)
    
    if not service:
        messages.error(request, "Service not found.")
        return redirect("core:service_list")
    
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            try:
                service_service.update_service(pk, {
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'category': form.cleaned_data.get('category', ''),
                    'skill_type': form.cleaned_data.get('skill_type', ''),
                    'FacilityId': form.cleaned_data.get('FacilityId')  # Pass the Facility object directly
                })
                messages.success(request, "Service updated successfully!")
                return redirect("core:service_detail", pk=service.ServiceId)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ServiceForm(instance=service)
    return render(request, "service/form.html", {"form": form})

def service_delete(request, pk):
    service_service = ServiceService(ServiceRepository())
    service = service_service.get_service_by_id(pk)
    
    if not service:
        messages.error(request, "Service not found.")
        return redirect("core:service_list")
    
    if request.method == "POST":
        try:
            service_service.delete_service(pk)
            messages.success(request, "Service deleted successfully!")
            return redirect("core:service_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:service_detail", pk=pk)
    
    return render(request, "service/confirm_delete.html", {"service": service})