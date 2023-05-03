from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('sites/', include('dj_site_accounts.sites_profiles.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
