from rest_framework import serializers

from Stat.models import Service, Stat
from facilitators.models import Facilitator


class StatSerializer(serializers.ModelSerializer):
    total_attendance = serializers.SerializerMethodField()
    total_junior = serializers.SerializerMethodField()
    total_senior = serializers.SerializerMethodField()
    total_salvations = serializers.SerializerMethodField()
    total_visitors = serializers.SerializerMethodField()
    facilitators_count = serializers.SerializerMethodField()
    total_that_served = serializers.SerializerMethodField()

    class Meta:
        model = Stat
        fields = '__all__'

    def get_total_attendance(self, obj):
        return obj.totalAttendance()

    def get_total_junior(self, obj):
        return obj.totalJunior()

    def get_total_senior(self, obj):
        return obj.totalSenior()

    def get_total_salvations(self, obj):
        return obj.totalSalvations()

    def get_total_visitors(self, obj):
        return obj.totalVisitors()

    def get_facilitators_count(self, obj):
        return obj.facilitatorsCount()

    def get_total_that_served(self, obj):
        return obj.total_that_served()


class FacilitatorsAvailableField(serializers.PrimaryKeyRelatedField):
    """
    Accepts facilitator primary keys (strings or ints) and 
    returns a list of string IDs during serialization.
    """
    def __init__(self, **kwargs):
        kwargs["queryset"] = Facilitator.objects.all()
        super().__init__(**kwargs)

    def to_representation(self, value):
        # DRF passes a SINGLE Facilitator instance here when many=True is set on the serializer field
        return str(value.pk)
    

class ServiceSerializer(serializers.ModelSerializer):
    facilitators_available = FacilitatorsAvailableField(many=True)

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
            "fixed_total",
        ]
