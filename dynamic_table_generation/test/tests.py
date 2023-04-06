from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DynamicModelTests(APITestCase):
    def test_create_dynamic_model(self):
        url = reverse('create-dynamic-model')
        data = {
            "name": "MyModel",
            "fields": [
                {"name": "name", "type": "CharField", "max_length": 50},
                {"name": "age", "type": "IntegerField"},
                {"name": "is_active", "type": "BooleanField"}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Model MyModel created successfully'})

        # Test duplicate model name
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Model with name MyModel already exists'})
