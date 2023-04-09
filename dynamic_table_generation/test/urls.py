from django.urls import path
from . import views

urlpatterns = [
    path('table/', views.create_dynamic_model, name='create_dynamic_model'),
    path('table/<int:id>', views.update_dynamic_model, name='update_dynamic_model'),
    path('table/<int:id>/row/', views.create_row, name='create_dynamic_object'),
    path('table/<int:id>/rows/', views.get_rows, name='get_dynamic_objects')
]
