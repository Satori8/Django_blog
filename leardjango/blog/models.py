from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="Full name")
    about = models.CharField(max_length=1000, verbose_name="About")
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    content = models.TextField(max_length=10000, default='')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="Publish")
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Category")
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.deletion.SET_NULL)
    post_reactions = models.ManyToManyField(CustomUser,
                                            through="Reaction",
                                            through_fields=('post', 'user'),
                                            blank=True, related_name="reactions")

    def is_reactioned(self, user, reaction_type='any'):
        if reaction_type == 'any':
            return self.post_reactions.through.objects.filter(post=self, user=user).exists()
        else:
            return self.post_reactions.through.objects.filter(post=self, user=user, react_type=reaction_type).exists()

    def get_reaction_count(self, reaction_type):
        return self.post_reactions.through.objects.filter(post=self, react_type=reaction_type).count()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['time_create']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.deletion.SET_NULL)
    text = models.CharField(max_length=1000, blank=False, null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, blank=True, related_name="comments", on_delete=models.deletion.CASCADE)


class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.deletion.SET_NULL)
    post = models.ForeignKey(Post, null=False, on_delete=models.deletion.CASCADE)
    react_type = models.CharField(blank=False, max_length=10, choices=[
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    ])


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
