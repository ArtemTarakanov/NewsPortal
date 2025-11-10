from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, NewsSearch,
    ArticleCreate, ArticleUpdate, ArticleDelete, register
)
from django.urls import path
from .views import subscribe, unsubscribe

urlpatterns = [
    # Новости
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),  
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),

    
    # Статьи
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    
    # Авторизация
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),

    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe, name='unsubscribe'),

    
]
