from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text', 
            'category_type',
            'categories',
            'author',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Заголовок должен содержать минимум 5 символов")
        if len(title) > 128:
            raise ValidationError("Заголовок не может превышать 128 символов")
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 20:
            raise ValidationError("Текст должен содержать минимум 20 символов")
        return text

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        
        # Проверка, что заголовок не совпадает с текстом
        if title and text and title.lower() == text.lower()[:len(title)]:
            raise ValidationError({
                'title': "Заголовок не должен совпадать с началом текста"
            })
        
        return cleaned_data