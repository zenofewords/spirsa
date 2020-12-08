from django.views.decorators.cache import cache_page
from django.urls import path

from art.views import (
    ArtworkDetailView,
    ArtworkListView,
    ArtworkTraditionalListView,
    ArtworkDetailPreView,
    ArtworkListPreView,
    ArtworkTraditionalListPreView,
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
        cache_page(CACHE_SECONDS)(ArtworkTraditionalListView.as_view()),
        name='traditional'
    ),
    path(
        'artwork/<slug:slug>/',
        cache_page(CACHE_SECONDS)(ArtworkDetailView.as_view()),
        name='artwork-detail'
    ),
    path(
        'preview/',
        cache_page(CACHE_SECONDS)(ArtworkListPreView.as_view()),
        name='{}-preview'.format(HOME_URL_NAME)
    ),
    path(
        'traditional/preview/',
        cache_page(CACHE_SECONDS)(ArtworkTraditionalListPreView.as_view()),
        name='traditional-preview'
    ),
    path(
        'artwork/<slug:slug>/preview/',
        cache_page(CACHE_SECONDS)(ArtworkDetailPreView.as_view()),
        name='artwork-detail-preview'
    ),
]
