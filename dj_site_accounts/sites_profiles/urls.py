from django.urls import path

from dj_site_accounts.sites_profiles.views import SiteView, SiteCreateOrUpdateView, SiteDeleteView

urlpatterns = [
    path('', SiteView.as_view(), name="sites-view"),
    path('create/', SiteCreateOrUpdateView.as_view(), name="create-site"),
    path('<int:site_id>/edit/', SiteCreateOrUpdateView.as_view(), name="edit-site"),
    path('<int:site_id>/delete/', SiteDeleteView.as_view(), name="delete-site"),
]
