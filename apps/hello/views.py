from base64 import b64decode
import json
import logging
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.images import ImageFile
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from io import BytesIO
from apps.hello.forms import EditProfileForm
import settings as hello_settings
from apps.hello.models import Request, Profile

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


@login_required
def editpage(request):
    admin = User.objects.get(id=1)
    if request.user == admin:
        if request.method == 'POST':
            if "application/json" in request.META["CONTENT_TYPE"]:
                post_data = json.loads(request.body)
                temp_img = BytesIO()

                if post_data.get("photo", None):
                    m = re.search(
                        r"data:image/(?P<datatype>.+);base64,(?P<data>.+)",
                        post_data["photo"],
                        re.M)
                    if m:
                        datatype = m.group('datatype')
                        temp_img.write(b64decode(m.group("data")))
                        temp_img.seek(0)
                        img = ImageFile(temp_img, "admin")
                    else:
                        img = ImageFile("", "dumbname")
                else:
                    img = admin.profile.photo

                editform = EditProfileForm(post_data, files={"photo": img})
                if editform.is_valid():
                    data = editform.cleaned_data
                    person = Profile.objects.get(id=1)
                    person.user.first_name = data['first_name']
                    person.user.last_name = data['last_name']
                    person.bio = data['bio']
                    person.user.email = data['email']
                    person.jabber = data['jabber']
                    person.user.skype = data['skype']
                    person.contacts = data['contacts']
                    if img != admin.profile.photo:
                        person.photo.save("photo."+datatype, img)
                    person.save()
                    return HttpResponse()

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
