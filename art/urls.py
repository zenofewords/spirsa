from django.urls import path

from art.views import (
    AsyncArtworkListView,
    AsyncArtworkTraditionalListView,
    ArtworkDetailView,
    ArtworkListView,
    ArtworkTraditionalListView,
    ArtworkDetailPreView,
    ArtworkListPreView,
    ArtworkTraditionalListPreView,
)
from spirsa.constants import (
    HOME_URL_NAME,
)


urlpatterns = [
    path('', ArtworkListView.as_view(), name=HOME_URL_NAME),
    path('traditional/', ArtworkTraditionalListView.as_view(), name='traditional'),
    path('artwork/<slug:slug>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('preview/', ArtworkListPreView.as_view(), name='{}-preview'.format(HOME_URL_NAME)),
    path(
        'traditional/preview/', ArtworkTraditionalListPreView.as_view(),
        name='traditional-preview'
    ),
    path(
        'artwork/<slug:slug>/preview/', ArtworkDetailPreView.as_view(),
        name='artwork-detail-preview'
    ),
    path(
        'async-artworks', AsyncArtworkListView.as_view(),
        name='async-artwork-list'
    ),
    path(
        'traditional/async-artworks', AsyncArtworkTraditionalListView.as_view(),
        name='async-artwork-traditional-list'
    ),
]
