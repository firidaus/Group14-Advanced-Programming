

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.forms.Facility_form import FacilityForm
from core.services import FacilityService
from core.repositories import FacilityRepository

# List + filter/search
def facility_list(request):
    facility_service = FacilityService(FacilityRepository())
    facilities = facility_service.get_all_facilities()

    f_type = request.GET.get("type")
    f_partner = request.GET.get("partner")
    f_cap = request.GET.get("capability")

    if f_type:
        facilities = facility_service.filter_by_type(f_type)
    if f_partner:
        facilities = facility_service.filter_by_partner(f_partner)
    if f_cap:
        facilities = facility_service.search_facilities(f_cap)
    
    context = {
        "facilities": facilities,
        "facility_types": ['Laboratory','Workshop','Testing Center','Maker Space'],
        "partners": ['UniPod','UIRI','Lwera'],
    }

    return render(request, "Facility/facilityview.html", context)
    

# AJAX endpoint for filtering facilities
def facility_filter_ajax(request):
    facility_service = FacilityService(FacilityRepository())
    facilities = facility_service.get_all_facilities()

    f_type = request.GET.get("type")
    f_partner = request.GET.get("partner")
    f_cap = request.GET.get("capability")

    if f_type:
        facilities = facility_service.filter_by_type(f_type)
    if f_partner:
        facilities = facility_service.filter_by_partner(f_partner)
    if f_cap:
        facilities = facility_service.search_facilities(f_cap)

    # Render the table rows only
    table_html = render_to_string('Facility/facility_table_rows.html', {'facilities': facilities})
    
    return JsonResponse({
        'table_html': table_html,
        'count': len(facilities)
    })
    

# Detail
def facility_detail(request, pk):
    facility_service = FacilityService(FacilityRepository())
    facility = facility_service.get_facility_by_id(pk)
    
    if not facility:
        messages.error(request, "Facility not found.")
        return redirect("core:facility_list")
    
    return render(request, "Facility/facilitydetail.html", {"facility": facility})


# Create
def facility_create(request):
    facility_service = FacilityService(FacilityRepository())
    
    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            try:
                facility_service.create_facility({
                    'name': form.cleaned_data.get('name', ''),
                    'location': form.cleaned_data.get('location', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'partner': form.cleaned_data.get('partner', ''),
                    'facility_type': form.cleaned_data.get('facility_type', ''),
                    'capabilities': form.cleaned_data.get('capabilities', '')
                })
                messages.success(request, "Facility created successfully!")
                return redirect("core:facility_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = FacilityForm()
    return render(request, "Facility/facilityform.html", {"form": form})


# Update
def facility_update(request, pk):
    facility_service = FacilityService(FacilityRepository())
    facility = facility_service.get_facility_by_id(pk)
    
    if not facility:
        messages.error(request, "Facility not found.")
        return redirect("core:facility_list")
    
    if request.method == "POST":
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            try:
                facility_service.update_facility(pk, {
                    'name': form.cleaned_data.get('name', ''),
                    'location': form.cleaned_data.get('location', ''),
                    'description': form.cleaned_data.get('description', ''),
                    'partner': form.cleaned_data.get('partner', ''),
                    'facility_type': form.cleaned_data.get('facility_type', ''),
                    'capabilities': form.cleaned_data.get('capabilities', '')
                })
                messages.success(request, "Facility updated successfully!")
                return redirect("core:facility_list")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = FacilityForm(instance=facility)
    return render(request, "Facility/facilityform.html", {"form": form})


# Delete (with safeguard)
def facility_delete(request, pk):
    facility_service = FacilityService(FacilityRepository())
    facility = facility_service.get_facility_by_id(pk)
    
    if not facility:
        messages.error(request, "Facility not found.")
        return redirect("core:facility_list")

    if request.method == "POST":
        try:
            # Service handles business logic for deletion checks
            facility_service.delete_facility(pk)
            messages.success(request, "Facility deleted successfully!")
            return redirect("core:facility_list")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("core:facility_detail", pk=pk)

    return render(request, "Facility/facilityconfirmationdelete.html", {"facility": facility})
