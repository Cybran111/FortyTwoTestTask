from base64 import b64decode
import json
import logging
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseForbidden
from django.shortcuts import render, redirect
from io import BytesIO
from apps.hello.forms import EditProfileForm
import settings as hello_settings
from apps.hello.models import Request

logger = logging.getLogger(__name__)


def homepage(request):
    logger.info(u"Accessed homepage by %s on %s route"
                % (request.method, request.path))
    person = User.objects.get(username="admin")
    logger.debug(u"Returned User object %s with next data: {%s}"
                 % (person,
                    u", ".join(u"'{0}': '{1}'".format(k, v)
                               for k, v in model_to_dict(person).iteritems())))

    return render(request, "index.html", {"person": person})


@login_required
def editpage(request):
    admin = User.objects.get(username="admin")
    if request.user != admin:
        return HttpResponseForbidden("Only admin can access this page.")

    if request.method == 'POST':
        if "application/json" not in request.META["CONTENT_TYPE"]:
            return HttpResponseBadRequest()

        post_data = json.loads(request.body)
        img, datatype = get_photo(post_data)

        editform = EditProfileForm(post_data, files={
            "photo": img or admin.profile.photo
        })

        if editform.is_valid():
            admin.profile.update_user(editform.cleaned_data)
            if img:
                admin.profile.photo.save("photo.%s" % datatype, img)
            admin.save()
            return HttpResponse()
    else:
        editform = EditProfileForm(initial=admin.profile.to_dict())

    return render(request, "editpage.html", {"person": admin,
                                             "editform": editform})


def get_photo(data):
    encoded_photo = data.get("photo", None)
    if not encoded_photo:
        return None, None
    return parse_b64_photo(data["photo"])


def parse_b64_photo(encoded_photo):
    temp_img = BytesIO()
    parsed_photo = re.search(
        r"data:image/(?P<datatype>.+);base64,(?P<data>.+)",
        encoded_photo,
        re.M)
    datatype = ""
    if parsed_photo:
        datatype = parsed_photo.group('datatype')
        temp_img.write(b64decode(parsed_photo.group("data")))
        temp_img.seek(0)
        img = ImageFile(temp_img, "admin")
    else:
        img = ImageFile("", "empty_photo")
    return img, datatype


def requests(request):
    if request.method == 'POST':
        if request.user != User.objects.get(username="admin"):
            return HttpResponseForbidden()
        req = Request.objects.get(id=request.POST["request"])
        req.priority = request.POST["priority"]
        req.save()
        return redirect(reverse("requests"))

    request_models = Request.objects.exclude(
        path__in=hello_settings.REQUESTS_IGNORE_FILTERS
    )[:hello_settings.MAX_REQUESTS]
    return render(request, "requests.html", {"requests": request_models})


def requests_list(request):
    if "last_count" not in request.GET:
        return HttpResponseBadRequest()

    return HttpResponse(
        serializers.serialize(
            'json',
            list(Request.objects
                 .exclude(path__in=hello_settings.REQUESTS_IGNORE_FILTERS)
                 [request.GET["last_count"]:])
        ),
        content_type="application/json")
