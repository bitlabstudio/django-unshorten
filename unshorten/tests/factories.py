"""Factories for the models of the ``unshorten`` app."""
from factory import Factory, SubFactory

from django_libs.tests.factories import UserFactory

from unshorten.models import APICallDayHistory


class APICallDayHistoryFactory(Factory):
    FACTORY_FOR = APICallDayHistory

    amount_api_calls = 2500
    user = SubFactory(UserFactory)


class APICallMonthHistoryFactory(Factory):
    FACTORY_FOR = APICallDayHistory

    amount_api_calls = 2500
    user = SubFactory(UserFactory)
