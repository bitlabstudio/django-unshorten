"""Tests for the views of the ``unshorten`` app."""
import json
import urllib2
from base64 import b64encode
from mock import Mock

from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from unshorten.backend import RateLimit
from unshorten.models import APICallDayHistory, UnshortenURL


class UnshortenAPIViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``UnshortenAPIView`` view class."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory(email='foo@example.com')
        self.short_url = 'http://examp.le/short'
        self.long_url = 'http://example.com/long_url/'
        self.old_rate_limit_exceeded = RateLimit.is_rate_limit_exceeded
        RateLimit.is_rate_limit_exceeded = Mock(return_value=False)
        self.old_urlopen = urllib2.urlopen
        urllib2.urlopen = Mock(return_value=Mock(code=200, url=self.long_url))
        # adding the authorization info to the request header
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic {0}'.format(
            b64encode('{0}:test123'.format(self.user.email)))

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
        resp = self.is_callable()
        self.assertEqual(
            json.loads(resp.content), {'long_url': self.long_url}, msg=(
                'Should return the long url.'))

        self.assertEqual(
            UnshortenURL.objects.all().count(), 1, msg=(
                'Should have created a cached URL.'))

        cache = UnshortenURL.objects.get()
        # I alter the long_url to be sure that it is returned from cache
        cache.long_url = 'cached_url'
        cache.save()

        # tests for caching and logging
        resp = self.is_callable()
        self.assertEqual(
            json.loads(resp.content), {'long_url': 'cached_url'}, msg=(
                'Should return the long url from cache if called again.'))
        history = APICallDayHistory.objects.get()
        self.assertEqual(history.amount_api_calls, 2, msg=(
            'when called again, the amount of api calls should be increased.'))

        # tests for an exceeded rate limit
        RateLimit.is_rate_limit_exceeded = Mock(return_value=True)
        resp = self.client.get(self.get_url(), self.get_data_payload())
        self.assertEqual(resp.status_code, 403, msg=(
            'When the rate limit is exceeded, accessing the view should'
            ' not be permitted.'))

        # tests for an urlopen exception
        self.short_url = 'foo'
        RateLimit.is_rate_limit_exceeded = Mock(return_value=False)
        urllib2.urlopen = Mock(side_effect=urllib2.URLError('foo'))
        resp = self.client.get(self.get_url(), data=self.get_data_payload())
        self.assertEqual(resp.content, 'null', msg=(
            'Should return the long url.'))
