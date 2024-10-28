from django.db.models import When, Case, Value, IntegerField, Q
from django_filters import (
    CharFilter,
    FilterSet,
    DateFromToRangeFilter
)
from rest_framework.exceptions import APIException

from apps.blogs.models import Post


class FilterException(APIException):
    status_code = 400
    default_detail = 'Uncorrected filter data'
    default_code = 'uncorrected_filter_data'


class PostFilter(FilterSet):
    search = CharFilter(method="filter_search")
    updated_at = DateFromToRangeFilter()

    @staticmethod
    def filter_search(queryset, name, value):
        queryset = queryset.annotate(
            weight=Case(
                When(title__icontains=value, then=Value(3)),
                When(content__icontains=value, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        ).order_by('-weight')

        return queryset

    class Meta:
        model = Post
        fields = ['updated_at']
