from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.Equipment_form import EquipmentForm
from core.services import EquipmentService, FacilityService
from core.repositories import EquipmentRepository, FacilityRepository

# List all equipment
def equipment_list(request):
    equipment_service = EquipmentService(EquipmentRepository())
    equipments = equipment_service.get_all_equipment()
    return render(request, "Equipment/list.html", {"equipments": equipments})


# List equipment by facility
def equipment_by_facility(request, facility_id):
    equipment_service = EquipmentService(EquipmentRepository())
    facility_service = FacilityService(FacilityRepository())
    
    facility = facility_service.get_facility_by_id(facility_id)
    if not facility:
        messages.error(request, "Facility not found.")
        return redirect("core:facility_list")
    
    equipments = equipment_service.filter_by_facility(facility_id)
    return render(request, "Equipment/by_facility.html", {"facility": facility, "equipments": equipments})


# Equipment detail view
def equipment_detail(request, pk):
    equipment_service = EquipmentService(EquipmentRepository())
    equipment = equipment_service.get_equipment_by_id(pk)
    
    if not equipment:
        messages.error(request, "Equipment not found.")
        return redirect("core:equipment_list")
    
    return render(request, "Equipment/detail.html", {"equipment": equipment})


# Create equipment
def equipment_create(request):
    equipment_service = EquipmentService(EquipmentRepository())
    
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            try:
                equipment_service.create_equipment({
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'capabilities': form.cleaned_data.get('capabilities', ''),
                    'inventory_code': form.cleaned_data.get('inventory_code', ''),
                    'usage_domain': form.cleaned_data.get('usage_domain', ''),
                    'support_phase': form.cleaned_data.get('support_phase', ''),
                    'facility': form.cleaned_data.get('facility')  # Pass the Facility object directly
                })
                messages.success(request, "Equipment created successfully!")
                return redirect("core:equipment_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = EquipmentForm()
    return render(request, "Equipment/form.html", {"form": form})


# Update equipment
def equipment_update(request, pk):
    equipment_service = EquipmentService(EquipmentRepository())
    equipment = equipment_service.get_equipment_by_id(pk)
    
    if not equipment:
        messages.error(request, "Equipment not found.")
        return redirect("core:equipment_list")
    
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            try:
                equipment_service.update_equipment(pk, {
                    'name': form.cleaned_data.get('name', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'capabilities': form.cleaned_data.get('capabilities', ''),
                    'inventory_code': form.cleaned_data.get('inventory_code', ''),
                    'usage_domain': form.cleaned_data.get('usage_domain', ''),
                    'support_phase': form.cleaned_data.get('support_phase', ''),
                    'facility': form.cleaned_data.get('facility')  # Pass the Facility object directly
                })
                messages.success(request, "Equipment updated successfully!")
                return redirect("core:equipment_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, "Equipment/form.html", {"form": form})


# Delete equipment
def equipment_delete(request, pk):
    equipment_service = EquipmentService(EquipmentRepository())
    equipment = equipment_service.get_equipment_by_id(pk)
    
    if not equipment:
        messages.error(request, "Equipment not found.")
        return redirect("core:equipment_list")
    
    if request.method == "POST":
        try:
            equipment_service.delete_equipment(pk)
            messages.success(request, "Equipment deleted successfully!")
            return redirect("core:equipment_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:equipment_detail", pk=pk)
    
    return render(request, "Equipment/confirm_delete.html", {"equipment": equipment})


# Search equipment
def equipment_search(request):
    equipment_service = EquipmentService(EquipmentRepository())
    query = request.GET.get("q")
    
    if query:
        equipments = equipment_service.search_equipment(query)
    else:
        equipments = equipment_service.get_all_equipment()
    
    return render(request, "Equipment/search.html", {"equipments": equipments, "query": query})
