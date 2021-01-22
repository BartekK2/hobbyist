import django_filters
from .models import Post
from django import forms
from .forms import choice_list


class DateInput(forms.DateInput):
    input_type = 'date'

class PostFilter(django_filters.FilterSet):
    od = django_filters.DateFilter(field_name="data", lookup_expr='gte', label=('Data od'),
        widget=DateInput())
    do = django_filters.DateFilter(field_name="data", lookup_expr='lte', label=('Do'),
        widget=DateInput())
    kategoria = django_filters.ChoiceFilter(field_name="category", choices=choice_list, label=('Kategoria'))
    miejscowosc = django_filters.CharFilter(field_name="city", label=("Miasto"), max_length=100)
    class Meta:
        model = Post
        fields = []
