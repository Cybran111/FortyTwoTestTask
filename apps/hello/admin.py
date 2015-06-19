from django.contrib import admin
from apps.hello.models import Profile, Request
# Register your models here.

admin.site.register((Profile, Request))
