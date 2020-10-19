HOME_URL_NAME = 'digital'

DEFAULT_QUALITY = 75
DEFAULT_SIZE = 1000
DEFAULT_TYPE = 'jpeg'
LARGE = 'large'
MEDIUM = 'medium'
SMALL = 'small'
SRCSET_TYPES = ('webp', DEFAULT_TYPE, )
SRCSET_MAPPING = {srcset: [] for srcset in [
    '{}_{}'.format(t, s) for t in SRCSET_TYPES for s in (LARGE, MEDIUM, SMALL, )]
}
VARIATION_SETS = (
    (LARGE, 1400, 2800),
    (LARGE, 1400, 1400),
    (MEDIUM, 800, 1600),
    (MEDIUM, 800, 800),
    (SMALL, 500, DEFAULT_SIZE),
    (SMALL, 500, 500),
)

FB_SHARE_URL = 'https://www.facebook.com/sharer.php?u='
TT_SHARE_URL = 'https://twitter.com/intent/tweet?url='
IN_SHARE_URL = 'https://www.linkedin.com/sharing/share-offsite/?url='
PT_SHARE_URL = 'https://pinterest.com/pin/create/button/?url='
