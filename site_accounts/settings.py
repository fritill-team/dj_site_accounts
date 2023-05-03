import sys

from site_accounts.config.apps import *
from site_accounts.config.auth import *
from site_accounts.config.database import *
from site_accounts.config.email import *
from site_accounts.config.locale import *
from site_accounts.config.main import *
from site_accounts.config.middleware import *
from site_accounts.config.templates import *

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3',
    }

from base_template.settings import *
