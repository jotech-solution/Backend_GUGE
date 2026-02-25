# filters.py
import django_filters
from .models import School


class SchoolFilter(django_filters.FilterSet):

    class Meta:
        model = School
        fields = {
            "province": ["exact"],
            "division": ["exact"],
            "sub_division": ["exact"],
            "city": ["exact"],
            "territory": ["exact"],
            "management_regime": ["exact"],
            "mechanized_status": ["exact"],
        }