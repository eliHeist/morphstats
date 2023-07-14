from rest_framework import serializers

from Stat.models import Service, Stat


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'