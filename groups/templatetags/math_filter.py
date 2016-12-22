#https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply (value,arg):
    # need to adjust the content_per_page to be dynamic
    content_per_page = 6
    return ((value-1) * content_per_page) + arg
