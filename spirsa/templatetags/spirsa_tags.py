from django import template
from django.urls import reverse

from art.models import Collection

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(title, slug, path, dynamic=False):
    return {
        'title': title,
        'url': reverse(slug) if dynamic else '/{}'.format(slug),
        'current': slug in path,
    }


@register.inclusion_tag('spirsa/tags/navigation_tag.html', takes_context=True)
def navigation_tag(context, mobile=False):
    request = context.get('request')

    return {
        'mobile': mobile,
        'request_path': request.path,
        'collections': Collection.objects.for_navigation()
    }
