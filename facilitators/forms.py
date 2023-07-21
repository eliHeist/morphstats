from django.forms import ModelForm

from facilitators.models import Facilitator

class FacilitatorForm(ModelForm):
    class Meta:
        model = Facilitator
        fields = '__all__'
