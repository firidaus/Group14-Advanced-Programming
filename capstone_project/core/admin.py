from django.contrib import admin
from .models import Program



@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ('ProgramId', 'name', 'start_date', 'end_date', 'active')
	search_fields = ('name', 'national_alignment')
     
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'partner', 'facility_type')
    search_fields = ('name', 'location', 'partner', 'facility_type')
    list_filter = ('partner', 'facility_type')
    filter_horizontal = ('capabilities',)