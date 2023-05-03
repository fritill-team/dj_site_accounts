# Application definition

INSTALLED_APPS = [
    # package installations
    'translation',
    'base_template',
    # authentication
    'dj_site_accounts.authentication',
    'dj_site_accounts.authentication.tests',
    'rest_framework_simplejwt.token_blacklist',

    # sites profiles
    'dj_site_accounts.sites_profiles',
    'dj_site_accounts.sites_profiles.tests.tests_sites_profiles',
    
    # django packages
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]
