from rest_framework.serializers import ModelSerializer

from facilitators.models import Facilitator, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FacilitatorSerializer(ModelSerializer):
    class Meta:
        model = Facilitator
        fields = '__all__'