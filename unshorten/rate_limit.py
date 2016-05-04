"""Simple class for rate limiting."""
from django.conf import settings
from django.utils.timezone import now

from .models import APICallDayHistory


class SimpleRateLimit(object):
    """Manages the rate limiting."""

    def __init__(self, request):
        self.user = request.user

    def get_history(self):
        """Returns the history from cache or DB or a newly created one."""
        if hasattr(self, '_history'):
            return self._history
        try:
            self._history = APICallDayHistory.objects.get(
                user=self.user, creation_date=now().date())
        except APICallDayHistory.DoesNotExist:
            self._history = APICallDayHistory(user=self.user)
            self._history.amount_api_calls = 0
        return self._history

    def is_rate_limit_exceeded(self):
        """Returns ``True`` if the rate limit is exceeded, otherwise False."""
        history = self.get_history()
        if history.amount_api_calls >= settings.UNSHORTEN_DAILY_LIMIT:
            return True
        return False

    def log_api_call(self):
        """Increases the amount of logged API calls for the user by 1."""
        history = self.get_history()
        history.amount_api_calls += 1
        self._history = history.save()
        return history
