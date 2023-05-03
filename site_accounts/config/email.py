import distutils
import os

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = os.environ.get('EMAIL_PORT', None)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', None)
use_ssl = bool(distutils.util.strtobool(os.environ.get('EMAIL_USE_SSL', "false")))
use_tls = bool(distutils.util.strtobool(os.environ.get('EMAIL_USE_TLS', "false")))
if use_tls:
    EMAIL_USE_TLS = True

if use_ssl:
    EMAIL_USE_SSL = True
