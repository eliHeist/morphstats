import django_filters
from .models import Grade, Morpher

class MorpherFilter(django_filters.FilterSet):
    grade = django_filters.ModelMultipleChoiceFilter(queryset=Grade.objects.all().order_by('name'))

    candidates = django_filters.BooleanFilter(method='candidate_mtd', field_name='grade')

    def candidate_mtd(self, queryset):
        return queryset.filter(grade__is_candidate=True)
        
    class Meta:
        model = Morpher
        fields = ('grade', 'residence', 'school')