from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', AllPostsListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('login/', SingInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>', PostView.as_view(), name='post'),
    path('post/edit/<slug:post_slug>', EditPostView.as_view(), name='edit_post'),
    path('post/delete/<slug:post_slug>', delete_post, name='delete_post'),
    path('category/<slug:cat_slug>', PostCategoryView.as_view(), name='category'),
    path('registration/', RegistrationView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
    path('profile/change_password', PasswordsChangeView.as_view(), name='pwd_change'),
    path('profile/change_password_success', PasswordChangeSuccess.as_view(), name='pwd_change_success')
]
