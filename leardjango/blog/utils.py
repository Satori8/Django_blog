from django.core.cache import cache
from django.db.models import Count
from django.views.generic.base import ContextMixin

from .models import *

menu = [
    {'title': 'Home', 'url_name': 'home'},
    {'title': 'Add post', 'url_name': 'add_post'},
    {'title': 'Feedback', 'url_name': 'feedback'},
    {'title': 'About', 'url_name': 'about'},
]


class DataMixin(ContextMixin):
    paginate_by = 5
    title = ''

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('post'))
        user_menu = menu.copy()

        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs, title=self.title)
        return dict(list(context.items()) + list(c_def.items()))
