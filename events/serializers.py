from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_ongoing(self, obj):
        return obj.isOngoing()
