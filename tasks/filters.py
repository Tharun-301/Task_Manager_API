import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.BooleanFilter(field_name='status')
    owner = django_filters.NumberFilter(field_name='owner__id')
    due_date_before = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    due_date_after = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['status', 'owner', 'due_date_before', 'due_date_after'] 