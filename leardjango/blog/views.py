from bootstrap_modal_forms.mixins import PassRequestMixin
from bootstrap_modal_forms.utils import is_ajax
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView
from django.views.generic.edit import FormMixin
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


class PostView(DataMixin, FormMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    form_class = CommentForm
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post', kwargs={'post_slug': self.object.slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print(form['user'])
        form.save()
        return super(PostView, self).form_valid(form)


class AddPostView(LoginRequiredMixin, DataMixin, SuccessMessageMixin, CreateView):
    title = 'Add post'
    form_class = AddPostForm
    template_name = "blog/add_post.html"
    success_url = reverse_lazy('home')
    success_message = 'You were successfully published new post.'

    def get_form_kwargs(self):
        kwargs = super(AddPostView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

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


class PasswordsChangeView(DataMixin, PassRequestMixin, PasswordChangeView):
    template_name = 'blog/users/change_password.html'
    form_class = PasswordsChangeForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not is_ajax(self.request.META):
            if form.is_valid():
                return super(PasswordsChangeView, self).post(request, *args, **kwargs)
            return HttpResponse(status=204)
        else:
            if form.is_valid():
                return HttpResponse(status=204)
            return super(PasswordsChangeView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        update_session_auth_hash(self.request, form.user)
        messages.add_message(self.request, messages.SUCCESS, "Password successfuly changed.")
        return redirect('profile')


class RegistrationView(DataMixin, BSModalCreateView):
    form_class = RegistrationForm
    template_name = 'blog/users/signup.html'
    success_message = 'You were successfully registered, now you can login'
    success_url = reverse_lazy('about')
    extra_context = {
        "icons": {
            "username": "fa-right-to-bracket",
            "full_name": "fa-user",
            "password1": "fa-lock",
            "password2": "fa-lock",
            "email": "fa-envelope"
        }
    }


class SingInView(BSModalLoginView):
    form_class = LoginForm
    template_name = "blog/users/signin.html"
    success_message = 'You were successfully logged in.'
    extra_context = {
        "icons": {
            "username": "fa-right-to-bracket",
            "password": "fa-lock",
        }
    }


class FeedbackFormView(DataMixin, FormView):
    title = 'Feedback'
    form_class = FeedbackForm
    template_name = 'blog/feedback.html'
    success_url = reverse_lazy('login')
    extra_context = {
        "icons": {
            "name": "fa-user",
            "email": "fa-envelope"
        }
    }

    def form_valid(self, form):
        data = form.cleaned_data
        feedback = Feedback(
            name=data['name'],
            email=data['email'],
            content=data['content']
        )
        feedback.save()
        return redirect('home')


class EditProfileView(DataMixin, LoginRequiredMixin, UpdateView):
    title = 'Edit profile'
    form_class = UserEditForm
    template_name = 'blog/users/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class WatchProfileView(DataMixin, UpdateView):
    title = 'Watch profile'
    context_object_name = 'profile'
    form_class = UserEditForm
    slug_url_kwarg = 'profile_slug'
    template_name = 'blog/users/watch_profile.html'

    def get_object(self, queryset=None):
        user = CustomUser.objects.get(username=self.kwargs['profile_slug'])
        return user


class AboutView(DataMixin, TemplateView):
    title = 'About this site'
    template_name = 'blog/about.html'


class Page404View(DataMixin, TemplateView):
    title = "404"
    template_name = "blog/404.html"


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
    post = Post.objects.get(slug=post_slug)
    title = post.title
    post.delete()
    messages.add_message(request, messages.WARNING, f'Post \"{title}\" deleted.')
    return redirect(request.META.get('HTTP_REFERER'))


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.WARNING, 'You have signed out.')
    return redirect(request.META.get('HTTP_REFERER'))


def reaction(request, post_slug):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, "Login to like or dislike.")
        return redirect(request.META.get('HTTP_REFERER'))

    if act := request.GET.get('act'):
        post = Post.objects.get(slug=post_slug)
        try:
            if react := post.post_reactions.through.objects.get(post=post, user=request.user):
                react.delete()
        except:
            react = None

        if not react or react.react_type != act:
            post.post_reactions.through.objects.create(user=request.user, react_type=act, post=post)

    return redirect(request.META.get('HTTP_REFERER'))