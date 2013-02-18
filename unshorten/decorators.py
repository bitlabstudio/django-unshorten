"""Decorators for the ``unshorten`` app."""
import re
from functools import wraps

from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def get_username(identifier):
    """Checks if a string is a email adress or not."""
    pattern = re.compile('.+@\w+\..+')
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
        if not request.user.is_authenticated():
            if "HTTP_AUTHORIZATION" in request.META.keys():
                authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
                if authmeth.lower() == 'basic':
                    auth = auth.strip().decode('base64')
                    identifier, password = auth.split(':', 1)
                    username = get_username(identifier)
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
                        return func(request, *args, **kwargs)
        else:
            return func(request, *args, **kwargs)
        raise Http404
    return _decorator
