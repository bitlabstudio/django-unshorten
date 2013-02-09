"""Views for the ``unshorten`` app."""
import httplib
import json
import urllib2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View


class UnshortenAPIView(View):
    """API view to handle the unshortening."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # importing and instantiating the rate limit the class
        class_name = settings.UNSHORTEN_RATE_LIMIT_CLASS.split('.')[-1]
        module_name = '.'.join(
            settings.UNSHORTEN_RATE_LIMIT_CLASS.split('.')[:-1])
        module = __import__(module_name, fromlist=[class_name])
        RateLimit = getattr(module, class_name)
        rate_limit = RateLimit(request)

        # checking if rate limit is exceeded
        if rate_limit.is_rate_limit_exceeded(request.user):
            raise PermissionDenied
        self.short_url = request.GET.get('url')
        return super(UnshortenAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.short_url:
            try:
                resp = urllib2.urlopen(self.short_url)
            except (
                    urllib2.HTTPError, urllib2.URLError,
                    httplib.HTTPException):
                return HttpResponse(json.dumps(None))
            else:
                if resp.code == 200:
                    return HttpResponse(json.dumps({'long_url': resp.url}))
        return HttpResponse(json.dumps(None))
