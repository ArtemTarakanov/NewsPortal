from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse  


class Author(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        
        posts_rating = self.post_set.aggregate(Sum('rating'))['rating__sum'] or 0
        posts_rating *= 3
        
        
        comments_rating = self.user.comment_set.aggregate(Sum('rating'))['rating__sum'] or 0
        
        
        posts_comments_rating = Comment.objects.filter(
            post__author=self
        ).aggregate(Sum('rating'))['rating__sum'] or 0
        
        
        self.rating = posts_rating + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return f"Author: {self.user.username}"


class Category(models.Model):
    
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    categories = models.ManyToManyField(Category, through='PostCategory')
    
    title = models.CharField(max_length=128)
    
    text = models.TextField()
    
    rating = models.SmallIntegerField(default=0)

    def like(self):
        
        self.rating += 1
        self.save()

    def dislike(self):
        
        self.rating -= 1
        self.save()

    def preview(self):
        
        return self.text[:124] + '...'

    def __str__(self):
        return f"{self.title}: {self.preview()}"
    
  
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"


class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    text = models.TextField()
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    rating = models.SmallIntegerField(default=0)

    def like(self):
        
        self.rating += 1
        self.save()

    def dislike(self):
        
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"