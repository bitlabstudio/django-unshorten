"""Tests for the simple rate limiting classes of the ``unshorten`` app."""
from mock import Mock

from django.conf import settings
from django.test import TestCase

from mixer.backend.django import mixer

from ..backend import RateLimit
from ..models import APICallDayHistory


class SimpleRateLimitTestCase(TestCase):
    """Tests for the ``SimpleRateLimit`` class."""
    longMessage = True

    def setUp(self):
        self.history = mixer.blend('unshorten.APICallDayHistory',
                                   amount_api_calls=2500)
        self.request = Mock(user=self.history.user)

    def test_is_rate_limit_exceeded(self):
        """Test for the ``is_rate_limit_exceeded`` method."""
        rate_limit = RateLimit(self.request)
        self.assertEqual(rate_limit.is_rate_limit_exceeded(), False, msg=(
            'Rate limit should not be exceeded.'))

        rate_limit = RateLimit(self.request)
        self.history.amount_api_calls = settings.UNSHORTEN_DAILY_LIMIT
        self.history.save()

        self.assertEqual(rate_limit.is_rate_limit_exceeded(), True, msg=(
            'Rate limit should be exceeded.'))

        rate_limit = RateLimit(self.request)
        self.history.delete()
        self.assertEqual(rate_limit.is_rate_limit_exceeded(), False, msg=(
            'Rate limit should not be exceeded if no history is logged.'))

    def test_log_api_call(self):
        """Test for the ``log_api_call`` method."""
        rate_limit = RateLimit(self.request)
        history = rate_limit.log_api_call()
        self.assertEqual(APICallDayHistory.objects.all().count(), 1, msg=(
            'Should create a APICallDayHistory object.'))
        self.assertEqual(
            history.amount_api_calls, self.history.amount_api_calls + 1, msg=(
                'The amount of api calls should have increased.'))
