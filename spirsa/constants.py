HOME_URL_NAME = 'digital'
DEFAULT_QUALITY = 75
DEFAULT_SIZE = 2400
DEFAULT_TYPE = 'jpeg'
LARGE = 'large'
MEDIUM = 'medium'
SMALL = 'small'
SRCSET_TYPES = ('webp', DEFAULT_TYPE, )
SRCSET_MAPPING = {srcset: [] for srcset in [
    '{}_{}'.format(t, s) for t in SRCSET_TYPES for s in (LARGE, MEDIUM, SMALL, )]
}
VARIATION_SETS = (
    (LARGE, 2500, 5000),
    (LARGE, 2500, 2500),
    (MEDIUM, 1200, DEFAULT_SIZE),
    (MEDIUM, 1200, 1200),
    (SMALL, 500, 1000),
    (SMALL, 500, 500),
)
