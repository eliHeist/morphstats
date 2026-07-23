from django.forms import ModelForm, CharField, ModelMultipleChoiceField

from facilitators.models import Facilitator, Tag


class FacilitatorFormOld(ModelForm):
    class Meta:
        model = Facilitator
        fields = '__all__'


class TagNameMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('to_field_name', 'name')
        super().__init__(*args, **kwargs)
        # self.label_from_instance = lambda obj: obj.name

    # def _get_choices(self):
    #     return [(obj.name, obj.name) for obj in self.queryset]

    # choices = property(_get_choices)

    # def clean(self, value):
    #     if not value:
    #         return self.queryset.none()
    #     return self.queryset.filter(name__in=value)


class FacilitatorForm(ModelForm):
    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
    other_name = CharField(max_length=50, required=False)

    tags = TagNameMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Facilitator
        fields = ['first_name', 'last_name', 'other_name', 'active', 'gender', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Parse name field logic
        if self.instance.pk and getattr(self.instance, 'name', None):
            parts = self.instance.name.split()
            if len(parts) == 0:
                first = last = other = ''
            elif len(parts) == 1:
                first, last, other = parts[0], '', ''
            else:
                first = parts[0]
                last = parts[-1]
                other = ' '.join(parts[1:-1])

            self.fields['first_name'].initial = first
            self.fields['last_name'].initial = last
            self.fields['other_name'].initial = other

        # 2. Fix tags initial values (Force Tag Names instead of Tag IDs)
        if self.instance.pk:
            self.fields['tags'].initial = list(
                self.instance.tags.values_list('name', flat=True)
            )

    def clean(self):
        cleaned = super().clean()

        first = (cleaned.get('first_name') or '').strip()
        last = (cleaned.get('last_name') or '').strip()
        other = (cleaned.get('other_name') or '').strip()

        if not first and not last:
            from django.core.exceptions import ValidationError
            raise ValidationError('Enter at least a first or last name.')

        parts = [p for p in (first, other, last) if p]
        cleaned['name'] = ' '.join(parts)

        return cleaned

    def save(self, commit=True):
        self.instance.name = self.cleaned_data['name']
        return super().save(commit=commit)
