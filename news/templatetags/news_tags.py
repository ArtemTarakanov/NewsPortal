from datetime import datetime
from django import template

register = template.Library()

@register.simple_tag()
def current_time(format_string='%d.%m.%Y'):
    
    return datetime.utcnow().strftime(format_string)

@register.simple_tag()
def news_stats():
    """Показывает статистику по новостям"""
    from ..models import Post  
    
    total = Post.objects.count()
    articles = Post.objects.filter(category_type='AR').count()
    news_count = Post.objects.filter(category_type='NW').count()
    
    return f"📊 Статистика: {total} записей ({articles} статей, {news_count} новостей)"