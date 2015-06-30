from django import template
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models

register = template.Library()


class BadModelException(Exception):
    pass


@register.simple_tag
def editlink(model):
    if not isinstance(model, models.Model) \
            or type(model) not in admin.site._registry:
        raise BadModelException("Can't get link to model edit page in admin. "
                                "Maybe it's not a model "
                                "or model isn't registered in admin panel")

    return reverse('admin:%s_%s_change' % (model._meta.app_label.lower(),
                                           model._meta.object_name.lower()),
                   args=[model.id])
