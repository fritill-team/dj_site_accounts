from django.contrib.auth.views import LoginView as BaseLoginView

from authentication.mixins import LoginGetFormClassMixin
from common.utils import get_settings_value


class LoginView(LoginGetFormClassMixin, BaseLoginView):
    redirect_authenticated_user = True

    def get_template_names(self):
        """
        returns the template based on selected theme in settings
        """
        return ['dj_site_accounts/authentication/themes/{}/login.html'.format(
            get_settings_value('AUTHENTICATION_THEME', 'corporate'))]
