from django.db import models
from django.utils import timezone


class DynamicModel(models.Model):
    class Meta:
        app_label = 'test'

    # We override the __init__ method to allow creation of instances
    # with arbitrary keyword arguments.
    def __init__(self, *args, **kwargs):
        super(DynamicModel, self).__init__(*args, **kwargs)
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)

    # We override the __str__ method to return a string representation
    # of the model instance.
    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{attr}={value}" for attr, value in self.__dict__.items() if not attr.startswith("_"))})'

    # We define a subclass of DynamicModel using the type() function.
    # The subclass will have the fields specified in the fields argument,
    # which should be a dictionary mapping field names to field types.
    # The subclass will also have the name specified in the name argument.


def register_dynamic_model(name, fields):
    attrs = {field_name: fields[field_name] for field_name in fields}
    attrs['__module__'] = __name__
    print(attrs)
    return type(name, (DynamicModel,), attrs)


class DynamicModelDefinition(models.Model):
    name = models.CharField(max_length=255)
    definition = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
    changed_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name}"
