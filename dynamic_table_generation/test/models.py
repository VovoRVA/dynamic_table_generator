from django.db import models


class DynamicModel(models.Model):
    class Meta:
        app_label = 'test'

    def __init__(self, *args, **kwargs):
        super(DynamicModel, self).__init__(*args, **kwargs)
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)

    def __str__(self):
        return f"{self.pk} - {self.__class__.__name__}"