from django.urls import path
from . import views

urlpatterns = [
    path('add_table/', views.create_dynamic_model, name='create_dynamic_model'),
]
