from django import forms
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from translation.models import TranslatableModel

from dj_site_accounts.sites_profiles.signals import create_site_profile_created_site_signal


class SiteProfile(TranslatableModel):
    translatable = {
        "name": {"field": forms.CharField, "widget": forms.Textarea(attrs={
            "class": "form-control bg-transparent",
            "rows": 2,
            "placeholder": _("Site Name")
        })},
        "address": {"field": forms.CharField, "widget": forms.Textarea(attrs={
            "class": "form-control bg-transparent",
            "rows": 2,
            "placeholder": _("Address")
        })},
        "copyrights": {"field": forms.CharField, "widget": forms.Textarea(attrs={
            "class": "form-control bg-transparent",
            "rows": 2,
            "placeholder": _("Copyrights")
        })},
        "description": {"field": forms.CharField, "widget": forms.Textarea(attrs={
            "class": "form-control bg-transparent",
            "rows": 2,
            "placeholder": _("Description")
        })},
        "keywords": {"field": forms.CharField, "widget": forms.Textarea(attrs={
            "class": "form-control bg-transparent",
            "rows": 2,
            "placeholder": _("Keywords")
        })},
    }

    class Meta:
        verbose_name = _("Site Profile")
        verbose_name_plural = _('Sites Profiles')
        default_permissions = ()

    def upload_logo_to(self, filename):
        return 'sites/{}/{}'.format(self.site_id, filename)

    site = models.OneToOneField(Site, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Site"))
    name = models.JSONField(default=dict, verbose_name=_("Name"))
    description = models.JSONField(default=dict, verbose_name=_("Description"))
    address = models.JSONField(default=dict, verbose_name=_("Address"))
    copyrights = models.JSONField(default=dict, verbose_name=_("Copyrights"))
    keywords = models.JSONField(default=dict, verbose_name=_("Keywords"))
    logo = models.FileField(default=None, null=True, blank=True, upload_to=upload_logo_to, verbose_name=_("Logo"))

    def __str__(self):
        return self.translated_name


post_save.connect(create_site_profile_created_site_signal, sender=Site)
