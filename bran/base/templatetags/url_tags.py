from django import template

register = template.Library()


@register.simple_tag
def active(request, *path):
    if request.resolver_match.view_name.startswith(tuple(path)):
        return 'active'

    return ''
