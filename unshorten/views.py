"""Views for the ``unshorten`` app."""
import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from unshorten.backend import RateLimit
from unshorten.decorators import api_auth
from unshorten.utils import unshorten_url


class UnshortenAPIView(View):
    """API view to handle the unshortening."""
    @method_decorator(api_auth)
    def dispatch(self, request, *args, **kwargs):
        self.rate_limit = RateLimit(request)
        # checking if rate limit is exceeded
        if self.rate_limit.is_rate_limit_exceeded():
            raise PermissionDenied
        self.short_url = request.GET.get('url')
        return super(UnshortenAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.short_url:
            return HttpResponse(json.dumps(None))

        self.rate_limit.log_api_call()
        long_url = unshorten_url(self.short_url)
        return HttpResponse(json.dumps({'long_url': long_url}))
