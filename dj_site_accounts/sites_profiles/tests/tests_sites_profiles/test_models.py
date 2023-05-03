import inspect

from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.test import TestCase
from django.utils.translation import activate, gettext as _
from translation.models import TranslatableModel

from ....common.utils import DisableSignals
from ...models import SiteProfile


class SiteProfileModelTestCase(TestCase):
    def setUp(self):
        activate(settings.LANGUAGE_CODE)

    def test_it_extends_TranslatableModel_class(self):
        self.assertTrue(issubclass(SiteProfile, TranslatableModel))

    def test_its_class_meta_verbose_name(self):
        self.assertEqual(SiteProfile._meta.verbose_name, _("Site Profile"))

    def test_its_class_meta_verbose_name_plural(self):
        self.assertEqual(SiteProfile._meta.verbose_name_plural, _("Sites Profiles"))

    def test_its_class_meta_default_permissions(self):
        self.assertEqual(SiteProfile._meta.default_permissions, ())

    def test_it_has_translatable_dict(self):
        self.assertTrue(hasattr(SiteProfile, 'translatable'))

    def test_translatable_dict_has_name(self):
        self.assertIn('name', SiteProfile.translatable.keys())
        self.assertTrue(isinstance(SiteProfile.translatable.get('name'), dict))
        self.assertIn('field', SiteProfile.translatable.get('name'))
        self.assertEqual(SiteProfile.translatable.get('name').get('field'), forms.CharField)

    def test_translatable_dict_has_address(self):
        self.assertIn('address', SiteProfile.translatable.keys())
        self.assertTrue(isinstance(SiteProfile.translatable.get('address'), dict))
        self.assertIn('field', SiteProfile.translatable.get('address'))
        field = SiteProfile.translatable.get('address')
        self.assertEqual(field.get('field'), forms.CharField)
        self.assertIsInstance(field.get('widget'), forms.Textarea)

    def test_translatable_dict_has_copyrights(self):
        self.assertIn('copyrights', SiteProfile.translatable.keys())
        self.assertTrue(isinstance(SiteProfile.translatable.get('copyrights'), dict))
        self.assertIn('field', SiteProfile.translatable.get('copyrights'))
        field = SiteProfile.translatable.get('copyrights')
        self.assertEqual(field.get('field'), forms.CharField)
        self.assertIsInstance(field.get('widget'), forms.Textarea)

    def test_translatable_dict_has_description(self):
        self.assertIn('description', SiteProfile.translatable.keys())
        self.assertTrue(isinstance(SiteProfile.translatable.get('description'), dict))
        self.assertIn('field', SiteProfile.translatable.get('description'))
        field = SiteProfile.translatable.get('description')
        self.assertEqual(field.get('field'), forms.CharField)
        self.assertIsInstance(field.get('widget'), forms.Textarea)

    def test_translatable_dict_has_keywords(self):
        self.assertIn('keywords', SiteProfile.translatable.keys())
        self.assertTrue(isinstance(SiteProfile.translatable.get('keywords'), dict))
        self.assertIn('field', SiteProfile.translatable.get('keywords'))
        field = SiteProfile.translatable.get('keywords')
        self.assertEqual(field.get('field'), forms.CharField)
        self.assertIsInstance(field.get('widget'), forms.Textarea)

    def test_it_has_name_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('name'))

    def test_name_field_is_instance_of_JSONField(self):
        field = SiteProfile._meta.get_field('name')
        self.assertIsInstance(field, models.JSONField)

    def test_name_field_verbose_name_is_Name(self):
        field = SiteProfile._meta.get_field('name')
        self.assertEquals(field.verbose_name, _('Name'))

    def test_name_field_default_value_is_empty_dict(self):
        field = SiteProfile._meta.get_field('name')
        self.assertEquals(field.default, dict)

    def test_it_has_description_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('description'))

    def test_description_field_is_instance_of_JSONField(self):
        field = SiteProfile._meta.get_field('description')
        self.assertIsInstance(field, models.JSONField)

    def test_description_field_verbose_name_is_Description(self):
        field = SiteProfile._meta.get_field('description')
        self.assertEquals(field.verbose_name, _('Description'))

    def test_description_field_default_value_is_empty_dict(self):
        field = SiteProfile._meta.get_field('description')
        self.assertEquals(field.default, dict)

    def test_it_has_address_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('address'))

    def test_address_field_is_instance_of_JSONField(self):
        field = SiteProfile._meta.get_field('address')
        self.assertIsInstance(field, models.JSONField)

    def test_address_field_verbose_name_is_Address(self):
        field = SiteProfile._meta.get_field('address')
        self.assertEquals(field.verbose_name, _('Address'))

    def test_address_field_default_value_is_empty_dict(self):
        field = SiteProfile._meta.get_field('address')
        self.assertEquals(field.default, dict)

    def test_it_has_copyrights_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('copyrights'))

    def test_copyrights_field_is_instance_of_JSONField(self):
        field = SiteProfile._meta.get_field('copyrights')
        self.assertIsInstance(field, models.JSONField)

    def test_copyrights_field_verbose_name_is_Copyrights(self):
        field = SiteProfile._meta.get_field('copyrights')
        self.assertEquals(field.verbose_name, _('Copyrights'))

    def test_copyrights_field_default_value_is_empty_dict(self):
        field = SiteProfile._meta.get_field('copyrights')
        self.assertEquals(field.default, dict)

    def test_it_has_keywords_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('keywords'))

    def test_keywords_field_is_instance_of_JSONField(self):
        field = SiteProfile._meta.get_field('keywords')
        self.assertIsInstance(field, models.JSONField)

    def test_keywords_field_verbose_name_is_Keywords(self):
        field = SiteProfile._meta.get_field('keywords')
        self.assertEquals(field.verbose_name, _('Keywords'))

    def test_keywords_field_default_value_is_empty_dict(self):
        field = SiteProfile._meta.get_field('keywords')
        self.assertEquals(field.default, dict)

    def test_it_has_site_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('site'))

    def test_site_field_verbose_name_is_Site(self):
        field = SiteProfile._meta.get_field('site')
        self.assertEquals(field.verbose_name, _('Site'))

    def test_site_field_is_instance_of_OneToOneField(self):
        field = SiteProfile._meta.get_field('site')
        self.assertIsInstance(field, models.OneToOneField)
        self.assertTrue(field.one_to_one)
        self.assertEqual(field.remote_field.model, Site)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_it_has_upload_logo_to_method(self):
        self.assertTrue(hasattr(SiteProfile, 'upload_logo_to'))
        self.assertTrue(callable(SiteProfile.upload_logo_to))

    def test_upload_logo_to_signature(self):
        expected_signature = ['self', 'filename']
        actual_signature = inspect.getfullargspec(SiteProfile.upload_logo_to)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_upload_logo_to_returns_right_path(self):
        with DisableSignals():
            site = Site.objects.create(
                name="Test",
                domain="test.com"
            )
            site_profile = SiteProfile.objects.create(
                site=site,
                name={"en": "test"},
                address={"en": "test"},
                description={"en": "test"},
                copyrights={"en": "test"},
                keywords={"en": "test"},
            )

            self.assertEqual(site_profile.upload_logo_to('test.png'), 'sites/{}/test.png'.format(site.id))

    def test_it_has_logo_field(self):
        self.assertIsNotNone(SiteProfile._meta.get_field('logo'))

    def test_logo_field_is_instance_of_FileField(self):
        field = SiteProfile._meta.get_field('logo')
        self.assertIsInstance(field, models.FileField)

    def test_logo_field_verbose_name_is_Logo(self):
        field = SiteProfile._meta.get_field('logo')
        self.assertEquals(field.verbose_name, _('Logo'))

    def test_logo_field_default_value_is_null(self):
        field = SiteProfile._meta.get_field('logo')
        self.assertIsNone(field.default)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_logo_field_upload_to_is_the_method_upload_logo_to(self):
        field = SiteProfile._meta.get_field('logo')
        self.assertIs(field.upload_to, SiteProfile.upload_logo_to)
