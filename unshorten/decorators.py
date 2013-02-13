"""Decorators for the ``unshorten`` app."""
import urlparse
import re
from functools import wraps

from django.conf import settings
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login


def get_username(identifier):
    """Checks if a string is a email adress or not."""
    pattern = re.compile('\w+@\w+\..+')
    if pattern.match(identifier):
        try:
            user = User.objects.get(email=identifier)
        except:
            raise Http404
        else:
            return user.username
    else:
        return identifier


def http_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if "HTTP_AUTHORIZATION" in request.GET.keys():
            authmeth, auth = request.GET['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                identifier, password = auth.split(':', 1)
                username = get_username(identifier)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return func(request, *args, **kwargs)
                else:
                    raise Http404
    return _decorator
