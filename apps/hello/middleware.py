from django.core.urlresolvers import reverse
from apps.hello.models import Request


class RequestsMiddleware:
    IGNORE_FILTERS = (
        reverse('requests_list'),
    )

    def process_request(self, request):
        """Storing every request that's not in IGNORE_FILTERS to DB"""
        if request.path in self.IGNORE_FILTERS:
            return

        Request.objects.create(method=request.method, path=request.path)