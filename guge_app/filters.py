# filters.py
import django_filters
from .models import School


class SchoolFilter(django_filters.FilterSet):

    province = django_filters.NumberFilter(field_name="province__id")
    division = django_filters.NumberFilter(field_name="division__id")
    sub_division = django_filters.NumberFilter(field_name="sub_division__id")
    city = django_filters.NumberFilter(field_name="city__id")
    territory = django_filters.NumberFilter(field_name="territory__id")

    class Meta:
        model = School
        fields = []