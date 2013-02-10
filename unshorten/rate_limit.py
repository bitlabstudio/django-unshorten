"""Simple class for rate limiting."""
from django.conf import settings
from django.utils.timezone import now

from unshorten.models import APICallDayHistory


class SimpleRateLimit(object):
    """Manages the rate limiting."""

    def __init__(self, request):
        self.user = request.user

    def is_rate_limit_exceeded(self):
        try:
            history = APICallDayHistory.objects.get(
                user=self.user, creation_date=now().date())
        except APICallDayHistory.DoesNotExist:
            pass
        else:
            if history.amount_api_calls >= settings.UNSHORTEN_DAILY_LIMIT:
                return True
        return False

    def log_api_call(self):
        try:
            history = APICallDayHistory.objects.get(
                user=self.user, creation_date=now().date())
        except APICallDayHistory.DoesNotExist:
            history = APICallDayHistory(user=self.user)
            history.amount_api_calls = 1
        else:
            history.amount_api_calls += 1
        history.save()
        return history
