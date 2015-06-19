from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from apps.hello.models import Request

MAX_REQUESTS = 10


def homepage(request):
    return render(request, "index.html", {"person": User.objects.get(pk=1)})


def requests(request):
    return render(request, "requests.html",
                  {"requests": Request.objects.all()[:MAX_REQUESTS]})


def requests_list(request):
    return HttpResponse(
        serializers.serialize(
            'json',
            list(
                Request.objects.filter(
                    id__gt=request.GET.get("last_id", 0)
                )[:MAX_REQUESTS])
        ),
        content_type="application/json")
