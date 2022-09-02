from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
from django.views.generic.edit import ProcessFormView

from .forms import *
from .utils import *


class AllPostsListView(DataMixin, ListView):
    model = Post
    title = 'All posts'
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-time_create')


class PostCategoryView(DataMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category: ' + c.name,
                                      cat_selected=c.slug)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat').order_by(
            "-time_create")


class PostView(DataMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPostView(LoginRequiredMixin, DataMixin, CreateView):
    title = 'Add post'
    form_class = AddPostForm
    template_name = "blog/add_post.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        post.save()
        return redirect('home')


class EditPostView(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = EditPostForm
    template_name = 'blog/edit_post.html'
    title = "Edit post"
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        return Post.objects.get(slug=self.kwargs['post_slug'])


class RegistrationView(DataMixin, CreateView):
    title = 'Sign Up'
    form_class = RegistrationForm
    template_name = 'blog/users/signup.html'
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class SingInView(DataMixin, LoginView):
    title = 'Sign In'
    form_class = LoginForm
    template_name = "blog/users/signin.html"

    def get_success_url(self):
        return reverse_lazy('home')


class FeedbackFormView(DataMixin, FormView):
    title = 'Feedback'
    form_class = FeedbackForm
    template_name = 'blog/feedback.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        data = form.cleaned_data
        feedback = Feedback(
            name=data['name'],
            email=data['email'],
            content=data['content']
        )
        feedback.save()
        return redirect('home')


class ProfileView(DataMixin, LoginRequiredMixin, UpdateView):
    title = 'Edit profile'
    form_class = UserEditForm
    template_name = 'blog/users/profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordsChangeView(DataMixin, PasswordChangeView):
    title = 'Change password'
    template_name = 'blog/users/change_password.html'
    form_class = PasswordsChangeForm
    success_url = reverse_lazy('pwd_change_success')


class AboutView(DataMixin, TemplateView):
    title = 'About this site'
    template_name = 'blog/about.html'


class Page404View(DataMixin, TemplateView):
    title = "404"
    template_name = "blog/404.html"


class PasswordChangeSuccess(DataMixin, TemplateView):
    title = 'Password change success'
    template_name = 'blog/users/password_change_success.html'


class SearchResultsView(DataMixin, ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        q = self.request.GET.get('search_request')
        return Post.objects.filter(Q(content__icontains=q) | Q(title__icontains=q))

    def get_user_context(self, **kwargs):
        context = super().get_user_context(**kwargs)
        search_req = self.request.GET.get('search_request')
        context['add_get'] = f"&search_request={search_req}"
        context['title'] = f"Search results for \"{search_req}\":"
        return context


def delete_post(request, post_slug):
    Post.objects.get(slug=post_slug).delete()
    return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('home')
