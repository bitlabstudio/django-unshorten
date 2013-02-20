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
            # since we always check this first, we tie this to the class for
            # later use
            self.history = APICallDayHistory.objects.get(
                user=self.user, creation_date=now().date())
        except APICallDayHistory.DoesNotExist:
            pass
        else:
            if self.history.amount_api_calls >= settings.UNSHORTEN_DAILY_LIMIT:
                return True
        return False

    def log_api_call(self):
        if not hasattr(self, 'history'):
            try:
                self.history = APICallDayHistory.objects.get(
                    user=self.user, creation_date=now().date())
            except APICallDayHistory.DoesNotExist:
                self.history = APICallDayHistory(user=self.user)
                self.history.amount_api_calls = 1
        self.history.amount_api_calls += 1
        self.history.save()
        return self.history
