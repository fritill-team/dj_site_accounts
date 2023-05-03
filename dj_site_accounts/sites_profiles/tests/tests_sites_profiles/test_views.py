import inspect

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages import get_messages
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from dj_site_accounts.authentication.tests.factories import UserFactory
from ...forms import SiteProfileForm
from ...models import SiteProfile
from ...views import SiteView, SiteCreateOrUpdateView, SiteDeleteView


class SiteViewStructureTestCase(TestCase):
    def test_it_extends_django_View_class(self):
        self.assertTrue(issubclass(SiteView, View))

    def test_it_extends_PermissionRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteView, PermissionRequiredMixin))

    def test_it_extends_LoginRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteView, LoginRequiredMixin))

    def test_permission_required(self):
        self.assertEquals(SiteView.permission_required, ('sites.view_site',))

    def test_view_has_method_get(self):
        self.assertTrue(hasattr(SiteView, 'get'))

    def test_view_has_method_get_is_callable(self):
        self.assertTrue(callable(SiteView.get))

    def test_get_method_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(SiteView.get)[0]
        self.assertEquals(actual_signature, expected_signature)


class SiteViewGETTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('sites-view')
        self.user = UserFactory(is_superuser=True)
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_it_returns_correct_template(self):
        self.assertTemplateUsed(self.response, 'dj_site_accounts/sites_profiles/index.html')

    def test_it_returns_title_in_context(self):
        self.assertIn('title', self.response.context)
        self.assertEqual(self.response.context.get('title'), _("Sites"))

    def test_it_returns_can_delete_in_context(self):
        self.assertIn('can_delete', self.response.context)
        self.assertEqual(self.response.context.get('can_delete'), Site.objects.count() > 1)

    def test_it_returns_breadcrumb_in_context(self):
        self.assertIn('breadcrumb', self.response.context)
        self.assertListEqual(self.response.context.get("breadcrumb"), [
            {"url": "/", "title": _("Home")},
            {"title": _("Sites")},
        ])

    def test_it_returns_all_sites_in_context(self):
        self.assertIn('sites', self.response.context)
        self.assertQuerysetEqual(self.response.context['sites'], Site.objects.all())


class SiteCreateOrUpdateViewStructureTestCase(TestCase):
    def test_it_extends_django_View_class(self):
        self.assertTrue(issubclass(SiteCreateOrUpdateView, View))

    def test_it_extends_PermissionRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteCreateOrUpdateView, PermissionRequiredMixin))

    def test_it_extends_LoginRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteCreateOrUpdateView, LoginRequiredMixin))

    def test_it_has_get_permission_required_method(self):
        self.assertTrue(hasattr(SiteCreateOrUpdateView, 'get_permission_required'))

    def test_view_has_method_get_permission_required_is_callable(self):
        self.assertTrue(callable(SiteCreateOrUpdateView.get_permission_required))

    def test_get_permission_required_method_signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(SiteCreateOrUpdateView.get_permission_required)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_get_method(self):
        self.assertTrue(hasattr(SiteCreateOrUpdateView, 'get'))

    def test_view_has_method_get_is_callable(self):
        self.assertTrue(callable(SiteCreateOrUpdateView.get))

    def test_get_method_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(SiteCreateOrUpdateView.get)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_post_method(self):
        self.assertTrue(hasattr(SiteCreateOrUpdateView, 'post'))

    def test_view_has_method_post_is_callable(self):
        self.assertTrue(callable(SiteCreateOrUpdateView.post))

    def test_post_method_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(SiteCreateOrUpdateView.post)[0]
        self.assertEquals(actual_signature, expected_signature)


class SiteCreateOrUpdateViewGetPermissionRequiredTestCase(TestCase):
    def setUp(self):
        self.create_view = SiteCreateOrUpdateView()
        self.create_view.kwargs = {}
        self.update_view = SiteCreateOrUpdateView()
        self.update_view.kwargs = {"site_id": 1}

    def test_it_returns_add_permission_if_site_id_is_not_present_in_url(self):
        self.assertEquals(('sites.add_site',), self.create_view.get_permission_required())

    def test_it_returns_change_site_permission_if_site_id_is_present_in_url(self):
        self.assertEquals(('sites.change_site',), self.update_view.get_permission_required())


class SiteCreateOrUpdateViewGetTitleTestCase(TestCase):
    def setUp(self):
        self.create_view = SiteCreateOrUpdateView()
        self.create_view.kwargs = {}
        self.update_view = SiteCreateOrUpdateView()
        self.update_view.kwargs = {"site_id": 1}

    def test_it_returns_add_new_site_if_site_id_is_not_present_in_url(self):
        self.assertEquals(_("Add New Site"), self.create_view.get_title())

    def test_it_returns_edit_site_if_site_id_is_present_in_url(self):
        self.assertEquals(_("Edit Site"), self.update_view.get_title())


class SiteCreateOrUpdateViewGetBreadcrumbTestCase(TestCase):
    def setUp(self):
        self.create_view = SiteCreateOrUpdateView()
        self.create_view.kwargs = {}
        self.update_view = SiteCreateOrUpdateView()
        self.update_view.kwargs = {"site_id": 1}

    def test_it_returns_add_breadcrumb_if_site_id_is_not_present_in_url(self):
        self.assertEquals([
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Add New Site")},
        ], self.create_view.get_breadcrumb())

    def test_it_returns_edit_breadcrumb_if_site_id_is_present_in_url(self):
        self.assertEquals([
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Edit Site")},
        ], self.update_view.get_breadcrumb())


class SiteCreateOrUpdateViewGetContextDataTestCase(TestCase):
    def setUp(self):
        self.create_view = SiteCreateOrUpdateView()
        self.create_view.kwargs = {}
        self.update_view = SiteCreateOrUpdateView()
        self.update_view.kwargs = {"site_id": 1}

    def test_it_returns_add_context_data_if_site_id_is_not_present_in_url(self):
        self.assertEquals({
            "title": _("Add New Site"),
            "breadcrumb": [
                {"url": "/", "title": _("Home")},
                {"url": reverse('sites-view'), "title": _("Sites")},
                {"title": _("Add New Site")},
            ]
        }, self.create_view.get_context_data())

    def test_it_returns_edit_context_data_if_site_id_is_present_in_url(self):
        self.assertEquals({
            "title": _("Edit Site"),
            "breadcrumb": [
                {"url": "/", "title": _("Home")},
                {"url": reverse('sites-view'), "title": _("Sites")},
                {"title": _("Edit Site")},
            ]
        }, self.update_view.get_context_data())


class SiteCreateOrUpdateViewGETTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create-site')
        self.test_site = Site.objects.create(domain="test.com", name="test")
        self.edit_url = reverse('edit-site', args=[self.test_site.id])
        self.client.force_login(UserFactory(is_superuser=True))

    def test_template_response(self):
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(response, 'dj_site_accounts/sites_profiles/form.html')

    def test_it_returns_404_if_update_request_is_for_none_existing_site(self):
        response = self.client.get(reverse('edit-site', args=[6]))
        self.assertEquals(404, response.status_code)

    def test_it_returns_create_site_as_title_in_context_for_create_request(self):
        response = self.client.get(self.create_url)
        self.assertIn('title', response.context)
        self.assertEqual(response.context.get('title'), _("Add New Site"))

    def test_it_returns_site_in_context_with_none_value_for_create_request(self):
        response = self.client.get(self.create_url)
        self.assertIn('site', response.context)
        self.assertEqual(response.context.get('site'), None)

    def test_it_returns_site_in_context_with_value_for_update_request(self):
        response = self.client.get(self.edit_url)
        self.assertIn('site', response.context)
        self.assertEqual(response.context.get('site'), self.test_site)

    def test_it_returns_edit_site_as_title_in_context_for_edit_request(self):
        response = self.client.get(self.edit_url)
        self.assertIn('title', response.context)
        self.assertEqual(response.context.get('title'), _("Edit Site"))

    def test_it_returns_breadcrumb_of_create_in_context_for_create_request(self):
        response = self.client.get(self.create_url)
        self.assertIn('breadcrumb', response.context)
        self.assertListEqual(response.context.get("breadcrumb"), [
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Add New Site")},
        ])

    def test_it_returns_breadcrumb_of_edit_in_context_for_edit_request(self):
        response = self.client.get(self.edit_url)
        self.assertIn('breadcrumb', response.context)
        self.assertListEqual(response.context.get("breadcrumb"), [
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Edit Site")},
        ])

    def test_it_returns_empty_SiteProfileForm_in_context_form_for_create_request(self):
        response = self.client.get(self.create_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SiteProfileForm)
        self.assertIsNone(response.context['form'].instance.id)

    def test_it_returns_SiteProfileForm_with_test_site_data_in_context_form_for_edit_request(self):
        response = self.client.get(self.edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SiteProfileForm)
        self.assertEquals(response.context['form'].instance, self.test_site.siteprofile)


class SiteCreateOrUpdateViewPOSTTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create-site')
        self.test_site = Site.objects.create(domain="test.com", name="test")
        # self.test_siteprofile = SiteProfile.objects.create(site=self.test_site,
        #                                                    name={settings.FALLBACK_LOCALE: self.test_site.name})
        self.edit_url = reverse('edit-site', args=[self.test_site.id])
        self.client.force_login(UserFactory(is_superuser=True))
        self.data = {
            "site_id": 2,
            "domain": "test2.com",
            "name": "test2",
            "description": "test",
            "address": "test",
            "copyrights": "test",
            "logo": "",
            "keywords": "test"
        }

    def test_it_redirects_to_sites_view_on_success(self):
        response = self.client.post(self.create_url, self.data)
        self.assertRedirects(response, reverse('sites-view'))

    def test_it_saves_new_instance_on_create(self):
        self.data.pop('site_id')
        self.client.post(self.create_url, self.data)
        self.assertTrue(Site.objects.filter(pk=3).exists())

    def test_it_returns_404_if_update_request_is_for_none_existing_site(self):
        response = self.client.post(reverse('edit-site', args=[6]), self.data)
        self.assertEquals(404, response.status_code)

    def test_it_updates_instance_on_edit(self):
        self.client.post(self.edit_url, self.data)
        self.test_site.refresh_from_db()
        self.assertTrue('test2', self.test_site.name)
        self.assertTrue('test2', self.test_site.siteprofile.name)
        self.assertTrue('test2.com', self.test_site.domain)

    def test_message_site_is_create_successfully_on_create_request(self):
        response = self.client.post(self.create_url, self.data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(_("Site Created Successfully!"), str(messages[0]))

    def test_message_is_updated_successfully_on_update_request(self):
        response = self.client.post(self.edit_url, self.data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(_("Site Updated Successfully!"), str(messages[0]))

    def test_template_response_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.create_url, self.data)
        self.assertTemplateUsed(response, 'dj_site_accounts/sites_profiles/form.html')

    def test_it_returns_create_site_as_title_in_context_for_create_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.create_url, self.data)
        self.assertIn('title', response.context)
        self.assertEqual(response.context.get('title'), _("Add New Site"))

    def test_it_returns_edit_site_as_title_in_context_for_edit_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.edit_url, self.data)
        self.assertIn('title', response.context)
        self.assertEqual(response.context.get('title'), _("Edit Site"))

    def test_it_returns_breadcrumb_of_create_in_context_for_create_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.create_url, self.data)
        self.assertIn('breadcrumb', response.context)
        self.assertListEqual(response.context.get("breadcrumb"), [
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Add New Site")},
        ])

    def test_it_returns_breadcrumb_of_edit_in_context_for_edit_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.edit_url, self.data)
        self.assertIn('breadcrumb', response.context)
        self.assertListEqual(response.context.get("breadcrumb"), [
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
            {"title": _("Edit Site")},
        ])

    def test_it_returns_empty_SiteProfileForm_in_context_form_for_create_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.create_url, self.data)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SiteProfileForm)
        self.assertIsNone(response.context['form'].instance.id)
        self.assertEquals(response.context['form'].data['name'], 'test2')

    def test_it_returns_SiteProfileForm_with_test_site_data_in_context_form_for_edit_request_on_failure(self):
        self.data.pop('domain')
        response = self.client.post(self.edit_url, self.data)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SiteProfileForm)
        self.assertEquals(response.context['form'].instance, self.test_site.siteprofile)
        self.assertEquals(response.context['form'].data['name'], 'test2')


class SiteDeleteViewStructureTestCase(TestCase):
    def test_it_extends_django_View_class(self):
        self.assertTrue(issubclass(SiteDeleteView, View))

    def test_it_extends_PermissionRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteDeleteView, PermissionRequiredMixin))

    def test_it_extends_LoginRequiredMixin_class(self):
        self.assertTrue(issubclass(SiteDeleteView, LoginRequiredMixin))

    def test_permission_required(self):
        self.assertEquals(SiteDeleteView.permission_required, ('sites.delete_site',))

    def test_view_has_method_post(self):
        self.assertTrue(hasattr(SiteDeleteView, 'post'))

    def test_view_has_method_post_is_callable(self):
        self.assertTrue(callable(SiteDeleteView.post))

    def test_post_method_signature(self):
        expected_signature = ['self', 'request', 'site_id']
        actual_signature = inspect.getfullargspec(SiteDeleteView.post)[0]
        self.assertEquals(actual_signature, expected_signature)


class SiteDeleteViewPOSTTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(UserFactory(is_superuser=True))
        self.test_site = Site.objects.create(domain="test.com", name="test")
        self.url = reverse('delete-site', args=[self.test_site.pk])

    def test_it_redirects_to_sites_view(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('sites-view'))

    def test_it_returns_404_if_delete_request_is_for_none_existing_site(self):
        response = self.client.post(reverse('delete-site', args=[6]))
        self.assertEquals(404, response.status_code)

    def test_message_site_is_deleted_successfully_on_request(self):
        response = self.client.post(self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(_("Site Deleted Successfully!"), str(messages[0]))

    def test_it_deletes_requested_site(self):
        self.client.post(self.url)
        self.assertFalse(Site.objects.filter(pk=self.test_site.pk).exists())

    def test_message_site_can_not_be_deleted_if_there_is_only_one_site(self):
        self.test_site.delete()
        response = self.client.post(reverse('delete-site', args=[1]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(_("Site can not be deleted if it is the only site exists!"), str(messages[0]))
        self.assertTrue(Site.objects.filter(pk=1).exists())
