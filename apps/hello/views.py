from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
from apps.hello.models import Request


def homepage(request):
    return render(request, "index.html", {"person": User.objects.get(pk=1)})


def requests(request):
    return render(request, "requests.html",
                  {"requests": Request.objects.all()[:10]})
