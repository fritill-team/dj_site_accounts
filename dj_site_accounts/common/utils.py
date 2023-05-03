import importlib
from collections import defaultdict

import pyotp
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.signals import *
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


account_activation_token = TokenGenerator()


def send_email_verification(request, user):
    current_site = get_current_site(request)
    mail_subject = _('Activate your account.')
    message = render_to_string('dj_accounts/emails/email_confirmation.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def get_settings_value(settings_key, default_value=None):
    return getattr(settings, settings_key, default_value)


def import_class_or_function(name):
    name_split = name.split('.')
    name = name_split[-1:][0]
    module_name = name_split[:-1]
    return getattr(importlib.import_module('.'.join(module_name)), name)


def get_class_from_settings(settings_key, default_class=None):
    class_name = get_settings_value(settings_key, None)

    if not class_name:
        class_name = default_class

    return import_class_or_function(class_name) if type(class_name) is str else class_name


def get_user_tokens(user):
    tokens = RefreshToken.for_user(user)
    return {
        "access_token": str(tokens.access_token),
        "refresh_token": str(tokens)
    }


def get_errors(errors):
    return {name: error[0] for name, error in errors.items()}


def is_unique(key):
    from django.contrib.auth import get_user_model
    UserModel = get_user_model()
    try:
        UserModel.objects.get(key=key)
    except UserModel.DoesNotExist:
        return True
    return False


def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


class DisableSignals(object):
    def __init__(self, disabled_signals=None):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init, post_init,
            pre_save, post_save,
            pre_delete, post_delete,
            pre_migrate, post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in list(self.stashed_signals):
            self.reconnect(signal)

    def disconnect(self, signal):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal):
        signal.receivers = self.stashed_signals.get(signal, [])
        del self.stashed_signals[signal]


def authenticate_api_user(client, user, ):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(refresh.access_token))
    return client
