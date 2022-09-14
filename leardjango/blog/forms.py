from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from captcha.fields import CaptchaField
from django_ckeditor_5.widgets import CKEditor5Widget
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'user', 'post']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'class': 'form-control', 'placeholder': 'Write a comment...'}),
            'user': forms.HiddenInput(attrs={'id': 'user_id'}),
            'post': forms.HiddenInput(attrs={'id': 'post_id'})
        }


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Choose a category"

    class Meta:
        model = Post

        fields = ['title', 'slug', 'photo', 'content', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}),
            'cat': forms.Select(attrs={'required': 'true', 'class': 'form-select'}),
            'content': CKEditor5Widget(attrs={'class': "django_ckeditor_5"}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Title more than 200 sybmols')
        return title


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'photo', 'content', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(attrs={'required': 'true', 'class': "django_ckeditor_5"}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'required': 'true', 'class': 'form-select'})
        }


class RegistrationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    username = forms.CharField(label="Login", max_length=32, min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password", max_length=32, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Repeat password", max_length=32, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    full_name = forms.CharField(label="Full name", max_length=32, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2')


class PasswordsChangeForm(PopRequestMixin, PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                   label="Old password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                    label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                    label="Confirmation")


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Incorrect password or login"
    }
    username = forms.CharField(label="Login", min_length=3, max_length=32,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Password", min_length=3, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = forms.CharField(label="Name", max_length=32, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", required=True, validators=[EmailValidator],
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = Feedback


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser

        fields = ['username', 'email', 'full_name', 'about']

        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control'})
        }
