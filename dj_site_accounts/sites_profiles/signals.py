from django.conf import settings


def create_site_profile_for_initial_sites(sender, **kwargs):
    from django.contrib.sites.models import Site
    from .models import SiteProfile

    for site in Site.objects.filter(siteprofile__isnull=True):
        SiteProfile.objects.create(
            site=site,
            name={settings.FALLBACK_LOCALE: site.name}
        )


def create_site_profile_created_site_signal(sender, instance, created, **kwargs):
    if created:
        from .models import SiteProfile

        instance.siteprofile = SiteProfile.objects.create(
            site=instance,
            name=instance.name)


def create_key_pre_save_signal(sender, instance, **kwargs):
    """This creates the key for users that don't have keys"""
    if not instance.key:
        from ..common.utils import generate_key
        instance.key = generate_key()
