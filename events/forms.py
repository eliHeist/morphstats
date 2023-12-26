from django import forms

from events.models import Event

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.SelectDateWidget()
        }

