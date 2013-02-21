"""Holds the basic authentication classes for the ``unshorten`` app."""
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import Http404


def get_username(identifier):
    """Checks if a string is a email adress or not."""
    pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    if pattern.match(identifier):
        try:
            user = User.objects.get(email=identifier)
        except:
            raise Http404
        else:
            return user.username
    else:
        return identifier


class SimpleAuthentication(object):
    """
    Provides authentication methods that are run in the API's login decorator.

    """
    def __init__(self, request):
        self.request = request

    def authenticate(self):
        if self.user_logged_in():
            return True
        if self.http_auth():
            return True
        return False

    def http_auth(self):
        """
        Returns ``True`` if valid http auth credentials are found in the
        request header.

        """
        if 'HTTP_AUTHORIZATION' in self.request.META.keys():
            authmeth, auth = self.request.META['HTTP_AUTHORIZATION'].split(
                ' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                identifier, password = auth.split(':', 1)
                username = get_username(identifier)
                user = authenticate(username=username, password=password)
                if user:
                    login(self.request, user)
                    return True

    def user_logged_in(self):
        """Returns ``True`` if the user is logged in."""
        if self.request.user.is_authenticated():
            return True
