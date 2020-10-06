HOME_URL_NAME = 'digital'
IMAGE_MAX_WIDTH = 5000
IMAGE_LARGE_WIDTH = 2500
IMAGE_MEDIUM_WIDTH = 1200
IMAGE_MIN_WIDTH = 500
IMAGE_QUALITY = 80
IMAGE_VARIATION_WIDTHS = [
    IMAGE_MIN_WIDTH,
    1000,
    IMAGE_MEDIUM_WIDTH,
    2400,
    IMAGE_LARGE_WIDTH,
    IMAGE_MAX_WIDTH
]
SRCSET_TYPE = [
    'webp_large', 'webp_medium', 'webp_small', 'jpeg_large', 'jpeg_medium', 'jpeg_small'
]
SRCSET_MAPPING = {srcset_type: [] for srcset_type in SRCSET_TYPE}
