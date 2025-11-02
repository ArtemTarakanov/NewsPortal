from django import forms
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post

class PostFilter(FilterSet):
    # Поиск по названию
    title = CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        label='Название содержит'
    )
    
    # Поиск по автору
    author__user__username = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains', 
        label='Имя автора содержит'
    )
    
    # Фильтр по дате (позже указанной даты) с календарем
    date_creation__gt = DateFilter(
        field_name='date_creation',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []  # Указываем пустой список, т.к. поля уже объявлены выше