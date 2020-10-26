from django import template

from spirsa.constants import (
    FACEBOOK_SHARE_URL,
    LINKEDIN_SHARE_URL,
    PINTEREST_SHARE_URL,
    TWITTER_SHARE_URL,
)
from spirsa.utils import (
    get_site_url,
    get_artwork_navigation_urls,
)

register = template.Library()


@register.inclusion_tag('art/tags/artwork_tag.html', takes_context=True)
def artwork_tag(context, obj, decoding=None, detail=False):
    request = context.get('request')
    site_url = get_site_url(request)

    data = {
        'artwork': obj,
        'facebook_share_url': '{}{}{}'.format(
            FACEBOOK_SHARE_URL, site_url, obj.get_absolute_url()
        ),
        'twitter_share_url': '{}{}{}'.format(
            TWITTER_SHARE_URL, site_url, obj.get_absolute_url()
        ),
        'linkedin_share_url': '{}{}{}'.format(
            LINKEDIN_SHARE_URL, site_url, obj.get_absolute_url()
        ),
        'pinterest_share_url': '{}{}{}'.format(
            PINTEREST_SHARE_URL, site_url, obj.get_absolute_url()
        ),
        'decoding': decoding,
        'detail': detail,
    }
    if obj.srcsets:
        data.update(**{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()})

    if detail:
        data = get_artwork_navigation_urls(data, obj)
    return data
