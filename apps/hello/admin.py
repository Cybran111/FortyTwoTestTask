from django.contrib import admin
from apps.hello.models import Profile, Request
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstname', 'lastname', 'birth_date', 'jabber')

    def firstname(self, instance):
        return instance.user.first_name

    def lastname(self, instance):
        return instance.user.last_name

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Request)
