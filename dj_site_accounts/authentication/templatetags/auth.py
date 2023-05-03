from django import template
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def get_authentication_field_placeholder():
    user_model = get_user_model()
    if hasattr(user_model, 'AUTHENTICATION_FIELDS') and type(user_model.AUTHENTICATION_FIELDS) == list:
        fields = []
        for field_name in user_model.AUTHENTICATION_FIELDS:
            if hasattr(user_model, field_name):
                fields.append(str(user_model._meta.get_field(field_name).verbose_name))
            else:
                fields.append(str(field_name))
        if len(fields) > 1:
            return _("{} or {}").format(', '.join(fields[:-1]), fields[-1])
        return fields[0]
    raise Exception("User model must implement AUTHENTICATION_FIELDS list")
