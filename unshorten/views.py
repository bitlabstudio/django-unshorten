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


class UnshortenAPIView(View):
    """API view to handle the unshortening."""
    @method_decorator(login_required)
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
                resp = urllib2.urlopen(self.short_url)
            except (
                    urllib2.HTTPError, urllib2.URLError,
                    httplib.HTTPException):
                pass
            else:
                if resp.code == 200:
                    return HttpResponse(json.dumps({'long_url': resp.url}))
        return HttpResponse(json.dumps(None))
