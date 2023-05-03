from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from dj_site_accounts.common.utils import get_settings_value


class HasPhone(models.Model):
    class Meta:
        abstract = True

    phone = PhoneNumberField(unique=True,
                             error_messages={'unique': _("A user with that phone already exists.")})

    phone_verified_at = models.DateTimeField(blank=True, null=True)

    def verify_phone(self):
        self.phone_verified_at = now()
        self.save()


class HasOTPVerification(HasPhone):
    class Meta:
        abstract = True

    key = models.CharField(max_length=100, unique=True, blank=True)

    if get_settings_value('OTP_VERIFICATION_TYPE') == 'HOTP':
        otp_counter = models.IntegerField(default=0)
