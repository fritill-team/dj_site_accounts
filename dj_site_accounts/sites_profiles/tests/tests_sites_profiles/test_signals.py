import inspect

from django.contrib.sites.models import Site
from django.test import TestCase

from ....authentication.apps import AuthenticationConfig
from ....common.utils import DisableSignals
from ...models import SiteProfile
from ...signals import create_site_profile_for_initial_sites, create_site_profile_created_site_signal


class CreateSiteProfileForInitialSitesTestCase(TestCase):
    def test_signature(self):
        expected_signature = ['sender']
        actual_signature = inspect.getfullargspec(create_site_profile_for_initial_sites)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_creates_site_profile_for_each_site(self):
        with DisableSignals():
            create_site_profile_for_initial_sites(AuthenticationConfig)
            self.assertTrue(all([isinstance(site.siteprofile, SiteProfile) for site in Site.objects.all()]))


class CreateSiteProfileForCreatedSiteSignalTestCase(TestCase):
    def test_signature(self):
        expected_signature = ['sender', 'instance', 'created']
        actual_signature = inspect.getfullargspec(create_site_profile_created_site_signal)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_creates_site_profile_for_created_site(self):
        with DisableSignals():
            site = Site.objects.create(name="Test", domain="test.com")
            create_site_profile_created_site_signal(Site, site, created=True)
            self.assertIsInstance(site.siteprofile, SiteProfile)
