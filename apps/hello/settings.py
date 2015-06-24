from django.core.urlresolvers import reverse
# For using in hello/requests views and middleware
REQUESTS_IGNORE_FILTERS = (
    reverse('requests_list'),
)
