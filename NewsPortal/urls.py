from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),           # пути для новостей
    path('articles/', include('news.urls_articles')),  
    path('pages/', include('django.contrib.flatpages.urls')),
        path('', include('protect.urls')),          
    path('sign/', include('sign.urls')),        
    path('accounts/', include('allauth.urls')),
]