from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from translation.forms import TranslatableModelForm

from .models import SiteProfile


class SiteProfileForm(TranslatableModelForm):
    domain = forms.URLField(
        required=True,
        initial="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-transparent",
            "placeholder": _("Domain")
        }))

    class Meta:
        model = SiteProfile
        fields = ('domain', 'site', 'name', 'description', 'address', 'copyrights', 'keywords', 'logo')
        widgets = {
            "site": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SiteProfileForm, self).__init__(*args, **kwargs)
        self.fields['site'].required = False
        self.fields['keywords'].required = False
        self.fields['copyrights'].required = False
        self.fields['address'].required = False
        self.fields['description'].required = False
        if self.instance.pk:
            self.fields['domain'].initial = self.instance.site.domain

    def save(self, commit=True):
        domain = self.cleaned_data.pop('domain')
        domain = domain.split('://')[1]
        instance = super().save(commit=False)
        if commit:
            site = self.cleaned_data.get('site', None)
            if not site:
                site = Site.objects.create(
                    domain=domain,
                    name=self.cleaned_data.get('name'))
                instance = site.siteprofile
            else:
                site.name = self.cleaned_data.get('name')
                site.domain = domain
                site.save()
            instance.save()
        return instance
