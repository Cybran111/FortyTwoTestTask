from apps.hello.models import Request
import settings as hello_settings


class RequestsMiddleware:
    def process_request(self, request):
        """Storing every request that's not in IGNORE_FILTERS to DB"""
        if request.path in hello_settings.REQUESTS_IGNORE_FILTERS:
            return

        Request.objects.create(method=request.method, path=request.path)
