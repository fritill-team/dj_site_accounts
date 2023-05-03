from django.test import TestCase
from django.urls import reverse, resolve

from dj_site_accounts.sites_profiles.views import SiteView, SiteCreateOrUpdateView, SiteDeleteView


class SitesProfilesUrlsTestCase(TestCase):
    def test_sites_view_url_resolves(self):
        url = reverse('sites-view')
        self.assertEqual(resolve(url).func.view_class, SiteView)

    def test_create_site_url_resolves(self):
        url = reverse('create-site')
        self.assertEqual(resolve(url).func.view_class, SiteCreateOrUpdateView)

    def test_edit_site_url_resolves(self):
        url = reverse('edit-site', args=[1])
        self.assertEqual(resolve(url).func.view_class, SiteCreateOrUpdateView)

    def test_delete_site_url_resolves(self):
        url = reverse('delete-site', args=[1])
        self.assertEqual(resolve(url).func.view_class, SiteDeleteView)
