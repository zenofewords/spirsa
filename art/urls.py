from django.views.decorators.cache import cache_page
from django.urls import path

from art.views import (
    ArtworkDetailView,
    ArtworkListView,
    ArtworTraditionalkListView,
)
from spirsa.constants import (
    CACHE_SECONDS,
    HOME_URL_NAME,
)


urlpatterns = [
    path(
        '',
        cache_page(CACHE_SECONDS)(ArtworkListView.as_view()),
        name=HOME_URL_NAME
    ),
    path(
        'traditional/',
        cache_page(CACHE_SECONDS)(ArtworTraditionalkListView.as_view()),
        name='traditional'
    ),
    path(
        'artwork/<slug:slug>/',
        cache_page(CACHE_SECONDS)(ArtworkDetailView.as_view()),
        name='artwork-detail'
    ),
]
