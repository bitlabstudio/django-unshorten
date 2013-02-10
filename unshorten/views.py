"""Views for the ``unshorten`` app."""
import httplib
import json
import urllib2

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import View

from unshorten.backend import RateLimit
from unshorten.models import APICallDayHistory


class UnshortenAPIView(View):
    """API view to handle the unshortening."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        rate_limit = RateLimit(request)

        # checking if rate limit is exceeded
        if rate_limit.is_rate_limit_exceeded(request.user):
            raise PermissionDenied
        self.short_url = request.GET.get('url')
        return super(UnshortenAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.short_url:
            try:
                history = APICallDayHistory.objects.get(
                    user=request.user, creation_date=now().date())
            except APICallDayHistory.DoesNotExist:
                history = APICallDayHistory(user=request.user)
                history.amount_api_calls = 1
            else:
                history.amount_api_calls += 1
            history.save()
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
