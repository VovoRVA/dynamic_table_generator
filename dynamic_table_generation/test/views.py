import logging
from .models import models
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_dynamic_model(request):
    try:
        data = request.data
        model_name = data['model_name']
        fields = data['fields']
        attrs = {}
        for field_name, field_type in fields.items():
            attrs[field_name] = models.CharField(max_length=100)
            if field_type == 'number':
                attrs[field_name] = models.IntegerField()
            elif field_type == 'boolean':
                attrs[field_name] = models.BooleanField()
        attrs['__module__'] = __name__
        model = type(model_name, (models.Model,), attrs)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)

        return Response(status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.exception(e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
