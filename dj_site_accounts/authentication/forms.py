from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from translation.forms import TranslatableModelForm

from .models import SiteProfile
from .templatetags.auth import get_authentication_field_placeholder
from .verify_phone import VerifyPhone

UserModel = get_user_model()


class MultipleLoginForm(forms.ModelForm):
    identifier = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": get_authentication_field_placeholder(),
            "class": "form-control bg-transparent"
        }))
    password = forms.CharField(
        label=_("Password"),
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(
        required=False,
        label=_('Remember Me'),
        initial=False)

    error_messages = {
        'required': _("This field is required"),
        'invalid_login': _(
            "Please enter a correct credentials. Note that "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        "invalid_credentials": _("Please enter a correct credentials"),
    }

    class Meta:
        model = UserModel
        fields = ('identifier', 'password', 'remember_me')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(MultipleLoginForm, self).__init__(*args, **kwargs)

    def get_user(self):
        return self.user_cache

    def clean(self):
        identifier = self.cleaned_data.get('identifier', None)
        password = self.cleaned_data.get('password', None)
        remember_me = self.cleaned_data.get('remember_me')

        if not identifier or not password:
            if not identifier:
                self.add_error('identifier', ValidationError(self.error_messages['required'], code='required'))

            if not password:
                self.add_error('password', ValidationError(self.error_messages['required'], code='required'))
        else:
            credentials = {"password": password, 'identifier': identifier}

            self.user_cache = authenticate(request=self.request, **credentials)
            if not self.user_cache:
                raise ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            if not remember_me and self.request:
                self.request.session.set_expiry(0)
                self.request.session.modified = True
            else:
                if not self.user_cache.is_active:
                    raise ValidationError(self.error_messages['inactive'], code='inactive')

        return self.cleaned_data


class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            "placeholder": _("Password"),
            "class": "form-control bg-transparent"
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            "placeholder": _("Password Confirmation"),
            "class": "form-control bg-transparent"
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    toc = forms.BooleanField(
        required=True,
        label=_('terms'),
        initial=False)

    class Meta(BaseUserCreationForm.Meta):
        model = UserModel
        widgets = {
            "password2": forms.PasswordInput(attrs={
                'autocomplete': 'off',
                "placeholder": _("Password Confirmation"),
                "class": "form-control bg-transparent"
            })
        }

    def is_valid(self):
        result = super().is_valid()
        # loop on *all* fields if key '__all__' found else only on errors:
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your username"),
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "placeholder": _("Username"),
            "class": "form-control bg-transparent"
        }))

    first_name = forms.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your first name"),
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "placeholder": _("First Name"),
            "class": "form-control bg-transparent"
        }))

    last_name = forms.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your last name"),
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "placeholder": _("Last Name"),
            "class": "form-control bg-transparent"
        }))

    email = forms.EmailField(
        required=True,
        max_length=100, help_text=_("Required, please provide your email"),
        widget=forms.EmailInput(attrs={
            "autocomplete": "off",
            "placeholder": _("Email"),
            "class": "form-control bg-transparent"
        }))

    phone = forms.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your phone number"),
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "placeholder": _("Phone"),
            "class": "form-control bg-transparent"
        }))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("username", "first_name", "last_name", 'email', 'phone',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if UserModel.objects.filter(phone=phone).exists():
            raise ValidationError("Phone already exists", code="unique")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("Email already exists", code="unique")
        return email


class VerifyPhoneForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(VerifyPhoneForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.cleaned_data.get('code')

        success = VerifyPhone(self.user, self.user.phone).check(code)
        if not success:
            self.add_error('code', ValidationError(_("The provided code is invalid"), code='invalid_code'))

        return self.cleaned_data


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
