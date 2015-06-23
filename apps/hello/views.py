import logging
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from apps.hello.forms import EditProfileForm
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


def editpage(request):
    editform = EditProfileForm(request.POST or None)
    return render(request, "editpage.html", {"editform": editform})


def requests(request):
    return render(request, "requests.html",
                  {"requests": Request.objects.all()[:MAX_REQUESTS]})


def requests_list(request):
    if "last_id" not in request.GET:
        return HttpResponseBadRequest()

    return HttpResponse(
        serializers.serialize(
            'json',
            list(Request.objects.filter(id__gt=request.GET["last_id"]))
        ),
        content_type="application/json")
