from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Equipment, Facility  # Import your models
# Create your views here.
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment/list.html'
    context_object_name = 'equipments'  # Used in template as {% for equipment in equipments %}

class FacilityEquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment/by_facility.html'

    def get_queryset(self):
        facility_id = self.kwargs['facility_id']
        return Equipment.objects.filter(facility_id=facility_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facility'] = get_object_or_404(Facility, pk=self.kwargs['facility_id'])
        return context

class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'equipment/detail.html'
    context_object_name = 'equipment'

class EquipmentCreateView(CreateView):
    model = Equipment
    fields = ['facility', 'name', 'description', 'capabilities', 'inventory_code', 'usage_domain', 'support_phase']
    template_name = 'equipment/form.html'
    success_url = reverse_lazy('equipment_list')  # Redirect to list after create

class EquipmentUpdateView(UpdateView):
    model = Equipment
    fields = ['name', 'description', 'capabilities', 'inventory_code', 'usage_domain', 'support_phase']  # Facility not editable to avoid breaking links; adjust if needed
    template_name = 'equipment/form.html'
    success_url = reverse_lazy('equipment_list')  # Redirect to list after update

class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'equipment/confirm_delete.html'
    success_url = reverse_lazy('equipment_list')  # Redirect to list after delete

class EquipmentSearchView(ListView):
    model = Equipment
    template_name = 'equipment/search.html'
    context_object_name = 'equipments'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Search capabilities (comma-separated) or usage_domain
            return Equipment.objects.filter(capabilities__icontains=query) | Equipment.objects.filter(usage_domain__icontains=query)
        return Equipment.objects.all()