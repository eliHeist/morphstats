from rest_framework.serializers import ModelSerializer

from facilitators.models import Facilitator

class FacilitatorSerializer(ModelSerializer):
    class Meta:
        model = Facilitator
        fields = '__all__'