import logging
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from apps.hello.models import Request

MAX_REQUESTS = 10

logger = logging.getLogger(__name__)


def homepage(request):
    logger.info(u"Accessed homepage by %s on %s route"
                % (request.method, request.path))
    person = User.objects.get(pk=1)
    logger.debug(u"Returned User object %s with next data: {%s}"
                 % (person,
                    u", ".join(u"'{0}': '{1}'".format(k, v)
                               for k, v in model_to_dict(person).iteritems())))

    return render(request, "index.html", {"person": person})


def requests(request):
    return render(request, "requests.html",
                  {"requests": Request.objects.all()[:MAX_REQUESTS]})


def requests_list(request):
    return HttpResponse(
        serializers.serialize(
            'json',
            list(Request.objects.filter(
                id__gt=request.GET.get("last_id", 0))[:MAX_REQUESTS])
        ),
        content_type="application/json")
