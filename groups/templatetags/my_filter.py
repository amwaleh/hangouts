#https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='multiply')
def multiply (value, arg):
    content_per_page = settings.GROUPS_PER_PAGE
    return ((value-1) * content_per_page) + arg

@register.filter(name="split")
def comma_split(value):
    if value:
        words = value.split(",")
        return words

