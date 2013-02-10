"""Tests for the views of the ``unshorten`` app."""
import json
import urllib2
from mock import Mock

from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from unshorten.backend import RateLimit
from unshorten.models import APICallDayHistory


class UnshortenAPIViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``UnshortenAPIView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.short_url = 'http://examp.le/short'
        self.long_url = 'http://example.com/long_url/'
        self.old_rate_limit_exceeded = RateLimit.is_rate_limit_exceeded
        RateLimit.is_rate_limit_exceeded = Mock(return_value=False)
        self.old_urlopen = urllib2.urlopen
        urllib2.urlopen = Mock(return_value=Mock(code=200, url=self.long_url))

    def get_data_payload(self):
        return {'url': self.short_url}

    def get_view_name(self):
        return 'unshorten_api'

    def tearDown(self):
        RateLimit.is_rate_limit_exceeded = self.old_rate_limit_exceeded
        urllib2.urlopen = self.old_urlopen

    def test_view(self):
        """Test for the ``UnshortenAPIView``."""
        # testing regular functionality
        resp = self.should_be_callable_when_authenticated(self.user)
        self.assertEqual(
            json.loads(resp.content), {'long_url': self.long_url}, msg=(
                'Should return the long url.'))

        # tests for an exceeded rate limit
        RateLimit.is_rate_limit_exceeded = Mock(return_value=True)
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 403, msg=(
            'When the rate limit is exceeded, accessing the view should'
            ' not be permitted.'))

        # tests for an urlopen exception
        RateLimit.is_rate_limit_exceeded = Mock(return_value=False)
        urllib2.urlopen = Mock(side_effect=urllib2.URLError('foo'))
        resp = self.client.get(self.get_url(), data=self.get_data_payload())
        self.assertEqual(resp.content, 'null', msg=(
            'Should return the long url.'))
        history = APICallDayHistory.objects.get()
        self.assertEqual(history.amount_api_calls, 2, msg=(
            'when called again, the amount of api calls should be increased.'))
