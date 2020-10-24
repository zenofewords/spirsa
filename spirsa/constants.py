CACHE_SECONDS = 600
HOME_URL_NAME = 'digital'

DEFAULT_QUALITY = 75
DEFAULT_TYPE = 'jpeg'
LARGE = 'large'
MEDIUM = 'medium'
SMALL = 'small'
SMALL_WIDTH = 380
MEDIUM_WIDTH = SMALL_WIDTH * 2
LARGE_WIDTH = SMALL_WIDTH * 3
DEFAULT_WIDTH = MEDIUM_WIDTH
RATIO_THRESHOLD = 1.2
BASE_HEIGHT = 400

SRCSET_TYPES = ('webp', DEFAULT_TYPE, )
SRCSET_MAPPING = {srcset: [] for srcset in [
    '{}_{}'.format(t, s) for t in SRCSET_TYPES for s in (LARGE, MEDIUM, SMALL, )]
}
VARIATION_SETS = (
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH * 2),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH * 2),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH),
)
LANDSCAPE_VARIATION_SETS = (
    (LARGE, LARGE_WIDTH, LARGE_WIDTH * 2),
    (LARGE, LARGE_WIDTH, LARGE_WIDTH),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH * 2),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH * 2),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH),
)

FB_SHARE_URL = 'https://www.facebook.com/sharer.php?%3D'
TT_SHARE_URL = 'https://twitter.com/intent/tweet?url%3D'
IN_SHARE_URL = 'https://www.linkedin.com/sharing/share-offsite/?url%3D'
PT_SHARE_URL = 'https://pinterest.com/pin/create/button/?url%3D'
