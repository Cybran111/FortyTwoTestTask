import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from apps.hello.forms import EditProfileForm
import settings as hello_settings
from apps.hello.models import Request

logger = logging.getLogger(__name__)


def homepage(request):
    logger.info(u"Accessed homepage by %s on %s route"
                % (request.method, request.path))
    person = User.objects.get(pk=1)

    if request.user == person:
        return redirect(reverse("editpage"))

    logger.debug(u"Returned User object %s with next data: {%s}"
                 % (person,
                    u", ".join(u"'{0}': '{1}'".format(k, v)
                               for k, v in model_to_dict(person).iteritems())))

    return render(request, "index.html", {"person": person})


@login_required
def editpage(request):
    admin = User.objects.get(id=1)
    if request.user == admin:
        if request.method == 'POST':
            print
            if request.META["CONTENT_TYPE"] == "application/json":
                editform = EditProfileForm(request.POST)
            else:
                return HttpResponseBadRequest()
        else:
            editform = EditProfileForm(initial=admin.profile.to_dict())

        return render(request, "editpage.html", {"editform": editform})
    else:
        return HttpResponseBadRequest()


def requests(request):
    request_models = Request.objects.exclude(
        path__in=hello_settings.REQUESTS_IGNORE_FILTERS
    )[:hello_settings.MAX_REQUESTS]
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
