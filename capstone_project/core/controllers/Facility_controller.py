

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Facility
from core.forms.Facility_form import FacilityForm  

# List + filter/search
def facility_list(request):
    facilities = Facility.objects.all()

    f_type = request.GET.get("type")
    f_partner = request.GET.get("partner")
    f_cap = request.GET.get("capability")

    if f_type:
        facilities = facilities.filter(facility_type=f_type)
    if f_partner:
        facilities = facilities.filter(partner=f_partner)
    if f_cap:
        facilities = facilities.filter(capabilities=f_cap) 
    context = {
        "facilities": facilities,
        "facility_types": ['Laboratory','Workshop','Testing Center','Maker Space'],
        "partners": ['UniPod','UIRI','Lwera'],
    } # exact match like facility_type

    return render(request, "Facility/facilityview.html", context)
    

# Detail
def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    return render(request, "Facility/facilitydetail.html", {"facility": facility})


# Create
def facility_create(request):
    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility created successfully!")
            return redirect("core:facility_list")
    else:
        form = FacilityForm()
    return render(request, "Facility/facilityform.html", {"form": form})


# Update
def facility_update(request, pk):
    facility = get_object_or_404(Facility, pk=pk)
    if request.method == "POST":
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility updated successfully!")
            return redirect("core:facility_list")
    else:
        form = FacilityForm(instance=facility)
    return render(request, "Facility/facilityform.html", {"form": form})


# Delete (with safeguard)
def facility_delete(request, pk):
    facility = get_object_or_404(Facility, pk=pk)

    if request.method == "POST":
        # safeguard if linked to projects
        if hasattr(facility, "project_set") and facility.project_set.exists():
            messages.error(request, "Cannot delete: Facility is linked to existing projects.")
            return redirect("core:facility_detail", pk=facility.pk)

        facility.delete()
        messages.success(request, "Facility deleted successfully!")
        return redirect("core:facility_list")

    return render(request, "Facility/facilityconfirmationdelete.html", {"facility": facility})
