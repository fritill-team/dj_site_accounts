from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name="get_lang")
def get_lang(name):
    languages = dict(settings.LANGUAGES)
    if languages[name]:
        return languages[name]
    else:
        return languages[settings.FALLBACK_LOCALE]
