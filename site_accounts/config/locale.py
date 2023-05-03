from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en-us'

FALLBACK_LOCALE = 'en-us'
MAIN_LANGUAGE = 'en-us'
LANGUAGES = [
    ("en-us", _("English United States")),
    ("ar", _("Arabic"))
]

LANGUAGES_KEYS = [
    'en', 'ar', 'en-us'
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
