from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.models import Site
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from .forms import SiteProfileForm
from .models import SiteProfile


class SiteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sites.view_site',)

    def get(self, request, *args, **kwargs):
        sites = Site.objects.all()
        return render(request, 'dj_site_accounts/sites_profiles/index.html', {
            "sites": sites,
            "title": _("Sites"),
            "can_delete": sites.count() > 1,
            "breadcrumb": [
                {"url": "/", "title": _("Home")},
                {"title": _("Sites")},
            ]
        })


class SiteCreateOrUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):

    def get_permission_required(self):
        return ('sites.change_site',) if self.kwargs.get('site_id', None) else ('sites.add_site',)

    def get_title(self):
        return _("Edit Site") if self.kwargs.get('site_id', None) else _("Add New Site")

    def get_breadcrumb(self):
        breadcrumb = [
            {"url": "/", "title": _("Home")},
            {"url": reverse('sites-view'), "title": _("Sites")},
        ]
        if self.kwargs.get('site_id', None):
            breadcrumb.append({"title": _("Edit Site")})
        else:
            breadcrumb.append({"title": _("Add New Site")})

        return breadcrumb

    def get_context_data(self):
        return {
            "title": self.get_title(),
            "breadcrumb": self.get_breadcrumb()
        }

    def get(self, request, *args, **kwargs):
        site = None
        if kwargs.get('site_id', None):
            site = get_object_or_404(Site, pk=kwargs.get('site_id'))
            form = SiteProfileForm(instance=site.siteprofile)
        else:
            form = SiteProfileForm()

        return render(request, 'dj_site_accounts/sites_profiles/form.html', {
            "form": form,
            "site": site,
            **self.get_context_data()
        })

    def post(self, request, *args, **kwargs):
        site = None
        if kwargs.get('site_id', None):
            site = get_object_or_404(Site, pk=kwargs.get('site_id'))

            form = SiteProfileForm(request.POST, request.FILES, instance=site.siteprofile, initial={
                'site': site.id
            })
            message = _("Site Updated Successfully!")
        else:
            form = SiteProfileForm(request.POST, request.FILES)
            message = _("Site Created Successfully!")

        if form.is_valid():
            form.save()
            messages.success(request, message)
            return redirect(reverse('sites-view'))

        return render(request, 'dj_site_accounts/sites_profiles/form.html', {
            "form": form,
            "site": site,
            **self.get_context_data()
        })


class SiteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sites.delete_site',)

    def post(self, request, site_id, *args, **kwargs):
        if Site.objects.count() == 1:
            messages.error(request, _("Site can not be deleted if it is the only site exists!"))
        else:
            site = get_object_or_404(Site, pk=site_id)

            site.delete()

            messages.success(request, _("Site Deleted Successfully!"))

        return redirect('sites-view')
