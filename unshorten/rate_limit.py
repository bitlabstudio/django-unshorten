"""Base classes for rate limiting."""
from django.utils.timezone import now

from unshorten.models import APICallDayHistory


class RateLimit(object):
    """Manages the rate limiting."""

    def __init__(self, request):
        self.user = request.user
        self.request = request

    def is_rate_limit_exceeded(self):
        # TODO At the moment, this serves only testing purposes.
        return False

    def log_api_call(self):
        try:
            history = APICallDayHistory.objects.get(
                user=self.request.user, creation_date=now().date())
        except APICallDayHistory.DoesNotExist:
            history = APICallDayHistory(user=self.request.user)
            history.amount_api_calls = 1
        else:
            history.amount_api_calls += 1
        history.save()
