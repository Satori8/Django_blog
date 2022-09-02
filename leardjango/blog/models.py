from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    content = models.TextField(max_length=10000, default='')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="Publish")
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Category")
    author = models.ForeignKey(User, null=True, on_delete=models.deletion.SET_NULL)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['time_create']

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    content = models.TextField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True)
