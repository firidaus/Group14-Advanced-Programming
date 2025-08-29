from django.urls import path
from core.controllers import program_controller as pc

app_name = 'core'

urlpatterns = [
    path('', pc.program_list, name='home'),
    path('programs/', pc.program_list, name='program_list'),
    path('programs/create/', pc.program_create, name='program_create'),
    path('programs/<int:pk>/', pc.program_detail, name='program_detail'),
    path('programs/<int:pk>/edit/', pc.program_update, name='program_update'),
    path('programs/<int:pk>/delete/', pc.program_delete, name='program_delete'),
]
