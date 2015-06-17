from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
def homepage(request):
    return render(request, "index.html", {"person": User.objects.get(pk=1)})
