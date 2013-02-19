"""Holds utility functions for the ``unshorten`` app."""
import httplib
import urllib2

from .models import UnshortenURL


def unshorten_url(short_url):
    """Unshortens the short_url or returns None if not possible."""
    if not short_url.startswith('http'):
        short_url = 'http://{0}'.format(short_url)

    try:
        cached_url = UnshortenURL.objects.get(short_url=short_url)
    except UnshortenURL.DoesNotExist:
        cached_url = UnshortenURL(short_url=short_url)
    else:
        return cached_url.long_url

    try:
        resp = urllib2.urlopen(short_url)
    except (
            urllib2.HTTPError, urllib2.URLError,
            httplib.HTTPException):
        return None

    if resp.code == 200:
        cached_url.long_url = resp.url
        cached_url.save()
        return resp.url
