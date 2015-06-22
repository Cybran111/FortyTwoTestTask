from django.core.urlresolvers import reverse
from apps.hello.models import Request


class RequestsMiddleware:
    def process_request(self, request):
        # Can be transformed into list of filters
        if request.path != reverse('requests_list'):
            Request.objects.create(method=request.method, path=request.path)