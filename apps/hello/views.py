from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import settings as hello_settings


# Create your views here.
import logging
from apps.hello.models import Request

MAX_REQUESTS = 10

logger = logging.getLogger(__name__)


def homepage(request):
    logger.info("Accessed homepage by %s on %s route"
                % (request.method, request.path))
    person = User.objects.get(pk=1)
    logger.debug("Returned User object %s with next data: %s"
                 % (person, model_to_dict(person)))
    return render(request, "index.html", {"person": person})


def requests(request):
    request_models = Request.objects.exclude(
        path__in=hello_settings.REQUESTS_IGNORE_FILTERS
    )[:MAX_REQUESTS]
    return render(request, "requests.html", {"requests": request_models})


def requests_list(request):
    if "last_id" not in request.GET:
        return HttpResponseBadRequest()

    return HttpResponse(
        serializers.serialize(
            'json',
            list(Request.objects.filter(id__gt=request.GET["last_id"])
                 .exclude(path__in=hello_settings.REQUESTS_IGNORE_FILTERS))
        ),
        content_type="application/json")
