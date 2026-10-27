from functools import cache

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils.safestring import mark_safe

from art.models import Collection

register = template.Library()


@register.inclusion_tag("spirsa/tags/menu_link_tag.html")
def menu_link_tag(title, slug, path, dynamic=False):
    return {
        "title": title,
        "url": reverse(slug) if dynamic else f"/{slug}/",
        "current": slug in path,
    }


@register.inclusion_tag("spirsa/tags/navigation_tag.html", takes_context=True)
def navigation_tag(context, mobile=False):
    request = context.get("request")

    return {
        "mobile": mobile,
        "request_path": request.path,
        "collections": Collection.objects.for_navigation(),
    }


@cache
def _read_static(path):
    with open(finders.find(path), encoding="utf-8") as f:
        return f.read()


@register.simple_tag
def inline_css(path):
    css = _read_static.__wrapped__(path) if settings.DEBUG else _read_static(path)
    return mark_safe(f"<style>{css}</style>")
