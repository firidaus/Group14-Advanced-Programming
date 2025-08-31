from django.urls import path
from core.controllers import program_controller as pc
from core.controllers import Facility_controller as fa


app_name = 'core'

urlpatterns = [
    path('', pc.program_list, name='home'),
    path('programs/', pc.program_list, name='program_list'),
    path('programs/create/', pc.program_create, name='program_create'),
    path('programs/<int:pk>/', pc.program_detail, name='program_detail'),
    path('programs/<int:pk>/edit/', pc.program_update, name='program_update'),
    path('programs/<int:pk>/delete/', pc.program_delete, name='program_delete'),
    path('facilities/',fa.facility_list, name='facility_list'),
    path('facilities/create/', fa.facility_create, name='facility_create'),
    path('facilities/<int:pk>/',fa.facility_detail, name='facility_detail'),
    path('facilities/<int:pk>/edit/', fa.facility_update, name='facility_update'),
    path('facilities/<int:pk>/delete/', fa.facility_delete, name='facility_delete'),
]

