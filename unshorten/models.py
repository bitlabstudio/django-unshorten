"""Models for the ``unshorten`` app."""
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class APICallHistoryBase(models.Model):
    """
    Stores the amount of API calls per user per day or month.

    :amount_api_calls: The actual amount of calls on this day.
    :creation_date: The date these calls are logged.
    :user: Foreignkey to the user, whose calls are stored.

    """
    amount_api_calls = models.PositiveIntegerField(
        verbose_name='API call amount',
    )

    creation_date = models.DateField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='unshorten_profile',
    )

    class Meta:
        abstract = True
        unique_together = ('creation_date', 'user')

    def __str__(self):
        return '{0} ({1})'.format(self.user.email, self.amount_api_calls)


class APICallDayHistory(APICallHistoryBase):
    pass


class APICallMonthHistory(APICallHistoryBase):
    pass


@python_2_unicode_compatible
class UnshortenURL(models.Model):
    """
    Holds the information about a short to long url relation.

    :creation_date: The time it was created.
    :long_url: The long url that resulted out of it.
    :short_url: The short url that needed lookup.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    long_url = models.CharField(
        max_length=4000,
        verbose_name='Long URL',
    )

    short_url = models.CharField(
        max_length=1024,
        verbose_name='Short URL',
    )

    def __str__(self):
        return self.short_url
