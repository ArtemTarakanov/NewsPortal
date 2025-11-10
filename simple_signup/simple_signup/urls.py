from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('protect.urls')),      # главная страница
    path('sign/', include('sign.urls')),    # всё, что начинается с /sign/
    path('accounts/', include('allauth.urls')), 
]
