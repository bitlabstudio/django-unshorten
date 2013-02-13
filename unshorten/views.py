"""Views for the ``unshorten`` app."""
import httplib
import json
import urllib2

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from unshorten.backend import RateLimit
from unshorten.decorators import http_auth_and_login
from unshorten.models import UnshortenURL


class UnshortenAPIView(View):
    """API view to handle the unshortening."""
    @method_decorator(http_auth_and_login)
    def dispatch(self, request, *args, **kwargs):
        self.rate_limit = RateLimit(request)
        # checking if rate limit is exceeded
        if self.rate_limit.is_rate_limit_exceeded():
            raise PermissionDenied
        self.short_url = request.GET.get('url')
        return super(UnshortenAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.short_url:
            self.rate_limit.log_api_call()
            try:
                cached_url = UnshortenURL.objects.get(short_url=self.short_url)
            except UnshortenURL.DoesNotExist:
                cached_url = UnshortenURL(short_url=self.short_url)
            else:
                return HttpResponse(
                    json.dumps({'long_url': cached_url.long_url}))
            try:
                resp = urllib2.urlopen(self.short_url)
            except (
                    urllib2.HTTPError, urllib2.URLError,
                    httplib.HTTPException):
                pass
            else:
                if resp.code == 200:
                    cached_url.long_url = resp.url
                    cached_url.save()
                    return HttpResponse(json.dumps({'long_url': resp.url}))
        return HttpResponse(json.dumps(None))
