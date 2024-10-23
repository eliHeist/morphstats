from rest_framework import serializers

from Stat.models import Service, Stat


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "stat",
            "name",
            "junior",
            "senior",
            "first_time_visitors",
            "salvations",
            "facilitators",
            "non_system_facilitators",
            "facilitators_available",
        ]
