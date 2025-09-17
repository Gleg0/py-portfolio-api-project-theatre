import django_filters
from theatre.models import Performance, Play


class PerformanceFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="show_time")
    play_title = django_filters.CharFilter(field_name="play__title", lookup_expr="icontains")
    genre = django_filters.CharFilter(field_name="play__genres__name", lookup_expr="icontains")
    actor = django_filters.CharFilter(field_name="play__actors__last_name", lookup_expr="icontains")

    class Meta:
        model = Performance
        fields = ["date", "play_title", "genre", "actor"]

class PlayFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    genre = django_filters.CharFilter(field_name="genres__name", lookup_expr="icontains")
    actor = django_filters.CharFilter(field_name="actors__last_name", lookup_expr="icontains")

    class Meta:
        model = Play
        fields = ["title", "genre", "actor"]