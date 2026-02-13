from django import template

from spirsa.constants import (
    FACEBOOK_SHARE_URL,
    LINKEDIN_SHARE_URL,
    PINTEREST_SHARE_URL,
    REDDIT_SHARE_URL,
    TWITTER_SHARE_URL,
)
from spirsa.utils import (
    get_artwork_navigation_urls,
    get_full_size_image,
    get_site_url,
)

register = template.Library()


@register.inclusion_tag("art/tags/artwork_tag.html", takes_context=True)
def artwork_tag(context, obj, detail=False, is_lcp=False):
    request = context.get("request")
    params = request.path.split("/")
    slug = params[1] if len(params) > 1 and params[1] != "" else "featured"
    object_url = f"{get_site_url(request)}{obj.get_absolute_url(slug)}"

    data = {
        "artwork": obj,
        "facebook_share_url": f"{FACEBOOK_SHARE_URL}{object_url}",
        "linkedin_share_url": f"{LINKEDIN_SHARE_URL}{object_url}",
        "pinterest_share_url": f"{PINTEREST_SHARE_URL}{object_url}",
        "reddit_share_url": f"{REDDIT_SHARE_URL}{object_url}",
        "twitter_share_url": f"{TWITTER_SHARE_URL}{object_url}",
        "detail": detail,
        "is_lcp": is_lcp or detail,
        "slug": slug,
        "preview": "preview" in request.GET,
    }
    if obj.srcsets:
        data.update(**{key: ", ".join(srcsets) for key, srcsets in obj.srcsets.items()})
        data.update(get_full_size_image(obj.srcsets))

    if detail:
        data = get_artwork_navigation_urls(data, slug, obj)
    return data


@register.inclusion_tag("art/tags/artwork_picture_tag.html")
def artwork_picture_tag(obj):
    data = {
        "artwork": obj,
        "decoding": "async",
    }
    if obj.srcsets:
        data.update(**{key: ", ".join(srcsets) for key, srcsets in obj.srcsets.items()})

    return data
