import json
from django.utils import timezone
from .models import DynamicModelDefinition

from rest_framework import status
from rest_framework.response import Response


def create_model_definition(name, definition):
    model_definition = DynamicModelDefinition(
        name=name,
        definition=definition,
        created_at=timezone.now(),
        changed_at=timezone.now(),
    )
    model_definition.save()
    return model_definition.pk


def update_model_definition(name, definition_id, definition):
    try:
        model_definition = DynamicModelDefinition.objects.get(pk=definition_id)
    except DynamicModelDefinition.DoesNotExist:
        return Response({'error': 'Dynamic model not found.'}, status=status.HTTP_404_NOT_FOUND)
    try:
        model_definition.definition = json.dumps(definition)
        model_definition.changed_at = timezone.now()
        model_definition.save()
        print(model_definition)
        return model_definition.pk
    except DynamicModelDefinition.DoesNotExist:
        create_model_definition(name, definition)
