from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import DynamicModelDefinition
from .serializers import DynamicModelSerializer, DynamicModelRowSerializer


class CreateDynamicModelTestCase(APITestCase):
    def test_create_dynamic_model(self):
        url = reverse('create_dynamic_model')
        data = {
            'model_name': 'TestModel',
            'fields': {
                'field1': 'text',
                'field2': 'number',
                'field3': 'boolean'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('definition_id', response.data)

    def test_create_dynamic_model_with_invalid_data(self):
        url = reverse('create_dynamic_model')
        data = {
            'model_name': 'TestModel',
            'fields': {
                'field1': 'text',
                'field2': 'invalid_field_type',
                'field3': 'boolean'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateDynamicModelTestCase(APITestCase):
    def setUp(self):
        self.definition = DynamicModelDefinition.objects.create(
            name='TestModel',
            fields={
                'field1': 'text',
                'field2': 'number',
                'field3': 'boolean'
            }
        )

    def test_update_dynamic_model(self):
        url = reverse('update_dynamic_model', args=[self.definition.id])
        data = {
            'model_name': 'TestModel',
            'fields': {
                'field1': 'text',
                'field2': 'number',
                'field3': 'boolean',
                'field4': 'text'
            }
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('definition_id', response.data)

    def test_update_dynamic_model_with_invalid_data(self):
        url = reverse('update_dynamic_model', args=[self.definition.id])
        data = {
            'model_name': 'TestModel',
            'fields': {
                'field1': 'text',
                'field2': 'invalid_field_type',
                'field3': 'boolean',
                'field4': 'text'
            }
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.definition.delete()


class CreateRowTestCase(APITestCase):
    def setUp(self):
        self.definition = DynamicModelDefinition.objects.create(
            name='TestModel',
            fields={
                'field1': 'text',
                'field2': 'number',
                'field3': 'boolean'
            }
        )

    def test_create_row(self):
        url = reverse('create_row', args=[self.definition.id])
        data = {
            'field1': 'some text',
            'field2': 123,
            'field3': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_row_with_invalid_data(self):
        url = reverse('create_row', args=[self.definition.id])
        data = {
            'field1': 'some text',
            'field2': 'invalid_field_type',
            'field3': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
