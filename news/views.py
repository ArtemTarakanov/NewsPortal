from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  
from django.urls import reverse_lazy  
from .models import Post
from .filters import PostFilter  
from .forms import PostForm

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

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        form.save_m2m()  
        return super().form_valid(form)

class NewsUpdate(UpdateView):
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
    template_name = 'news_search.html'  # отдельный шаблон для поиска
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
    
# Классы для статей
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'  # автоматически ставим тип "Статья"
        post.save()
        form.save_m2m()  
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
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