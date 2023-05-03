from django import forms
from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils.translation import gettext as _
from translation.forms import TranslatableModelForm

from ...forms import SiteProfileForm
from ...models import SiteProfile


class SiteProfileFormStructureTestCase(TestCase):
    def test_it_extends_TranslatableModelForm(self):
        self.assertTrue(issubclass(SiteProfileForm, TranslatableModelForm))

    def test_form_class_has_meta_class_on_it(self):
        self.assertIn('Meta', SiteProfileForm.__dict__)

    def test_form_class_meta_has_model_on_it(self):
        self.assertIn('model', SiteProfileForm.Meta.__dict__)

    def test_the_model_used_in_the_meta_is_SiteProfile_model(self):
        self.assertEquals(SiteProfile, SiteProfileForm.Meta.model)

    def test_form_class_meta_has_fields_on_it(self):
        self.assertIn('fields', SiteProfileForm.Meta.__dict__)

    def test_form_class_meta_fields_is_a_list(self):
        self.assertEquals(type(SiteProfileForm.Meta.fields), tuple)

    def test_class_meta_fields_has_name(self):
        self.assertIn('name', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_site(self):
        self.assertIn('site', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_description(self):
        self.assertIn('description', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_address(self):
        self.assertIn('address', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_copyrights(self):
        self.assertIn('copyrights', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_keywords(self):
        self.assertIn('keywords', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_logo(self):
        self.assertIn('logo', SiteProfileForm.Meta.fields)

    def test_class_meta_fields_has_domain(self):
        self.assertIn('domain', SiteProfileForm.Meta.fields)
        self.assertIsInstance(SiteProfileForm().fields['domain'], forms.URLField)

    def test_meta_class_has_widgets_dict(self):
        self.assertIn('widgets', SiteProfileForm._meta.__dict__)

    def test_site_field_widget_is_hidden(self):
        self.assertIn('site', SiteProfileForm._meta.widgets)
        self.assertIsInstance(SiteProfileForm().fields['site'].widget, forms.HiddenInput)


class SiteProfileFormValidationTestCase(TestCase):
    def setUp(self):
        self.form = SiteProfileForm
        self.data = {
            "site": None,
            "domain": "test.com",
            "name": "test",
            "description": "test",
            "address": "test",
            "copyrights": "test",
            "logo": "",
            "keywords": "test"
        }

    def test_form_is_not_valid_if_name_is_not_present(self):
        self.data.pop("name")
        form = self.form(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.as_data()['name'][0].code, 'required')
        self.assertEqual(form.errors['name'][0], _("This field is required."))

    def test_from_is_not_valid_if_domain_is_not_present(self):
        self.data.pop("domain")
        form = self.form(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.as_data()['domain'][0].code, 'required')
        self.assertEqual(form.errors['domain'][0], _("This field is required."))

    def test_form_is_valid_if_site_is_not_present(self):
        self.data.pop('site')
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_if_keywords_is_not_present(self):
        self.data.pop('keywords')
        form = self.form(data=self.data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_form_is_valid_if_copyrights_is_not_present(self):
        self.data.pop('copyrights')
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_if_address_is_not_present(self):
        self.data.pop('address')
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_if_description_is_not_present(self):
        self.data.pop('description')
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())


class SiteProfileFormSaveTestCase(TestCase):
    def setUp(self):
        self.form = SiteProfileForm
        self.data = {
            "site_id": 1,
            "domain": "test.com",
            "name": "test",
            "description": "test",
            "address": "test",
            "copyrights": "test",
            "logo": "",
            "keywords": "test"
        }

    def test_it_creates_new_site_if_site_not_present_in_data_or_none(self):
        self.data.pop('site_id')
        form = self.form(data=self.data)
        form.is_valid()
        instance = form.save()
        self.assertTrue(Site.objects.filter(pk=instance.site_id).exists())

    def test_it_updates_existing_siteprofile_instance(self):
        data = {**self.data}
        data.pop('domain')
        print(SiteProfile.objects.all())
        siteprofile = SiteProfile.objects.get(pk=1)
        self.data.update({"name": "test2"})
        form = self.form(instance=siteprofile, data=self.data)
        form.is_valid()
        self.assertEquals(siteprofile.name, 'test2')

    def test_it_updates_site_on_update(self):
        data = {**self.data}
        data.pop('domain')
        siteprofile = SiteProfile.objects.get(pk=1)
        self.data.update({"name": "test2"})
        self.data.update({"domain": "test2.com"})
        form = self.form(instance=siteprofile, data=self.data)
        form.is_valid()
        instance = form.save()
        self.assertEquals('test2', instance.site.name)
        self.assertEquals('test2.com', instance.site.domain)
