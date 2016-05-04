"""URLs for the ``unshorten`` app."""
from django.conf.urls import url

from .views import UnshortenAPIView


urlpatterns = [
    url(r'^api/v1/unshorten/',
        UnshortenAPIView.as_view(),
        name='unshorten_api'),
]
