from apps.hello.models import Request


class RequestsMiddleware:
    def process_response(self, request, response):
        Request.objects.create(method=request.method,
                               path=request.path,
                               statuscode=response.status_code)
        return response
