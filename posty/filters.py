import django_filters
from .models import Post
from django import forms
from .forms import choice_list


class DateInput(forms.DateInput):
    input_type = 'date'

class PostFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="data", lookup_expr='gte', label=('Data od'),
        widget=DateInput())
    end_date = django_filters.DateFilter(field_name="data", lookup_expr='lte', label=('Do'),
        widget=DateInput())
    category = django_filters.ChoiceFilter(choices=choice_list, label=('Kategoria'))
    city = django_filters.CharFilter(label=("Miasto: "))
    class Meta:
        model = Post
        fields = []
