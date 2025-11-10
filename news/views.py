from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  
from django.urls import reverse_lazy  
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Post
from .filters import PostFilter  
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Category


class NewsList(ListView):
    model = Post                    
    ordering = '-date_creation'     
    template_name = 'news.html'     
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)  
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    
    def get_form_kwargs(self):
        """Передаем пользователя в форму для проверки лимита постов"""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        post.save()
        form.save_m2m()  
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        form.save_m2m()
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class NewsSearch(ListView):
    model = Post
    ordering = '-date_creation'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)  
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    
    def get_form_kwargs(self):
        """Передаем пользователя в форму для проверки лимита постов"""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        post.category_type = 'AR'
        post.save()
        form.save_m2m()  
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        form.save_m2m()
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('news_list')


@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    return redirect('news_list')