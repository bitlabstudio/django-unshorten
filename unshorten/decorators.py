"""Decorators for the ``unshorten`` app."""
from functools import wraps

from django.http import Http404

from .backend import APIAuthentication


def api_auth(func):
    """
    If the user is not logged in, this decorator looks for basic HTTP auth
    data in the request header.

    """
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        authentication = APIAuthentication(request)
        if authentication.authenticate():
            return func(request, *args, **kwargs)
        raise Http404
    return _decorator
