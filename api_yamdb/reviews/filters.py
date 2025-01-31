import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):

    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['genre__slug', 'category__slug', 'year', 'name']
