# import django_filters
# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import FilterSet
# from reviews.models import Title
#
#
# class TitleFilter(FilterSet):
#     category_id__slug = django_filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = Title
#         fields = ()
#