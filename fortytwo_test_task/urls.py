from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

requests_patterns = patterns(
    '',
    url(r'^$', 'apps.hello.views.requests', name="requests"),
    url(r'^list/$', 'apps.hello.views.requests_list', name="requests_list")
)

auth_patterns = patterns(
    '',
    url('^login/', auth_views.login, name="login"),
    url('^logout/', auth_views.logout, name="logout"),
)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'apps.hello.views.homepage', name="homepage"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(auth_patterns)),
    url(r'^requests/', include(requests_patterns)),
)
