"""Simple admin registration for ``unshorten`` models."""
from django.contrib import admin

from unshorten.models import (
    APICallDayHistory,
    APICallMonthHistory,
    UnshortenURL,
)


class APICallDayHistoryAdmin(admin.ModelAdmin):
    """Custom admin for the ``APICallDayHistory`` model."""
    list_display = ['creation_date', 'email', 'amount_api_calls']
    list_filter = ('user__email', )

    def email(self, obj):
        return obj.user.email


class APICallMonthHistoryAdmin(APICallDayHistoryAdmin):
    """Custom admin for the ``APICallMonthHistory`` model."""


class UnshortenURLAdmin(admin.ModelAdmin):
    """Custom admin for the ``UnshortenURL`` model."""
    list_display = ['short_url', 'long_url', 'creation_date']


admin.site.register(APICallDayHistory, APICallDayHistoryAdmin)
admin.site.register(APICallMonthHistory, APICallMonthHistoryAdmin)
admin.site.register(UnshortenURL, UnshortenURLAdmin)
