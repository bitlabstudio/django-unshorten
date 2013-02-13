"""Simple admin registration for ``unshorten`` models."""
from django.contrib import admin

from unshorten.models import (
    APICallDayHistory,
    APICallMonthHistory,
    UnshortenURL,
)


admin.site.register(APICallDayHistory)
admin.site.register(APICallMonthHistory)
admin.site.register(UnshortenURL)
