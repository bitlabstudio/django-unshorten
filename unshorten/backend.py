"""Assigns the RateLimit class from what we import from the settings."""
from django.conf import settings


class_name = settings.UNSHORTEN_RATE_LIMIT_CLASS.split('.')[-1]
module_name = '.'.join(
    settings.UNSHORTEN_RATE_LIMIT_CLASS.split('.')[:-1])
module = __import__(module_name, fromlist=[class_name])
RateLimit = getattr(module, class_name)
