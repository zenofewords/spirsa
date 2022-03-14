from django.urls import path

from art.views import (
    AsyncArtworkListView,
    AsyncArtworkDigitalListView,
    AsyncArtworkTraditionalListView,
    ArtworkDetailView,
    ArtworkDigitalListView,
    ArtworkListView,
    ArtworkTraditionalListView,
    ArtworkDetailPreview,
    ArtworkListPreview,
    ArtworkTraditionalListPreview,
)
from spirsa.constants import (
    HOME_URL_NAME,
)


urlpatterns = [
    path('', ArtworkListView.as_view(), name=HOME_URL_NAME),
    path('digital/', ArtworkDigitalListView.as_view(), name='digital'),
    path('traditional/', ArtworkTraditionalListView.as_view(), name='traditional'),
    path('artwork/<slug:slug>', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('preview/', ArtworkListPreview.as_view(), name='{}-preview'.format(HOME_URL_NAME)),
    path(
        'traditional/preview/', ArtworkTraditionalListPreview.as_view(),
        name='traditional-preview'
    ),
    path(
        'artwork/<slug:slug>/preview/', ArtworkDetailPreview.as_view(),
        name='artwork-detail-preview'
    ),
    path(
        'async-artworks', AsyncArtworkListView.as_view(),
        name='async-artwork-list'
    ),
    path(
        'digital/async-artworks', AsyncArtworkDigitalListView.as_view(),
        name='async-artwork-traditional-list'
    ),
    path(
        'traditional/async-artworks', AsyncArtworkTraditionalListView.as_view(),
        name='async-artwork-traditional-list'
    ),
]
