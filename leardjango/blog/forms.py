from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from captcha.fields import CaptchaField
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Choose a category"

    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post

        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'cat': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Title more than 200 sybmols')
        return title


class EditPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'slug', 'photo', 'content', 'is_published', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'class': 'form-select'})
        }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Login", max_length=32, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password", max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Repeat password", max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label="First name", max_length=32, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Last name", max_length=32, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", max_length=32, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Password", max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = forms.CharField(label="Name", max_length=32, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label="Email", required=True, validators=[EmailValidator],
                            widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = Feedback


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }


class PasswordsChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                   label="Old password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                    label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'type': 'password'}),
                                    label="Confirmation")
