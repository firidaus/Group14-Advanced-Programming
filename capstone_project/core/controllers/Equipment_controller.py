from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from core.models.Equipment import Equipment 
from core.forms.Equipment_form import EquipmentForm
from django.db.models import Q

# List all equipment
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, "Equipment/list.html", {"equipments": equipments})


# List equipment by facility
def equipment_by_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    equipments = Equipment.objects.filter(facility=facility)
    return render(request, "Equipment/by_facility.html", {"facility": facility, "equipments": equipments})


# Equipment detail view
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, "Equipment/detail.html", {"equipment": equipment})


# Create equipment
def equipment_create(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:equipment_list")
    else:
        form = EquipmentForm()
    return render(request, "Equipment/form.html", {"form": form})


# Update equipment
def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect("core:equipment_list")
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, "Equipment/form.html", {"form": form})


# Delete equipment
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        equipment.delete()
        return redirect("core:equipment_list")
    return render(request, "Equipment/confirm_delete.html", {"equipment": equipment})


# Search equipment
def equipment_search(request):
    query = request.GET.get("q")
    if query:
        equipments = Equipment.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(capabilities__icontains=query)
            | Q(usage_domain__icontains=query)
        )
    else:
        equipments = Equipment.objects.all()
    return render(request, "Equipment/search.html", {"equipments": equipments, "query": query})
