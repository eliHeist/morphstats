from rest_framework import serializers

from Stat.models import Service, Stat


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    facilitators_count = serializers.SerializerMethodField()
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
            "facilitators_count",
        ]

    def get_facilitators_count(self, obj):
        return obj.facilitators_available.count()