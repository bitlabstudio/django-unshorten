"""Base classes for rate limiting."""


class RateLimit(object):
    """Manages the rate limiting."""

    def __init__(self, request):
        self.user = request.user

    def is_rate_limit_exceeded(self):
        # TODO At the moment, this serves only testing purposes.
        return False
