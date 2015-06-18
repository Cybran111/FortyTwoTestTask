from apps.hello.models import Request


class RequestsMiddleware:
    def process_request(self, request):
        Request.objects.create(method=request.method, path=request.path)
