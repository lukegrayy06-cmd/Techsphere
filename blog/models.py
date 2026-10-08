import math
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    content = RichTextField()  # <-- Updated to CKEditor field
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Like System Field
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    def total_likes(self):
        return self.likes.count()

    def reading_time(self):
        # Quick estimate: 200 words per minute
        words = len(self.content.split())
        return max(1, round(words / 200))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        words_per_minute = 200
        words = len(self.content.split()) if self.content else 0
        minutes = math.ceil(words / words_per_minute)
        return max(1, minutes)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.name or self.author} on {self.article}"