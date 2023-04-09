from rest_framework import serializers
from django.core import validators
from django.core.exceptions import ValidationError

import json


from .models import DynamicModel, DynamicModelDefinition


class DynamicModelSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    fields = serializers.DictField(
        child=serializers.ChoiceField(choices=['string', 'number', 'boolean'])
    )

    def validate_model_name(self, value):
        if not value.isidentifier():
            raise serializers.ValidationError('Invalid model name')
        return value

    def validate_fields(self, value):
        for field_name, field_type in value.items():
            if not field_name.isidentifier():
                raise serializers.ValidationError(f'Invalid field name: {field_name}')
        return value


class DynamicModelRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        if model is not None:
            self.Meta.model = model
            fields = [field.name for field in model._meta.fields]
            self.Meta.fields = fields
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError('Data must be a dictionary.')
        return data
