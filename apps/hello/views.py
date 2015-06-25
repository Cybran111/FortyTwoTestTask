from base64 import b64decode
import json
import logging
import StringIO
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from apps.hello.forms import EditProfileForm
import settings as hello_settings
from apps.hello.models import Request, Profile

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
                post_data = json.loads(request.body)

                temp_img = StringIO.StringIO()
                try:
                    # temp_img.write(post_data["photo"].decode('base64'))
                    temp_img.write(b64decode(post_data["photo"]))
                    del post_data["photo"]

                except (KeyError, TypeError) as e:
                    logger.debug(u"Got a Base64 photo error while parsing: %s" % e)
                    temp_img.write("")
                temp_img.seek(0)
                img = ImageFile(temp_img, "dumbname")
                editform = EditProfileForm(post_data, files={"photo": img})
                if editform.is_valid():
                    person = Profile.objects.get(id=1)
                    person.user.first_name = editform.cleaned_data['first_name']
                    person.user.last_name = editform.cleaned_data['last_name']
                    person.bio = editform.cleaned_data['bio']
                    person.user.email = editform.cleaned_data['email']
                    person.jabber = editform.cleaned_data['jabber']
                    person.user.skype = editform.cleaned_data['skype']
                    person.contacts = editform.cleaned_data['contacts']
                    person.photo = editform.cleaned_data['photo']
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
