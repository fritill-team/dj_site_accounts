AUTHENTICATION_BACKENDS = (
    'dj_site_accounts.authentication.backends.MultipleAuthenticationBackend',
)

AUTH_USER_MODEL = 'tests.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# django restFramework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

REST_SESSION_LOGIN = True
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt_access_token'
JWT_AUTH_REFRESH_COOKIE = 'jwt_refresh_token'
OLD_PASSWORD_FIELD_ENABLED = True

REST_AUTH_SERIALIZERS = {
    "PASSWORD_RESET_SERIALIZER": "apps.users.auth.serializers.PasswordResetSerializer"
}
