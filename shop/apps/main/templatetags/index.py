from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable.index(str(i))


@register.filter
def remove(indexable, i):
    return indexable.remove(str(i))
