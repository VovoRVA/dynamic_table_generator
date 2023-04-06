from rest_framework import serializers

class DynamicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
