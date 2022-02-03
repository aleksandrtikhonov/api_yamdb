import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Кастомный фильтр для вьюсета 'Title'.
    """
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
