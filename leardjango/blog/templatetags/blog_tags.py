from django import template
#from blog.models import *

from blog.models import Category

register = template.Library()


@register.simple_tag()
def get_categories(filter=None):
    if filter:
        return Category.objects(pk=filter)
    else:
        return Category.objects.all()


@register.inclusion_tag('templates/base/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}
