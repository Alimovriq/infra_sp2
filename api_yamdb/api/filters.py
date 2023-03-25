from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """Требуется для фильтрации строк у Title: name, category, genre."""

    pass


class TitleFilter(filters.FilterSet):
    """
    Позволяет фильтровать данные по указанным строкам у произведений.
    """

    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug')
    genre = CharFilterInFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
