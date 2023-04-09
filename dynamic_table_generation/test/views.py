import logging
import json

from django.apps import apps
from django.db import connection
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.db import models

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import DynamicModelDefinition, register_dynamic_model
from .serializers import DynamicModelSerializer, DynamicModelRowSerializer
from .utils import create_model_definition, update_model_definition

logger = logging.getLogger(__name__)
app_label = 'test'
app_config = apps.get_app_config(app_label)


@api_view(['POST'])
def create_dynamic_model(request):
    try:
        serializer = DynamicModelSerializer(data=request.data)
        if serializer.is_valid():
            model_name = serializer.validated_data['model_name']
            fields = serializer.validated_data['fields']
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        attrs = {}
        for field_name, field_type in fields.items():
            attrs[field_name] = models.CharField(max_length=100)
            if field_type == 'number':
                attrs[field_name] = models.IntegerField()
            elif field_type == 'boolean':
                attrs[field_name] = models.BooleanField()
        model = register_dynamic_model(model_name, attrs)
        dynamic_model = apps.get_model(app_label, model_name)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)
            apps.register_model(app_label, dynamic_model)
            definition_id = create_model_definition(model_name, fields)
        return Response({'definition_id': definition_id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.exception(e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_dynamic_model(request, id):
    try:
        serializer = DynamicModelSerializer(data=request.data)
        if serializer.is_valid():
            model_name = serializer.validated_data['model_name']
            fields = serializer.validated_data['fields']
            dynamic_model = apps.get_model(app_label=app_label, model_name=model_name)
            with connection.schema_editor() as schema_editor:
                old_fields = dynamic_model._meta.get_fields()
                print(old_fields)
                for field in old_fields[2:]:
                    schema_editor.remove_field(model=dynamic_model, field=field)
                    delattr(dynamic_model, field.name)
                print(dynamic_model._meta.get_fields())
                attrs = {}
                for field_name, field_type in fields.items():
                    attrs[field_name] = models.CharField(max_length=100)
                    if field_type == 'number':
                        attrs[field_name] = models.IntegerField()
                    elif field_type == 'boolean':
                        attrs[field_name] = models.BooleanField()
                intermediary_model = register_dynamic_model('intermediary_model', attrs)
                for field in intermediary_model._meta.fields[2:]:
                    schema_editor.add_field(dynamic_model, field)
            apps.register_model(app_label, dynamic_model)
            apps.all_models[app_label][model_name] = dynamic_model
            definition_id = update_model_definition(model_name, id, fields)
            return Response({'model updated. definition_id': definition_id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_row(request, id):
    try:
        definition = get_object_or_404(DynamicModelDefinition, id=id)
        model_name = definition.name
        model = apps.get_model(app_label=app_label, model_name=model_name)
    except DynamicModelDefinition.DoesNotExist:
            return Response({'error': 'Invalid id'}, status=400)

    serializer = DynamicModelRowSerializer(data=request.data, model=model)
    if serializer.is_valid():
        row = model(**serializer.validated_data)
        row.full_clean()
        row.save()
        return Response({'success': True}, status=201)
    else:
        return Response(serializer.errors, status=400)



@api_view(['GET'])
def get_rows(request, id):
    try:
        definition = get_object_or_404(DynamicModelDefinition, id=id)
        model_name = definition.name
        model = apps.get_model(app_label=app_label, model_name=model_name)
    except DynamicModelDefinition.DoesNotExist:
        return Response({'error': 'Invalid id'}, status=400)
    rows = model.objects.all()
    serializer = DynamicModelRowSerializer(rows, many=True, model=model)
    row_dicts = [model_to_dict(row) for row in rows]
    json_data = json.dumps(row_dicts)
    response_data = {
        'count': len(serializer.data),
        'results': json_data,
    }
    if serializer.is_valid():
        return Response(response_data, status=200)
    else:
        return Response(serializer.errors, status=400)




