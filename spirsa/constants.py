HOME_URL_NAME = ""

DEFAULT_TYPE = "jpeg"
LARGE = "large"
MEDIUM = "medium"
SMALL = "small"
THUMBNAIL = "thumbnail"
SMALL_WIDTH = 380
THUMBNAIL_WIDTH = 480
MEDIUM_WIDTH = SMALL_WIDTH * 2
LARGE_WIDTH = SMALL_WIDTH * 3
RATIO_THRESHOLD = 1.2
BASE_HEIGHT = 400

SRCSET_TYPES = (
    "webp",
    DEFAULT_TYPE,
)
SRCSET_MAPPING = {
    srcset: []
    for srcset in [
        f"{t}_{s}"
        for t in SRCSET_TYPES
        for s in (
            LARGE,
            MEDIUM,
            THUMBNAIL,
            SMALL,
        )
    ]
}
LANDSCAPE_VARIATION_SETS = (
    (LARGE, LARGE_WIDTH, LARGE_WIDTH * 2),
    (LARGE, LARGE_WIDTH, LARGE_WIDTH),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH * 2),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH * 2),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH),
)
SMALL_VARIATION_SETS = (
    (SMALL, SMALL_WIDTH, SMALL_WIDTH * 2),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH),
)
THUMBNAIL_VARIATION_SETS = (
    (THUMBNAIL, THUMBNAIL_WIDTH, THUMBNAIL_WIDTH * 2),
    (THUMBNAIL, THUMBNAIL_WIDTH, THUMBNAIL_WIDTH),
)
VARIATION_SETS = (
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH * 2),
    (MEDIUM, MEDIUM_WIDTH, MEDIUM_WIDTH),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH * 2),
    (SMALL, SMALL_WIDTH, SMALL_WIDTH),
)

FACEBOOK_SHARE_URL = "https://www.facebook.com/sharer.php?u="
LINKEDIN_SHARE_URL = "https://www.linkedin.com/sharing/share-offsite/?url="
PINTEREST_SHARE_URL = "https://pinterest.com/pin/create/button/?url="
REDDIT_SHARE_URL = "https://reddit.com/submit?url="
TWITTER_SHARE_URL = "https://twitter.com/intent/tweet?url="
