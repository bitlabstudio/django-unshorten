"""Tests for the models of the ``unshorten`` app."""
from django.test import TestCase

from unshorten.models import (
    APICallDayHistory,
    APICallMonthHistory,
    UnshortenURL,
)


class APICallDayHistoryTestCase(TestCase):
    """Tests for the ``APICallDayHistory`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test if the ``APICallDayHistory`` model instantiates."""
        api_call_day_history = APICallDayHistory()
        self.assertTrue(
            api_call_day_history, msg='Should be correctly instantiated.')


class APICallMonthHistoryTestCase(TestCase):
    """Tests for the ``APICallMonthHistory`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test if the ``APICallMonthHistory`` model instantiates."""
        api_call_month_history = APICallMonthHistory()
        self.assertTrue(
            api_call_month_history, msg='Should be correctly instantiated.')


class UnshortenURLTestCase(TestCase):
    """Tests for the ``UnshortenURL`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test if the ``UnshortenURL`` model instantiates."""
        unshorten_url = UnshortenURL()
        self.assertTrue(unshorten_url, msg='Should be correctly instantiated.')
