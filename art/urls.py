from django.urls import path

from art.views import (
    ArtworkDetailView,
    ArtworkListView,
    ArtworTraditionalkListView,
)
from spirsa.constants import HOME_URL_NAME


urlpatterns = [
    path('', ArtworkListView.as_view(), name=HOME_URL_NAME),
    path('traditional/', ArtworTraditionalkListView.as_view(), name='traditional'),
    path('artwork/<slug:slug>/', ArtworkDetailView.as_view(), name='artwork-detail'),
]
