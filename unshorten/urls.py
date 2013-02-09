"""URLs for the ``unshorten`` app."""
from django.conf.urls.defaults import patterns, url

from unshorten.views import UnshortenAPIView


urlpatterns = patterns(
    '',
    url(r'v1/',
       UnshortenAPIView.as_view(),
       name='unshorten_api',
    ),

)
