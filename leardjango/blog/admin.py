from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.models import User
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    # list_display = ('id', 'title', 'time_create', 'photo', 'is_published', 'cat', 'author')
    # list_editable = ('is_published',)
    # list_display_links = ('id', 'title', 'author')
    # list_filter = ('is_published', 'time_create', 'cat', 'author')
    # search_fields = ('title', 'content', 'author')
    # prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'time_create')
    list_display_links = ('id', 'name', 'email', 'time_create')
    search_fields = ('name', 'email', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
