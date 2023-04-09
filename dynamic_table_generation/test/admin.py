from django.contrib import admin
from .models import DynamicModelDefinition

@admin.register(DynamicModelDefinition)
class DynamicModelDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'created_at', 'changed_at')
