from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

requests_patterns = patterns(
    '',
    url(r'^$', 'apps.hello.views.requests', name="requests"),
    url(r'^list/$', 'apps.hello.views.requests_list', name="requests_list")
)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apps.hello.views.homepage', name="homepage"),
    url(r'^requests/', include(requests_patterns)),
)
