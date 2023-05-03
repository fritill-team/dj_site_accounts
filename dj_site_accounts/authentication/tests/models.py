from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _

from dj_site_accounts.authentication.models import HasOTPVerification, HasPhone
from dj_site_accounts.sites_profiles.signals import create_key_pre_save_signal


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, HasOTPVerification):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'email']
    AUTHENTICATION_FIELDS = ['email', 'username', 'phone', 'id']

    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    email = models.EmailField(validators=[email_validator],
                              unique=True, blank=False, null=False)
    email_verified_at = models.DateField(blank=True, null=True)

    username = models.CharField(max_length=150,

                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator], unique=True)

    def __str__(self):
        return self.username

    def clean(self):
        self.email = self.email.lower()


pre_save.connect(create_key_pre_save_signal, sender=User)


class VerboseNameFieldsUser(models.Model):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    AUTHENTICATION_FIELDS = ['email', 'username', 'phone', 'id']

    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    email = models.EmailField(validators=[email_validator],
                              unique=True, blank=False, null=False, verbose_name="Email")
    email_verified_at = models.DateField(blank=True, null=True, verbose_name="Email Verified At")

    username = models.CharField(_('username'), max_length=150,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                unique=True)
    phone = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        error_messages={'unique': _("A user with that phone already exists.")},
        verbose_name="Phone")

    phone_verified_at = models.DateTimeField(blank=True, null=True, verbose_name="Phone verified at")

    def __str__(self):
        return self.username

    def clean(self):
        self.email = self.email.lower()


class NoAuthenticationFieldsUser(models.Model):
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    email = models.EmailField(validators=[email_validator],
                              unique=True, blank=False, null=False, verbose_name="Email")
    email_verified_at = models.DateField(blank=True, null=True, verbose_name="Email Verified At")

    username = models.CharField(_('username'), max_length=150,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                unique=True)
    phone = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        error_messages={'unique': _("A user with that phone already exists.")},
        verbose_name="Phone")

    phone_verified_at = models.DateTimeField(blank=True, null=True, verbose_name="Phone verified at")

    def __str__(self):
        return self.username

    def clean(self):
        self.email = self.email.lower()


class UserPhone(HasPhone):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    under_verification = models.BooleanField(default=False)

